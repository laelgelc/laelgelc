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

def walk_dirs(root: Path, max_depth: int):
    # Yield root first; then walk subdirs with depth control
    yield root
    if max_depth == 0:
        return
    for dirpath, dirnames, _ in os.walk(root):
        depth = Path(dirpath).relative_to(root).parts
        if len(depth) >= max_depth:
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
    # Default behavior: only act on directories that are git repos themselves
    parser.add_argument(
        "--no-only-top",
        dest="only_top",
        action="store_false",
        help="Allow traversing into subdirectories inside repositories (disables default only-top behavior)",
    )
    parser.set_defaults(only_top=True)
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print non-repo directories as [SKIP]",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    seen_repos = set()

    for path in walk_dirs(root, args.max_depth):
        # Optionally skip hidden dirs (except root itself)
        if args.skip_hidden and path != root and path.name.startswith("."):
            continue

        # Consider only the directory itself as a repo (do not walk up)
        if not is_git_repo(path):
            if args.verbose:
                print(f"[SKIP] {path} - not a git repository")
            continue

        repo_root = path
        if args.only_top:
            if repo_root in seen_repos:
                continue
            seen_repos.add(repo_root)

        ok, msg = git_pull(repo_root, args.remote, args.branch)

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
        first_line = (msg.splitlines() or [""])[0]
        if first_line:
            print(f"  -> {first_line}")

if __name__ == "__main__":
    main()
