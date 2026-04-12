# `gitall.py` CLI tool specifications

## Description

A CLI tool for managing Git repositories under the directory it is located in.

## Usage

  python gitall.py status
  python gitall.py pull
  python gitall.py commit

### Docstring

A docstring should be added to the top of the programme explaining what the program does and how it should be used.

## Repository discovery

Finds Git repositories under the directory the programme is located in assuming there are no nested repositories in them.

## Commands

status:
- Displays the status of the repositories with `git status -sb`.
- Summarises clean versus dirty repositories at the end.
- Logs operations to stdout.

pull:
- Pulls all repositories with `git pull`.
- Logs operations to stdout.

commit:
- Stages with `git add -A` in all repositories.
- Commits with the message 'gitall_yyyymmdd-hhmm', with current local time, when there are changes.
- Pushes the current branch:
  - If a repository has no upstream set for the current branch, it should skip push with a warning
  - If push fails (e.g., non-fast-forward), it should log the failure and continue with the next repository
- Logs operations to stdout.
