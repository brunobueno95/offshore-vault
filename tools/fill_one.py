#!/usr/bin/env python3
"""Fill a single drilling article by invoking the Claude CLI.

Milestone 3a scaffolding: no pipeline, no batching, no review agent. Just
one article, one Claude subprocess, see what comes out.

Usage:
    python tools/fill_one.py <article_path> [--dry-run]

The article path can be relative to the vault root or absolute. Only
articles under `drilling/` are accepted in M3a; other trees join in later
milestones once the content for drilling is proven.

The Claude subprocess runs with:
    --model claude-opus-4-7
    --permission-mode bypassPermissions
    --add-dir <vault>
    --allowed-tools  Read, Write, Edit, Glob, Grep
    --disallowed-tools  Bash, WebFetch, WebSearch, Task
    --append-system-prompt <tools/prompts/drilling_content_system.md>
    --max-turns 50

It authenticates via your Max subscription (`claude login` session). No
API key is needed.
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
PROMPT_FILE = HERE / "prompts" / "drilling_content_system.md"

ALLOWED_TOOLS = "Read,Write,Edit,Glob,Grep"
DISALLOWED_TOOLS = "Bash,WebFetch,WebSearch,Task"
MODEL = "claude-opus-4-7"
MAX_TURNS = "50"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="tools/fill_one.py",
        description="Fill a single drilling article via the Claude CLI (M3a).",
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
            f"error: fill_one.py supports only the drilling tree in Milestone 3a "
            f"(got tree '{tree}' from path '{rel}')",
            file=sys.stderr,
        )
        return 2

    if not PROMPT_FILE.is_file():
        print(f"error: system prompt file missing: {PROMPT_FILE}", file=sys.stderr)
        return 2

    claude_exe = shutil.which("claude")
    if not claude_exe:
        print(
            "error: `claude` CLI not found on PATH. Install Claude Code and run `claude login` "
            "before using this script.",
            file=sys.stderr,
        )
        return 2

    # Short bootstrap system prompt. The detailed rules live on disk at
    # tools/prompts/drilling_content_system.md. The agent is told to Read
    # them first. Keeping the inline system prompt short is required on
    # Windows, where the cmd.exe argument length limit is about 8 KB.
    system_prompt = (
        "You are `drilling-content-v1`, the content agent for the drilling tree of "
        "offshore-vault. Your single job per invocation: fill one stub article with a "
        "complete body and updated frontmatter, following the vault rules.\n\n"
        "BEFORE you write anything, use the Read tool to read these files in full, in this "
        "order:\n"
        "1. tools/prompts/drilling_content_system.md  (your detailed rulebook, read this FIRST)\n"
        "2. _AGENT_RULES.md                            (vault-wide agent rules)\n"
        "3. _SCHEMA.md                                 (frontmatter schema)\n"
        "4. drilling/CLAUDE.md                         (self-contained tree rules + authority whitelist)\n"
        "5. drilling/_TOPICS.md                        (allowed topics for this tree)\n"
        "6. the target article stub (its current frontmatter and placeholder body)\n"
        "7. the target article's parent folder `_INDEX.md` for folder-scope context\n"
        "8. the sibling articles in the same folder (frontmatter only, for peer context)\n\n"
        "Then write the article body and update the frontmatter fields specified in "
        "`tools/prompts/drilling_content_system.md`, using the Edit or Write tool.\n\n"
        "Rules you must not violate (the detailed rulebook expands every one of these):\n"
        "- Pedagogical accessibility: every acronym, specialist term, and Norwegian term "
        "is expanded or glossed at every single use, not only first use.\n"
        "- No em dashes.\n"
        "- Cite only sources on the drilling authority whitelist in drilling/CLAUDE.md section 5.\n"
        "- Never fabricate a source.\n"
        "- Keep status as draft.\n"
        "- Do not touch files outside the drilling tree.\n"
        "- Do not touch CLAUDE.md, _TOPICS.md, _INDEX.md, or any underscore-prefixed file.\n\n"
        "When finished, output a single final line of the form:\n"
        "  DONE: <article-path> (<word-count> words, <source-count> sources, <depth>)\n"
        "Then stop."
    )

    task = (
        f"Fill the article at `{rel}`.\n\n"
        "Follow the rules in your system prompt and in `tools/prompts/drilling_content_system.md`.\n"
        "Read the rulebook first, then read the target stub and its sibling context, then write.\n\n"
        f"Target article: {rel}\n"
    )

    # Task prompt is piped via stdin to avoid Windows cmd.exe mangling
    # multi-line positional arguments. System prompt goes via flag since
    # it is short enough to fit within the 8 KB argument length limit.
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

    print(f"fill_one: invoking Claude on {rel}")
    print(f"fill_one: claude={claude_exe}")
    print(f"fill_one: model={MODEL}, max_turns={MAX_TURNS}")
    print(f"fill_one: vault={VAULT}")
    print("---")
    result = subprocess.run(cmd, cwd=str(VAULT), input=task, text=True)
    print("---")
    print(f"fill_one: claude exited with code {result.returncode}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
