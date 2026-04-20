#!/usr/bin/env python3
"""Review a single drilling article by invoking the Claude CLI.

Milestone 3b scaffolding: runs the drilling review agent against an
already-filled article. Applies mechanical fixes (em dashes, bare
acronyms, bare Norwegian terms, repetitive common-English glosses,
missing sections) and flags judgment issues as HTML comments. Never
rewrites the article wholesale. Always keeps status as draft.

Usage:
    python tools/review_one.py <article_path> [--dry-run]

The article path can be relative to the vault root or absolute. Only
articles under `drilling/` are accepted in M3b; other trees join in
later milestones.

The Claude subprocess runs with:
    --model claude-opus-4-7
    --permission-mode bypassPermissions
    --add-dir <vault>
    --allowed-tools  Read, Write, Edit, Glob, Grep
    --disallowed-tools  Bash, WebFetch, WebSearch, Task
    --append-system-prompt <short bootstrap>
    --max-turns 50

It authenticates via your Max subscription (`claude login` session).
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = HERE.parent
PROMPT_FILE = HERE / "prompts" / "drilling_review_system.md"

ALLOWED_TOOLS = "Read,Write,Edit,Glob,Grep"
DISALLOWED_TOOLS = "Bash,WebFetch,WebSearch,Task"
MODEL = "claude-opus-4-7"
MAX_TURNS = "50"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="tools/review_one.py",
        description="Review a single drilling article via the Claude CLI (M3b).",
    )
    p.add_argument("article", help="path to the article (relative to vault root or absolute)")
    p.add_argument("--dry-run", action="store_true", help="build the command and print it, do not execute")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    article_arg = Path(args.article)
    if article_arg.is_absolute():
        article_path = article_arg
    else:
        article_path = (VAULT / article_arg).resolve()

    if not article_path.is_file():
        print(f"error: article {article_path} does not exist", file=sys.stderr)
        return 2

    try:
        rel = article_path.relative_to(VAULT).as_posix()
    except ValueError:
        print(f"error: article {article_path} is not inside the vault {VAULT}", file=sys.stderr)
        return 2

    tree = rel.split("/", 1)[0]
    if tree != "drilling":
        print(
            f"error: review_one.py supports only the drilling tree in Milestone 3b "
            f"(got tree '{tree}' from path '{rel}')",
            file=sys.stderr,
        )
        return 2

    claude_exe = shutil.which("claude")
    if not claude_exe:
        print(
            "error: `claude` CLI not found on PATH. Install Claude Code and run `claude login` "
            "before using this script.",
            file=sys.stderr,
        )
        return 2

    if not PROMPT_FILE.is_file():
        print(f"error: system prompt file missing: {PROMPT_FILE}", file=sys.stderr)
        return 2

    # Short bootstrap system prompt. Detailed rules live on disk at
    # tools/prompts/drilling_review_system.md. The agent is told to Read
    # them first. Keeping the inline system prompt short is required on
    # Windows, where the cmd.exe argument length limit is about 8 KB.
    system_prompt = (
        "You are `drilling-review-v1`, the review agent for the drilling tree of "
        "offshore-vault. Your job: surgical review of one already-filled article. "
        "Apply mechanical fixes (em dashes, bare acronyms, bare Norwegian terms, "
        "repetitive common-English glosses, missing required sections, overlong "
        "paragraphs), flag judgment issues as HTML comments in the body, never "
        "rewrite wholesale, always keep status as draft.\n\n"
        "BEFORE you edit anything, use the Read tool to read these files in full, in this "
        "order:\n"
        "1. tools/prompts/drilling_review_system.md  (your detailed rulebook, READ FIRST)\n"
        "2. _AGENT_RULES.md                            (pedagogy rule and agent behaviour)\n"
        "3. _VALIDATION.md                             (what the validator enforces)\n"
        "4. drilling/CLAUDE.md                         (tree rules + authority whitelist)\n"
        "5. the target article (its frontmatter and body)\n\n"
        "Then apply mechanical fixes with the Edit tool and raise flags as HTML comments. "
        "Append \"agent:drilling-review-v1\" to the `authors` list and bump `updated` to "
        "today's ISO date. Do not change any other frontmatter field. Do not transition "
        "status away from draft.\n\n"
        "When finished, output a single final line of the form:\n"
        "  DONE: <article-path> (fixes_applied: <N>, flags_raised: <M>)\n"
        "Then stop."
    )

    task = (
        f"Review the article at `{rel}`.\n\n"
        "Follow the rules in your system prompt and in `tools/prompts/drilling_review_system.md`.\n"
        "Read the rulebook first, then the article, then edit.\n\n"
        f"Target article: {rel}\n"
    )

    cmd = [
        claude_exe, "-p",
        "--model", MODEL,
        "--permission-mode", "bypassPermissions",
        "--add-dir", str(VAULT),
        "--allowed-tools", ALLOWED_TOOLS,
        "--disallowed-tools", DISALLOWED_TOOLS,
        "--append-system-prompt", system_prompt,
        "--max-turns", MAX_TURNS,
    ]

    if args.dry_run:
        print("dry-run: would invoke:")
        for part in cmd:
            if part == system_prompt:
                print("  <short inline system prompt (~1.5 KB)>")
            else:
                print(f"  {part}")
        print(f"  <stdin>: {task.splitlines()[0]} ...")
        return 0

    print(f"review_one: invoking Claude on {rel}")
    print(f"review_one: claude={claude_exe}")
    print(f"review_one: model={MODEL}, max_turns={MAX_TURNS}")
    print(f"review_one: vault={VAULT}")
    print("---")
    result = subprocess.run(cmd, cwd=str(VAULT), input=task, text=True)
    print("---")
    print(f"review_one: claude exited with code {result.returncode}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
