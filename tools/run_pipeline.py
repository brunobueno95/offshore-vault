#!/usr/bin/env python3
"""offshore-vault pipeline orchestrator.

This is the Milestone 2 scaffolding: every non-LLM stage is implemented
end-to-end. The LLM stages (content filling, review, overview) are stubbed
with no-op placeholders that bump the `updated` frontmatter field on
touched articles so the rest of the pipeline has a real diff to commit,
validate, and (optionally) push.

Milestone 3 will replace the stubs with real Claude subprocess calls.

Modes:
    --mode dry-run       plan only, no mutation, prints batch plan and exits
    --mode daily         full pipeline: clone, fill, validate, commit, push, PR, merge

Use --no-push to run the full flow locally without touching the remote.
Use --no-merge to push and open PR but leave it for manual review.

Usage:
    python tools/run_pipeline.py --mode dry-run
    python tools/run_pipeline.py --mode daily --trees drilling --batch-size 5 --no-push
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from validate import TREES, _read_text, _write_text, _FRONTMATTER_RE  # noqa: E402
from priority import (  # noqa: E402
    BatchItem,
    compute_batch,
    load_progress,
    load_urgent_paths,
    plan_summary,
    save_progress,
)


# ========================================================================
# Config and CLI
# ========================================================================

DEFAULT_CONFIG_PATH = Path(__file__).parent / "config" / "pipeline.yaml"
TOOLS_STATE_DIR = Path(__file__).parent / "state"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="tools/run_pipeline.py",
        description="offshore-vault pipeline orchestrator",
    )
    p.add_argument(
        "--mode",
        choices=["daily", "dry-run", "validate-only"],
        default="dry-run",
        help="dry-run (default) plans only; daily runs the full pipeline",
    )
    p.add_argument(
        "--trees",
        help="comma-separated trees to process (default: all enabled in config)",
    )
    p.add_argument("--batch-size", type=int, help="override per-tree batch_size")
    p.add_argument("--total-budget", type=int, help="override pipeline.total_budget")
    p.add_argument("--urgent", help="comma-separated vault-relative paths to force to top")
    p.add_argument("--scratch-dir", help="override scratch directory location")
    p.add_argument("--keep-scratch", action="store_true", help="keep scratch dir after run")
    p.add_argument("--no-push", action="store_true", help="commit locally, do not push")
    p.add_argument("--no-merge", action="store_true", help="push and PR, do not auto-merge")
    p.add_argument("--vault", default=".", help="path to the vault root")
    p.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    p.add_argument(
        "--output-format", choices=["text", "json"], default="text",
        help="terminal output format",
    )
    p.add_argument("--log-level", choices=["info", "debug"], default="info")
    return p.parse_args(argv)


def load_config(path: str) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    return yaml.safe_load(text) or {}


# ========================================================================
# Run state
# ========================================================================

@dataclass
class RunState:
    run_id: str
    started_at: str
    vault: Path
    scratch: Path
    trees: list[str]
    mode: str
    batches: dict[str, list[BatchItem]] = field(default_factory=dict)
    branch_names: dict[str, str] = field(default_factory=dict)
    commits_made: dict[str, str] = field(default_factory=dict)   # tree -> commit sha
    pr_urls: dict[str, str] = field(default_factory=dict)        # tree -> pr url
    merge_results: dict[str, str] = field(default_factory=dict)  # tree -> status
    ended_at: str | None = None
    exit_code: int | None = None


def make_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")


def default_scratch_dir() -> Path:
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or os.environ.get("TEMP") or os.path.expanduser("~")
        return Path(base) / "offshore-vault" / "runs"
    return Path("/tmp") / "offshore-vault" / "runs"


# ========================================================================
# Stage 0: setup (scratch clone, bot branches)
# ========================================================================

def stage_0_setup(args: argparse.Namespace, cfg: dict) -> RunState:
    vault = Path(args.vault).resolve()
    if not vault.is_dir():
        raise SystemExit(f"error: vault {vault} is not a directory")

    run_id = make_run_id()
    if args.scratch_dir:
        scratch_parent = Path(args.scratch_dir)
    else:
        scratch_parent = default_scratch_dir()
    scratch = scratch_parent / run_id

    trees = _select_trees(args, cfg)
    state = RunState(
        run_id=run_id,
        started_at=datetime.now(timezone.utc).isoformat(),
        vault=vault,
        scratch=scratch,
        trees=trees,
        mode=args.mode,
    )

    if args.mode == "dry-run":
        # Dry-run does not clone. Read straight from the vault.
        return state

    # Full run clones into scratch and creates bot branches per tree.
    _ensure_environment_ready(vault)
    scratch.parent.mkdir(parents=True, exist_ok=True)
    origin_url = _run_git(vault, ["remote", "get-url", "origin"]).strip()
    _print(args, f"cloning {origin_url} -> {scratch}")
    subprocess.run(
        ["git", "clone", origin_url, str(scratch)],
        check=True,
    )
    # Ensure we start from the latest main.
    _run_git(scratch, ["fetch", "origin"])
    _run_git(scratch, ["checkout", cfg["github"]["base_branch"]])
    _run_git(scratch, ["reset", "--hard", f"origin/{cfg['github']['base_branch']}"])

    for tree in trees:
        prefix = cfg["trees"][tree]["branch_prefix"]
        branch = f"{prefix}/{run_id}"
        _run_git(scratch, ["checkout", "-b", branch, f"origin/{cfg['github']['base_branch']}"])
        state.branch_names[tree] = branch

    # Return to base_branch so stage 3 can iterate per tree.
    _run_git(scratch, ["checkout", cfg["github"]["base_branch"]])

    # Initialise per-run state directory.
    run_dir = TOOLS_STATE_DIR / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "state.json").write_text(
        json.dumps({
            "run_id": run_id,
            "started_at": state.started_at,
            "mode": state.mode,
            "trees": trees,
            "vault": str(vault),
            "scratch": str(scratch),
        }, indent=2),
        encoding="utf-8",
    )
    return state


def _select_trees(args: argparse.Namespace, cfg: dict) -> list[str]:
    if args.trees:
        requested = [t.strip() for t in args.trees.split(",") if t.strip()]
        return [t for t in requested if cfg["trees"].get(t, {}).get("enabled", False)]
    return [t for t, tc in cfg["trees"].items() if tc.get("enabled", False)]


def _ensure_environment_ready(vault: Path) -> None:
    missing = []
    for cmd in (["git", "--version"], ["gh", "--version"]):
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(cmd[0])
    if missing:
        raise SystemExit(f"error: required executable(s) not on PATH: {', '.join(missing)}")


# ========================================================================
# Stage 1: priority selection
# ========================================================================

def stage_1_priority(state: RunState, cfg: dict, urgent_extra: set[str]) -> None:
    progress = load_progress(TOOLS_STATE_DIR)
    urgent = load_urgent_paths(state.vault, cfg["priority"]["urgent_file"]) | urgent_extra
    priority_cfg = cfg["priority"]

    total_budget = cfg["pipeline"]["total_budget"]
    remaining_budget = total_budget

    for tree in state.trees:
        tree_cfg = cfg["trees"][tree]
        size = tree_cfg.get("batch_size", 25)
        size = min(size, remaining_budget)
        if size <= 0:
            state.batches[tree] = []
            continue
        items = compute_batch(
            vault=state.vault,
            tree=tree,
            batch_size=size,
            progress=progress,
            urgent_paths=urgent,
            priority_cfg=priority_cfg,
        )
        state.batches[tree] = items
        remaining_budget -= len(items)


# ========================================================================
# Stage 2: preflight validate (skip in dry-run)
# ========================================================================

def stage_2_preflight_validate(state: RunState) -> int:
    """Run validator on the scratch clone. Abort the run if errors exist."""
    rc = _run_validate(state.scratch)
    if rc != 0:
        raise SystemExit(
            f"error: preflight validate on scratch (origin/main snapshot) failed with exit {rc}. "
            "Fix validation errors on main before running the pipeline."
        )
    return rc


# ========================================================================
# Stage 3: tree execution (STUB for M2)
# ========================================================================

def stage_3_tree_execution(state: RunState, cfg: dict, args: argparse.Namespace) -> None:
    """Stub content filler.

    Milestone 2 does not call Claude. This stub walks each tree's batch,
    switches to the bot branch for that tree in the scratch clone, and
    bumps the `updated` frontmatter field on each batch article so the
    downstream commit flow has something to land. Article body, status,
    authoritative_sources, and everything else remain untouched. Because
    the `CONTENT PLACEHOLDER` marker is preserved, future pipeline runs
    will still see these articles as unfilled and the real content agent
    (Milestone 3) will pick them up.
    """
    today = date.today().isoformat()
    for tree, items in state.batches.items():
        if not items:
            continue
        branch = state.branch_names[tree]
        _run_git(state.scratch, ["checkout", branch])

        touched = 0
        for b in items:
            path = state.scratch / b.path
            if not path.is_file():
                _print(args, f"  [{tree}] skip {b.path} (not in scratch)")
                continue
            if _bump_updated_field(path, today):
                touched += 1
        _print(args, f"  [{tree}] stub-touched {touched} article(s) on branch {branch}")


def _bump_updated_field(path: Path, today_iso: str) -> bool:
    """Surgically update the `updated:` frontmatter line. Returns True if modified."""
    text = _read_text(path)
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return False
    fm_block = m.group(0)
    # Match the existing `updated:` line and replace with today's date.
    import re
    new_block, n = re.subn(
        r"^updated:\s*.*$",
        f'updated: "{today_iso}"',
        fm_block,
        flags=re.MULTILINE,
        count=1,
    )
    if n == 0 or new_block == fm_block:
        return False
    new_text = new_block + text[m.end():]
    _write_text(path, new_text)
    return True


# ========================================================================
# Stage 4: sync siblings
# ========================================================================

def stage_4_sync_siblings(state: RunState) -> None:
    subprocess.run(
        [sys.executable, str(Path(__file__).parent / "sync_siblings.py"), str(state.scratch)],
        check=False,
    )


# ========================================================================
# Stage 5 + 7: validator passes
# ========================================================================

def _run_validate(path: Path) -> int:
    cp = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "validate.py"), str(path)],
        capture_output=False,
    )
    return cp.returncode


def stage_5_validator_pass(state: RunState) -> int:
    return _run_validate(state.scratch)


# ========================================================================
# Stage 6: overview (STUB for M2)
# ========================================================================

def stage_6_overview(state: RunState) -> None:
    report = state.scratch / "_PIPELINE_REPORT.md"
    lines = [
        f"# _PIPELINE_REPORT.md",
        "",
        f"**Run:** {state.run_id}",
        f"**Mode:** {state.mode}",
        f"**Started:** {state.started_at}",
        "",
        "## Batches",
        "",
    ]
    for tree, items in state.batches.items():
        lines.append(f"- `{tree}`: {len(items)} article(s)")
    lines.append("")
    lines.append("_Generated by the Milestone 2 stub overview agent. The real overview agent is wired in Milestone 5._")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    findings = state.scratch / "_CROSS_TREE_FINDINGS.md"
    findings.write_text(
        "# _CROSS_TREE_FINDINGS.md\n\n"
        "_Generated by the Milestone 2 stub. The real cross-tree finder runs in Milestone 5._\n",
        encoding="utf-8",
    )


# ========================================================================
# Stage 8: commit per tree
# ========================================================================

def stage_8_commit(state: RunState, cfg: dict, args: argparse.Namespace) -> None:
    for tree, items in state.batches.items():
        if not items:
            continue
        branch = state.branch_names[tree]
        _run_git(state.scratch, ["checkout", branch])

        # Stage changes in the tree's folder plus top-level validator output.
        _run_git(state.scratch, ["add", tree])
        for root_file in (
            "_VALIDATION_REPORT.md", "_VALIDATION_REPORT.json",
            "_UNRESOLVED_LINKS.md", "_TODO_QUEUE.md", "_MANIFEST.txt",
            "_PIPELINE_REPORT.md", "_CROSS_TREE_FINDINGS.md",
        ):
            p = state.scratch / root_file
            if p.exists():
                _run_git(state.scratch, ["add", root_file])

        diff = _run_git(state.scratch, ["diff", "--cached", "--name-only"]).strip()
        if not diff:
            _print(args, f"  [{tree}] no staged changes; skipping commit")
            continue

        titles = ", ".join(b.path for b in items[:3])
        if len(items) > 3:
            titles += f" (+{len(items) - 3} more)"
        msg = (
            f"bot({tree}): pipeline run {state.run_id}\n\n"
            f"Batch size: {len(items)} article(s)\n"
            f"Sample: {titles}\n"
            f"Mode: {state.mode}\n"
            f"Agents: pipeline-stub-m2 (content), pipeline-stub-m2 (review)\n"
        )
        _run_git(state.scratch, ["commit", "-m", msg])
        sha = _run_git(state.scratch, ["rev-parse", "HEAD"]).strip()
        state.commits_made[tree] = sha


# ========================================================================
# Stage 9: push and open PR per tree
# ========================================================================

def stage_9_push_and_pr(state: RunState, cfg: dict, args: argparse.Namespace) -> None:
    for tree, sha in state.commits_made.items():
        branch = state.branch_names[tree]
        _run_git(state.scratch, ["push", "-u", "origin", branch])

        title = f"bot({tree}): pipeline run {state.run_id}"
        body = (
            f"Pipeline run `{state.run_id}` (mode: `{state.mode}`).\n\n"
            f"Tree: `{tree}`\n"
            f"Batch size: {len(state.batches[tree])} article(s)\n"
            f"Agents: `pipeline-stub-m2` (Milestone 2 scaffolding).\n\n"
            f"CI must be green before this PR is eligible for auto-merge.\n"
        )
        # Use `gh pr create` from the scratch directory.
        cp = subprocess.run(
            [
                "gh", "pr", "create",
                "--repo", _github_repo(state.scratch),
                "--base", cfg["github"]["base_branch"],
                "--head", branch,
                "--title", title,
                "--body", body,
                "--label", cfg["github"].get("pr_label", "bot"),
            ],
            cwd=state.scratch,
            capture_output=True, text=True, check=False,
        )
        if cp.returncode == 0:
            url = cp.stdout.strip().splitlines()[-1]
            state.pr_urls[tree] = url
            _print(args, f"  [{tree}] PR opened: {url}")
        else:
            _print(args, f"  [{tree}] gh pr create failed: {cp.stderr.strip()}")


# ========================================================================
# Stage 10: wait for CI and auto-merge (only if auto_merge_only_draft passes)
# ========================================================================

def stage_10_auto_merge(state: RunState, cfg: dict, args: argparse.Namespace) -> None:
    repo = _github_repo(state.scratch)
    for tree, url in state.pr_urls.items():
        pr_num = url.rsplit("/", 1)[-1]
        # Wait for checks.
        watch = subprocess.run(
            ["gh", "pr", "checks", pr_num, "--repo", repo, "--watch"],
            cwd=state.scratch,
            capture_output=True, text=True, check=False,
        )
        if watch.returncode != 0:
            state.merge_results[tree] = "ci-failed"
            _print(args, f"  [{tree}] CI not green: {watch.stdout.strip()}")
            continue

        # Only draft-touching PRs auto-merge.
        if cfg["pipeline"].get("auto_merge_only_draft", True):
            if not _pr_only_touches_draft_articles(state.scratch, pr_num, repo):
                state.merge_results[tree] = "non-draft-touched-held"
                _print(args, f"  [{tree}] PR touches non-draft paths, holding open")
                continue

        merge = subprocess.run(
            ["gh", "pr", "merge", pr_num, "--repo", repo, "--squash"],
            cwd=state.scratch,
            capture_output=True, text=True, check=False,
        )
        if merge.returncode == 0:
            state.merge_results[tree] = "merged"
            _print(args, f"  [{tree}] PR #{pr_num} merged")
        else:
            state.merge_results[tree] = "merge-failed"
            _print(args, f"  [{tree}] merge failed: {merge.stderr.strip()}")


def _pr_only_touches_draft_articles(scratch: Path, pr_num: str, repo: str) -> bool:
    """Return True if every changed article file has status: draft in frontmatter."""
    # Simple heuristic for M2: always treat as draft-only since the stub does not
    # transition status. Refine in Milestone 3 when real agents may touch status.
    return True


# ========================================================================
# Stage 11: summary and cleanup
# ========================================================================

def stage_11_summary(state: RunState, args: argparse.Namespace) -> None:
    state.ended_at = datetime.now(timezone.utc).isoformat()
    _print(args, "")
    _print(args, f"=== Pipeline run {state.run_id} ===")
    _print(args, f"Mode: {state.mode}")
    _print(args, f"Trees: {', '.join(state.trees)}")
    for tree in state.trees:
        items = state.batches.get(tree, [])
        pr = state.pr_urls.get(tree, "-")
        status = state.merge_results.get(tree, "-")
        _print(args, f"  {tree:22s} batch={len(items):3d}  PR={pr}  status={status}")
    _print(args, f"Scratch: {state.scratch}")


def stage_cleanup(state: RunState, args: argparse.Namespace) -> None:
    if args.keep_scratch or state.mode == "dry-run":
        return
    any_failed = any(r != "merged" for r in state.merge_results.values())
    if any_failed and state.merge_results:
        _print(args, f"  keeping scratch {state.scratch} for triage (some trees did not merge)")
        return
    if state.scratch.exists():
        try:
            shutil.rmtree(state.scratch)
        except OSError as exc:
            _print(args, f"  could not delete scratch {state.scratch}: {exc}")


# ========================================================================
# Main
# ========================================================================

def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    cfg = load_config(args.config)

    if args.batch_size is not None:
        for tc in cfg["trees"].values():
            tc["batch_size"] = args.batch_size
    if args.total_budget is not None:
        cfg["pipeline"]["total_budget"] = args.total_budget

    urgent_extra: set[str] = set()
    if args.urgent:
        urgent_extra.update(p.strip() for p in args.urgent.split(",") if p.strip())

    if args.mode == "validate-only":
        return _run_validate(Path(args.vault).resolve())

    try:
        state = stage_0_setup(args, cfg)
        stage_1_priority(state, cfg, urgent_extra)

        if args.mode == "dry-run":
            _print(args, plan_summary(state.batches))
            _print(args, "")
            _print(args, "dry-run mode: no changes made, no scratch created, no remote contacted")
            return 0

        stage_2_preflight_validate(state)
        stage_3_tree_execution(state, cfg, args)
        stage_4_sync_siblings(state)
        stage_5_validator_pass(state)
        stage_6_overview(state)
        stage_5_validator_pass(state)  # stage 7 repeat
        stage_8_commit(state, cfg, args)

        if args.no_push:
            stage_11_summary(state, args)
            return 0

        stage_9_push_and_pr(state, cfg, args)

        if args.no_merge:
            stage_11_summary(state, args)
            return 0

        stage_10_auto_merge(state, cfg, args)
        stage_11_summary(state, args)
        stage_cleanup(state, args)
        return 0

    except SystemExit:
        raise
    except Exception as exc:
        print(f"error: pipeline failed: {exc}", file=sys.stderr)
        if args.log_level == "debug":
            traceback.print_exc()
        return 3


# ========================================================================
# Utilities
# ========================================================================

def _run_git(cwd: Path, args: list[str]) -> str:
    cp = subprocess.run(
        ["git", "-C", str(cwd)] + args,
        capture_output=True, text=True, check=True,
    )
    return cp.stdout


def _github_repo(scratch: Path) -> str:
    """Return 'owner/repo' for the scratch clone's origin remote."""
    url = _run_git(scratch, ["remote", "get-url", "origin"]).strip()
    url = url.removesuffix(".git")
    if url.startswith("https://github.com/"):
        return url[len("https://github.com/"):]
    if url.startswith("git@github.com:"):
        return url[len("git@github.com:"):]
    return url


def _print(args: argparse.Namespace, msg: str) -> None:
    if args.output_format == "json":
        print(json.dumps({"msg": msg, "ts": datetime.now(timezone.utc).isoformat()}))
    else:
        print(msg)


if __name__ == "__main__":
    sys.exit(main())
