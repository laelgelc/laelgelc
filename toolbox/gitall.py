#!/usr/bin/env python3
"""
gitall.py

A CLI tool for managing Git repositories under the directory it is located in.

Usage:
    python gitall.py status
    python gitall.py pull
    python gitall.py commit

Behaviour:
- Repository discovery:
  * Starting from the directory where this script resides, recursively finds
    Git repositories (directories containing a `.git` directory).
  * Assumes there are no nested repositories: once a Git repository is found
    at a directory, subdirectories under it are not scanned for further repos.

- status:
  * Runs `git status -sb` in each discovered repository.
  * Prints the status output.
  * Classifies repositories as "clean" or "dirty" based on whether there are
    uncommitted changes (using `git status --porcelain`).
  * Prints a summary of clean vs dirty repositories at the end.
  * Logs all operations to stdout.

- pull:
  * Runs `git pull` in each discovered repository.
  * Logs success/failure and relevant messages to stdout.

- commit:
  * Runs `git add -A` in each discovered repository.
  * If there are changes (dirty repo), commits them with a message of the form
    `gitall_yyyymmdd-hhmm`, using the current local time.
  * Attempts to push the current branch:
      - If no upstream is set for the current branch, it skips the push and
        logs a warning.
      - If the push fails (e.g., non-fast-forward), it logs the failure and
        continues with the next repository.
  * Logs all operations to stdout.
"""

import argparse
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Tuple


def is_git_repo(path: Path) -> bool:
    """Return True if the given path is the root of a Git repository."""
    return (path / ".git").is_dir()


def discover_repos(base_dir: Path) -> List[Path]:
    """
    Recursively discover Git repositories under base_dir.

    Assumes there are no nested repositories: once a directory is identified
    as a Git repo, its subdirectories will not be traversed.
    """
    repos: List[Path] = []

    for dirpath, dirnames, _ in os.walk(base_dir):
        current = Path(dirpath)
        if is_git_repo(current):
            repos.append(current)
            # Do not descend into subdirectories of this repo
            dirnames[:] = []
        # Otherwise, continue walking as normal

    return sorted(repos)


def run_git_command(repo: Path, args: Iterable[str], timeout: int = 300) -> Tuple[bool, str]:
    """
    Run a git command in the given repository.

    Returns (success, combined_output).
    """
    cmd = ["git", "-C", str(repo), *args]
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
        )
        out = (result.stdout or "") + (("\n" + result.stderr) if result.stderr else "")
        return result.returncode == 0, out.strip()
    except subprocess.TimeoutExpired:
        return False, "Timed out"
    except FileNotFoundError:
        return False, "git not found"


def repo_is_dirty(repo: Path) -> Tuple[bool, str]:
    """
    Determine if the repository has uncommitted changes.

    Uses `git status --porcelain`, which prints nothing when the working tree
    and index are clean.
    """
    ok, out = run_git_command(repo, ["status", "--porcelain"])
    if not ok:
        # Treat failure to get status as "dirty" and propagate the message
        return True, out
    is_dirty = bool(out.strip())
    return is_dirty, out


def cmd_status(repos: List[Path]) -> None:
    """Execute the 'status' command on all repositories."""
    clean_count = 0
    dirty_count = 0
    dirty_repos: List[Path] = []

    if not repos:
        print("No Git repositories found.")
        return

    for repo in repos:
        print(f"\n=== [STATUS] {repo} ===")

        # Display status with -sb as specified
        ok, status_output = run_git_command(repo, ["status", "-sb"])
        if not ok:
            print("[ERROR] Failed to run 'git status -sb'")
            if status_output:
                print(status_output)
        else:
            print(status_output)

        # Determine clean vs dirty using porcelain
        is_dirty, porcelain_output = repo_is_dirty(repo)
        if not is_dirty and porcelain_output.strip() == "":
            print("[INFO] Repository is clean.")
            clean_count += 1
        else:
            print("[INFO] Repository has uncommitted changes.")
            dirty_count += 1
            dirty_repos.append(repo)

    # Summary
    print("\n=== Summary ===")
    print(f"Clean repositories: {clean_count}")
    print(f"Dirty repositories: {dirty_count}")
    if dirty_repos:
        print("Dirty repository paths:")
        for repo in dirty_repos:
            print(f"  - {repo}")


def cmd_pull(repos: List[Path]) -> None:
    """Execute the 'pull' command on all repositories."""
    if not repos:
        print("No Git repositories found.")
        return

    for repo in repos:
        print(f"\n=== [PULL] {repo} ===")
        ok, out = run_git_command(repo, ["pull"])
        if ok:
            print("[OK] git pull succeeded.")
        else:
            print("[ERROR] git pull failed.")
        if out:
            print(out)


def cmd_commit(repos: List[Path]) -> None:
    """Execute the 'commit' command on all repositories."""
    if not repos:
        print("No Git repositories found.")
        return

    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    commit_message = f"gitall_{timestamp}"

    for repo in repos:
        print(f"\n=== [COMMIT] {repo} ===")

        # Stage everything
        print("[INFO] Running 'git add -A'...")
        ok, out = run_git_command(repo, ["add", "-A"])
        if not ok:
            print("[ERROR] 'git add -A' failed; skipping this repository.")
            if out:
                print(out)
            continue

        # Check for changes after staging
        is_dirty, porcelain_output = repo_is_dirty(repo)
        if not is_dirty and porcelain_output.strip() == "":
            print("[INFO] No changes to commit; skipping commit and push.")
            continue

        # Commit changes
        print(f"[INFO] Committing with message '{commit_message}'...")
        ok, out = run_git_command(repo, ["commit", "-m", commit_message])
        if not ok:
            print("[ERROR] 'git commit' failed; skipping push for this repository.")
            if out:
                print(out)
            continue
        else:
            print("[OK] Commit created.")
            if out:
                print(out)

        # Determine current branch
        ok, branch = run_git_command(repo, ["rev-parse", "--abbrev-ref", "HEAD"])
        if not ok or not branch:
            print("[WARN] Unable to determine current branch; skipping push.")
            if branch:
                print(branch)
            continue
        branch = branch.strip()
        if branch == "HEAD":
            print("[WARN] Detached HEAD state; skipping push.")
            continue

        # Check for upstream (tracking) branch
        ok, upstream = run_git_command(
            repo, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]
        )
        if not ok or not upstream:
            print(
                f"[WARN] No upstream set for branch '{branch}'; "
                "skipping push for this repository."
            )
            if upstream:
                print(upstream)
            continue

        upstream = upstream.strip()
        print(f"[INFO] Pushing branch '{branch}' to '{upstream}'...")
        ok, out = run_git_command(repo, ["push"])
        if ok:
            print("[OK] Push succeeded.")
        else:
            print("[ERROR] Push failed.")
        if out:
            print(out)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Manage all Git repositories under the directory where this script is located."
    )
    parser.add_argument(
        "command",
        choices=["status", "pull", "commit"],
        help="Operation to perform on all discovered repositories.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Base directory: directory where this script resides
    base_dir = Path(__file__).resolve().parent
    print(f"[INFO] Discovering Git repositories under: {base_dir}")
    repos = discover_repos(base_dir)
    print(f"[INFO] Found {len(repos)} repository(ies).")

    if args.command == "status":
        cmd_status(repos)
    elif args.command == "pull":
        cmd_pull(repos)
    elif args.command == "commit":
        cmd_commit(repos)
    else:
        # This should never happen due to argparse choices
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()