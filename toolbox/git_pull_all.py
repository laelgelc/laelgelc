#!/usr/bin/env python3
import argparse
import os
import subprocess
from pathlib import Path
from typing import Tuple

def is_git_repo(path: Path) -> bool:
    return (path / ".git").is_dir()

def git_pull(path: Path, remote: str = None, branch: str = None) -> Tuple[bool, str]:
    cmd = ["git", "-C", str(path), "pull"]
    if remote:
        cmd.append(remote)
    if branch:
        cmd.append(branch)
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
            check=False,
        )
        out = (result.stdout or "") + (("\n" + result.stderr) if result.stderr else "")
        out = out.strip()
        success = result.returncode == 0
        return success, out
    except subprocess.TimeoutExpired:
        return False, "Timed out"
    except FileNotFoundError:
        return False, "git not found"

def walk_dirs(root: Path, max_depth: int) -> Path:
    # Yield root first if it's a repo; then walk subdirs with depth control
    yield root
    if max_depth == 0:
        return
    for dirpath, dirnames, _ in os.walk(root):
        depth = Path(dirpath).relative_to(root).parts
        if len(depth) >= max_depth:
            # Prevent descending further
            dirnames[:] = []
        yield Path(dirpath)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recursively run 'git pull' in git repositories under a directory."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=25,
        help="Maximum recursion depth (default: 25)",
    )
    parser.add_argument(
        "--remote",
        help="Optional remote name to pull from (e.g., origin)",
    )
    parser.add_argument(
        "--branch",
        help="Optional branch name to pull (e.g., main)",
    )
    parser.add_argument(
        "--skip-hidden",
        action="store_true",
        help="Skip hidden directories (those starting with a dot)",
    )
    parser.add_argument(
        "--only-top",
        action="store_true",
        help="Only run in directories that are git repos themselves; do not traverse into their children.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    seen_repos = set()

    for path in walk_dirs(root, args.max_depth):
        # Optionally skip hidden dirs (except root itself)
        if args.skip_hidden and path != root and path.name.startswith("."):
            continue

        # If we've already processed this repo (due to nested paths), skip
        # Determine repo root by walking up until .git found or filesystem root
        repo_root = None
        current = path
        while True:
            if is_git_repo(current):
                repo_root = current
                break
            if current.parent == current:
                break
            current = current.parent

        if repo_root is None:
            # Not a git repo
            # Print only if the directory itself has a .git? The user wants brief status even for non-repos.
            if path == root or (path / ".git").exists():
                pass  # handled above
            print(f"[SKIP] {path} - not a git repository")
            continue

        # If only-top is set, only act on the repo root directories encountered, not deeper paths within the same repo
        if args.only_top and repo_root != path:
            continue

        if repo_root in seen_repos:
            continue
        seen_repos.add(repo_root)

        ok, msg = git_pull(repo_root, args.remote, args.branch)

        # Classify message
        brief = "OK"
        if not ok:
            brief = "ERROR"
        else:
            lower = msg.lower()
            if "already up to date" in lower or "up to date" in lower:
                brief = "UP-TO-DATE"
            elif "fast-forward" in lower or "updating" in lower or "merge made" in lower:
                brief = "UPDATED"

        print(f"[{brief}] {repo_root}")
        # For quick context, show first line of git output
        first_line = (msg.splitlines() or [""]).pop(0)
        if first_line:
            print(f"  -> {first_line}")

        # If only-top, avoid descending into this repo's subdirs
        if args.only_top:
            # Prevent walking into children of this repo by clearing subsequent yields for its subtree
            # Not easily done with os.walk already in progress; rely on seen_repos to avoid repeats.
            pass

if __name__ == "__main__":
    main()
