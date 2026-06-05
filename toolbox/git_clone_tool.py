#!/usr/bin/env python3
"""
git_clone_tool.py

Scan a source directory for Git repositories and generate a portable export
containing:

- clone_repositories.sh
- repositories.json
- README.md

The generated Bash script clones all repositories into the same relative
directory structure from the directory where the script is executed.

This tool intentionally does not migrate credentials, secrets, .env files,
SSH keys, service-account files, Git credential stores, or repository contents.
"""

from __future__ import annotations

import argparse
import datetime as _datetime
import fnmatch
import json
import os
import shutil
import stat
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any


EXIT_SUCCESS = 0
EXIT_GENERAL_FAILURE = 1
EXIT_INVALID_ARGUMENTS = 2
EXIT_SOURCE_DIRECTORY_ERROR = 3
EXIT_GIT_NOT_AVAILABLE = 4
EXIT_OUTPUT_EXISTS = 5


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="git_clone_tool.py",
        description=(
            "Scan a directory for Git repositories and generate a Bash script "
            "that clones them elsewhere while preserving relative paths."
        ),
    )

    parser.add_argument(
        "source_directory",
        help="Directory to scan recursively for Git repositories.",
    )

    parser.add_argument(
        "--output",
        default="git_clone_export",
        help="Output directory for the generated export package. Default: ./git_clone_export",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output directory if it already exists.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and report repositories without writing output files.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed diagnostic output.",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print warnings and errors.",
    )

    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help=(
            "Exclude paths matching a glob pattern relative to the source directory. "
            "May be supplied multiple times."
        ),
    )

    parser.add_argument(
        "--include-submodules",
        action="store_true",
        help="Include submodule metadata where possible.",
    )

    preference_group = parser.add_mutually_exclusive_group()
    preference_group.add_argument(
        "--prefer-https",
        action="store_true",
        help="Prefer HTTPS remote URLs when multiple suitable URLs are available.",
    )
    preference_group.add_argument(
        "--prefer-ssh",
        action="store_true",
        help="Prefer SSH remote URLs when multiple suitable URLs are available.",
    )

    args = parser.parse_args()

    if args.verbose and args.quiet:
        parser.error("--verbose and --quiet cannot be used together.")

    return args


def log(message: str, *, quiet: bool = False) -> None:
    """Print a normal status message unless quiet mode is enabled."""
    if not quiet:
        print(message)


def warn(message: str) -> None:
    """Print a warning message."""
    print(f"WARNING: {message}", file=sys.stderr)


def validate_environment() -> None:
    """Validate that Git is installed and available."""
    if shutil.which("git") is None:
        raise RuntimeError("Git executable was not found on PATH.")


def validate_source_directory(source_root: Path) -> None:
    """Validate that the source directory exists and is a directory."""
    if not source_root.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_root}")
    if not source_root.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_root}")


def prepare_output_directory(output_root: Path, *, force: bool) -> None:
    """Create or replace the output directory according to --force."""
    if output_root.exists():
        if not force:
            raise FileExistsError(
                f"Output directory already exists: {output_root}. "
                "Use --force to overwrite it."
            )
        if output_root.is_dir():
            shutil.rmtree(output_root)
        else:
            output_root.unlink()

    output_root.mkdir(parents=True, exist_ok=False)


def normalize_relative_path(path: Path) -> str:
    """Return a stable POSIX-style relative path string."""
    return path.as_posix()


def relative_to_source(path: Path, source_root: Path) -> str:
    """Return path relative to source_root as a POSIX-style string."""
    return normalize_relative_path(path.relative_to(source_root))


def is_git_repository(path: Path) -> bool:
    """Return True if path appears to be the root of a Git repository."""
    git_path = path / ".git"
    return git_path.is_dir() or git_path.is_file()


def is_excluded(path: Path, source_root: Path, patterns: list[str]) -> bool:
    """Return True if path matches any exclude pattern."""
    if not patterns:
        return False

    try:
        relative = relative_to_source(path, source_root)
    except ValueError:
        return False

    name = path.name

    for pattern in patterns:
        normalized = pattern.replace(os.sep, "/")
        if fnmatch.fnmatch(relative, normalized):
            return True
        if fnmatch.fnmatch(name, normalized):
            return True
        if relative.startswith(normalized.rstrip("/") + "/"):
            return True

    return False


def discover_repositories(
    source_root: Path,
    excludes: list[str],
    *,
    include_nested: bool = False,
    verbose: bool = False,
    quiet: bool = False,
) -> list[Path]:
    """
    Recursively find Git repositories below source_root.

    By default, once a repository root is found, the scanner does not descend
    further into it. This avoids scanning .git internals and speeds up discovery.
    """
    repositories: list[Path] = []

    def walk(directory: Path) -> None:
        if is_excluded(directory, source_root, excludes):
            if verbose:
                log(f"Excluded: {directory}", quiet=quiet)
            return

        if is_git_repository(directory):
            repositories.append(directory)
            if verbose:
                log(f"Found repository: {directory}", quiet=quiet)
            if not include_nested:
                return

        try:
            children = sorted(directory.iterdir(), key=lambda p: p.name.lower())
        except OSError as exc:
            warn(f"Could not read directory {directory}: {exc}")
            return

        for child in children:
            if not child.is_dir():
                continue
            if child.name == ".git":
                continue
            walk(child)

    walk(source_root)
    return sorted(repositories, key=lambda p: relative_to_source(p, source_root))


def run_git(repo_path: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a Git command in a repository and capture output."""
    return subprocess.run(
        ["git", "-C", str(repo_path), *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_stdout(repo_path: Path, args: list[str]) -> tuple[str | None, str | None]:
    """
    Run a Git command and return (stdout, warning).

    stdout is stripped. If the command fails, stdout is None and warning contains
    a readable error message.
    """
    result = run_git(repo_path, args)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        command = "git " + " ".join(args)
        return None, f"{command} failed: {stderr or 'unknown error'}"
    return result.stdout.strip(), None


def collect_remotes(repo_path: Path) -> tuple[list[dict[str, str | None]], list[str]]:
    """Collect fetch and push URLs for all remotes."""
    warnings: list[str] = []
    remotes_output, warning = git_stdout(repo_path, ["remote"])
    if warning:
        warnings.append(warning)
        return [], warnings

    remotes: list[dict[str, str | None]] = []
    remote_names = [line.strip() for line in remotes_output.splitlines() if line.strip()]

    for remote_name in remote_names:
        fetch_url, fetch_warning = git_stdout(repo_path, ["remote", "get-url", remote_name])
        push_url, push_warning = git_stdout(
            repo_path,
            ["remote", "get-url", "--push", remote_name],
        )

        if fetch_warning:
            warnings.append(f"Could not read fetch URL for remote {remote_name}: {fetch_warning}")
        if push_warning:
            push_url = None

        remotes.append(
            {
                "name": remote_name,
                "fetch_url": fetch_url,
                "push_url": push_url,
            }
        )

    return remotes, warnings


def is_https_url(url: str) -> bool:
    """Return True if URL appears to be HTTPS."""
    return url.startswith("https://")


def is_ssh_url(url: str) -> bool:
    """Return True if URL appears to be SSH-style."""
    return url.startswith("ssh://") or (
        "@" in url
        and ":" in url
        and not url.startswith("http://")
        and not url.startswith("https://")
    )


def score_url(url: str, *, prefer_ssh: bool, prefer_https: bool) -> int:
    """Score a remote URL according to user preference."""
    if prefer_ssh and is_ssh_url(url):
        return 2
    if prefer_https and is_https_url(url):
        return 2
    if is_ssh_url(url) or is_https_url(url):
        return 1
    return 0


def select_clone_url(
    remotes: list[dict[str, str | None]],
    *,
    prefer_ssh: bool = True,
    prefer_https: bool = False,
) -> str | None:
    """
    Select the best remote URL for cloning.

    Default priority:
    1. origin fetch URL
    2. origin push URL
    3. first available fetch URL from any remote
    4. first available push URL from any remote

    If URL preference is requested, it is applied within available candidates.
    """
    candidates: list[tuple[int, str]] = []

    for remote in remotes:
        if remote.get("name") == "origin" and remote.get("fetch_url"):
            candidates.append((100, str(remote["fetch_url"])))
        if remote.get("name") == "origin" and remote.get("push_url"):
            candidates.append((90, str(remote["push_url"])))

    for remote in remotes:
        if remote.get("fetch_url"):
            candidates.append((50, str(remote["fetch_url"])))

    for remote in remotes:
        if remote.get("push_url"):
            candidates.append((40, str(remote["push_url"])))

    if not candidates:
        return None

    scored = [
        (base_score + score_url(url, prefer_ssh=prefer_ssh, prefer_https=prefer_https), url)
        for base_score, url in candidates
    ]

    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[0][1]


def collect_status(repo_path: Path) -> tuple[bool | None, bool | None, list[str]]:
    """Collect dirty and untracked status for a repository."""
    warnings: list[str] = []

    output, warning = git_stdout(repo_path, ["status", "--porcelain"])
    if warning:
        warnings.append(warning)
        return None, None, warnings

    lines = output.splitlines()
    dirty = any(line and not line.startswith("??") for line in lines)
    has_untracked_files = any(line.startswith("??") for line in lines)

    return dirty, has_untracked_files, warnings


def collect_submodules(repo_path: Path) -> tuple[list[dict[str, str]], list[str]]:
    """Collect submodule metadata where possible."""
    warnings: list[str] = []
    output, warning = git_stdout(repo_path, ["submodule", "status", "--recursive"])
    if warning:
        return [], warnings

    submodules: list[dict[str, str]] = []
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        parts = stripped.split()
        if len(parts) >= 2:
            commit = parts[0].lstrip("-+U")
            path = parts[1]
            submodules.append({"path": path, "commit": commit})

    return submodules, warnings


def collect_repository_metadata(
    repo_path: Path,
    source_root: Path,
    *,
    include_submodules: bool = False,
    prefer_ssh: bool = True,
    prefer_https: bool = False,
) -> dict[str, Any]:
    """Collect metadata for a single repository."""
    warnings: list[str] = []

    relative_path = relative_to_source(repo_path, source_root)

    branch, warning = git_stdout(repo_path, ["branch", "--show-current"])
    if warning:
        warnings.append(warning)
        branch = None
    if branch == "":
        branch = None
        warnings.append("Repository appears to be in detached HEAD state.")

    head_commit, warning = git_stdout(repo_path, ["rev-parse", "HEAD"])
    if warning:
        warnings.append(warning)
        head_commit = None

    remotes, remote_warnings = collect_remotes(repo_path)
    warnings.extend(remote_warnings)

    selected_clone_url = select_clone_url(
        remotes,
        prefer_ssh=prefer_ssh,
        prefer_https=prefer_https,
    )

    if selected_clone_url is None:
        warnings.append("No remote URL found; repository will not be included in clone script.")

    dirty, has_untracked_files, status_warnings = collect_status(repo_path)
    warnings.extend(status_warnings)

    metadata: dict[str, Any] = {
        "name": repo_path.name,
        "absolute_path": str(repo_path),
        "relative_path": relative_path,
        "current_branch": branch,
        "head_commit": head_commit,
        "dirty": dirty,
        "has_untracked_files": has_untracked_files,
        "remotes": remotes,
        "selected_clone_url": selected_clone_url,
        "warnings": warnings,
    }

    if include_submodules:
        submodules, submodule_warnings = collect_submodules(repo_path)
        metadata["submodules"] = submodules
        warnings.extend(submodule_warnings)

    return metadata


def utc_now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return _datetime.datetime.now(_datetime.timezone.utc).replace(microsecond=0).isoformat()


def build_metadata(
    repositories: list[Path],
    source_root: Path,
    *,
    include_submodules: bool,
    prefer_ssh: bool,
    prefer_https: bool,
    verbose: bool,
    quiet: bool,
) -> dict[str, Any]:
    """Build complete export metadata."""
    repo_metadata: list[dict[str, Any]] = []
    warnings: list[str] = []

    for repo_path in repositories:
        if verbose:
            log(f"Collecting metadata: {repo_path}", quiet=quiet)

        try:
            repo_metadata.append(
                collect_repository_metadata(
                    repo_path,
                    source_root,
                    include_submodules=include_submodules,
                    prefer_ssh=prefer_ssh,
                    prefer_https=prefer_https,
                )
            )
        except Exception as exc:
            relative_path = relative_to_source(repo_path, source_root)
            message = f"Failed to collect metadata for {relative_path}: {exc}"
            warnings.append(message)
            warn(message)

    repo_metadata.sort(key=lambda item: item["relative_path"])

    return {
        "version": 1,
        "created_at": utc_now_iso(),
        "source_root": str(source_root),
        "repositories": repo_metadata,
        "warnings": warnings,
    }


def shell_single_quote(value: str) -> str:
    """
    Safely single-quote a value for Bash.

    Example:
        abc'def -> 'abc'"'"'def'
    """
    return "'" + value.replace("'", "'\"'\"'") + "'"


def write_repositories_json(metadata: dict[str, Any], output_root: Path) -> None:
    """Write repository metadata to repositories.json."""
    output_path = output_root / "repositories.json"
    output_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_clone_script(metadata: dict[str, Any], output_root: Path) -> None:
    """Generate clone_repositories.sh."""
    output_path = output_root / "clone_repositories.sh"

    lines: list[str] = [
        "#!/usr/bin/env bash",
        "set -u",
        "",
        "FAILED=0",
        "",
        "clone_repo() {",
        "    local url=\"$1\"",
        "    local target=\"$2\"",
        "    local branch=\"$3\"",
        "",
        "    echo \"Cloning ${url} into ${target}\"",
        "",
        "    if [ -d \"${target}/.git\" ] || [ -f \"${target}/.git\" ]; then",
        "        echo \"Repository already exists, skipping: ${target}\"",
        "        return 0",
        "    fi",
        "",
        "    mkdir -p \"$(dirname \"${target}\")\"",
        "",
        "    if [ -n \"${branch}\" ]; then",
        "        git clone --branch \"${branch}\" \"${url}\" \"${target}\" || {",
        "            echo \"Failed to clone ${url}\" >&2",
        "            FAILED=1",
        "            return 1",
        "        }",
        "    else",
        "        git clone \"${url}\" \"${target}\" || {",
        "            echo \"Failed to clone ${url}\" >&2",
        "            FAILED=1",
        "            return 1",
        "        }",
        "    fi",
        "}",
        "",
        "echo \"Starting repository clone operation\"",
        "echo \"Repositories will be cloned relative to: $(pwd)\"",
        "",
    ]

    for repo in metadata["repositories"]:
        relative_path = repo["relative_path"]
        clone_url = repo.get("selected_clone_url")
        branch = repo.get("current_branch") or ""

        if not clone_url:
            lines.append(
                f"# WARNING: No remote URL found for local-only repository: {relative_path}"
            )
            lines.append("")
            continue

        lines.append(
            "clone_repo "
            f"{shell_single_quote(str(clone_url))} "
            f"{shell_single_quote(str(relative_path))} "
            f"{shell_single_quote(str(branch))}"
        )
        lines.append("")

    lines.extend(
        [
            "if [ \"${FAILED}\" -ne 0 ]; then",
            "    echo \"One or more repositories failed to clone.\" >&2",
            "else",
            "    echo \"All clone operations completed successfully.\"",
            "fi",
            "",
            "exit \"${FAILED}\"",
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    output_path.chmod(output_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def write_readme(metadata: dict[str, Any], output_root: Path) -> None:
    """Write README.md for the export package."""
    repo_count = len(metadata["repositories"])
    cloneable_count = sum(1 for repo in metadata["repositories"] if repo.get("selected_clone_url"))
    uncloneable_count = repo_count - cloneable_count

    content = f"""\
# Git Clone Export

This directory was generated by `git_clone_tool.py`.

It contains a Bash script and repository metadata for cloning discovered Git
repositories into the same relative directory structure on another machine.

## Contents

```text
clone_repositories.sh
repositories.json
README.md
```

## Summary

- Source root: `{metadata["source_root"]}`
- Created at: `{metadata["created_at"]}`
- Repositories found: `{repo_count}`
- Repositories with clone URLs: `{cloneable_count}`
- Repositories without clone URLs: `{uncloneable_count}`

## Restore repositories

Copy this export directory to the destination machine, then run:

```bash
bash clone_repositories.sh
```

The repositories will be cloned into the directory from which the script is
executed.

For example:

```bash
mkdir -p ~/restored-projects
cd ~/restored-projects
bash /path/to/git_clone_export/clone_repositories.sh
```

## Authentication

Credentials are not included.

This export does not contain `.env` files, SSH keys, service-account JSON files,
Git credential stores, global Git configuration, cloud credentials, API tokens,
or passwords.

Before running the clone script, make sure the destination machine already has
access to the repositories, for example through SSH keys, HTTPS authentication,
Git Credential Manager, or another authentication method.

## Repositories without remotes

Repositories that did not have a usable remote URL are recorded in
`repositories.json`, but they are not cloned by `clone_repositories.sh`.

## Notes

- Existing repositories are skipped.
- If one clone fails, the script continues with the remaining repositories.
- The script exits with a non-zero status if any repository fails.
- Paths are quoted to support spaces and common shell-special characters.
"""
    output_path = output_root / "README.md"
    output_path.write_text(textwrap.dedent(content), encoding="utf-8")


def write_output_files(metadata: dict[str, Any], output_root: Path) -> None:
    """Write all output files."""
    write_repositories_json(metadata, output_root)
    write_clone_script(metadata, output_root)
    write_readme(metadata, output_root)


def print_dry_run(metadata: dict[str, Any]) -> None:
    """Print dry-run repository report."""
    print(json.dumps(metadata, indent=2, sort_keys=True))


def main() -> int:
    """Programme entry point."""
    try:
        args = parse_args()
    except SystemExit as exc:
        return int(exc.code)

    source_root = Path(args.source_directory).expanduser().resolve()
    output_root = Path(args.output).expanduser().resolve()

    prefer_https = bool(args.prefer_https)
    prefer_ssh = bool(args.prefer_ssh or not args.prefer_https)

    try:
        validate_environment()
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return EXIT_GIT_NOT_AVAILABLE

    try:
        validate_source_directory(source_root)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return EXIT_SOURCE_DIRECTORY_ERROR

    log(f"Scanning {source_root}", quiet=args.quiet)

    repositories = discover_repositories(
        source_root,
        args.exclude,
        include_nested=args.include_submodules,
        verbose=args.verbose,
        quiet=args.quiet,
    )

    log(f"Found {len(repositories)} Git repositories", quiet=args.quiet)

    metadata = build_metadata(
        repositories,
        source_root,
        include_submodules=args.include_submodules,
        prefer_ssh=prefer_ssh,
        prefer_https=prefer_https,
        verbose=args.verbose,
        quiet=args.quiet,
    )

    if args.dry_run:
        print_dry_run(metadata)
        return EXIT_SUCCESS

    try:
        prepare_output_directory(output_root, force=args.force)
    except FileExistsError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return EXIT_OUTPUT_EXISTS
    except OSError as exc:
        print(f"Error: Could not prepare output directory {output_root}: {exc}", file=sys.stderr)
        return EXIT_GENERAL_FAILURE

    try:
        log(f"Writing export to {output_root}", quiet=args.quiet)
        write_output_files(metadata, output_root)
    except OSError as exc:
        print(f"Error: Could not write output files: {exc}", file=sys.stderr)
        return EXIT_GENERAL_FAILURE

    log("Done", quiet=args.quiet)
    log("", quiet=args.quiet)
    log("Next steps:", quiet=args.quiet)
    log(f"  cd {shell_single_quote(str(output_root))}", quiet=args.quiet)
    log("  bash clone_repositories.sh", quiet=args.quiet)

    if metadata.get("warnings"):
        warn(f"{len(metadata['warnings'])} warning(s) recorded in repositories.json")

    return EXIT_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())