# `branch` and `rebase`

## Branch best common ancestor

> 
> User:
> 
> In `git`, how do I know from which commit a branch was created?

AI Assistant:

In Git, a branch does **not permanently record “the commit it was created from.”** A branch is just a movable pointer to a commit. Once commits are added or history changes, Git may not know the exact original creation point.

That said, you can usually infer it.

### Most common answer: find the merge base

If you want to know where `feature/promax_pattern` diverged from `main`:

```shell script
git merge-base main feature/promax_pattern
```

This prints the (full) commit hash of the best common ancestor.

```shell script
git merge-base main feature/promax_pattern
b6596e0a32f59570019cea581a7aede82c8c8d93
```

You can get more information with:

```shell script
git log --oneline -1 b6596e0a32f59570019cea581a7aede82c8c8d93
b6596e0a (HEAD -> feature/promax_pattern, origin/main, origin/feature/promax_pattern, origin/HEAD, main) gitall_20260901-1111
```

This means that **both `main` and `feature/promax_pattern` currently point to the same commit**.

So right now:

- `main` is at `b6596e0a`
- `feature/promax_pattern` is also at `b6596e0a`
- `origin/main` is also at `b6596e0a`
- `origin/feature/promax_pattern` is also at `b6596e0a`

In other words, your feature branch currently has **no commits ahead of `main`**. It is at the same commit as `main`.

### Important caveat

`git merge-base` gives the **common ancestor**, not necessarily a formally recorded “branch creation commit.” In normal workflows, that is what people mean by “where the branch was created from,” but it can be misleading if:

- the branch was rebased;
- history was rewritten;
- the branch was created from another feature branch;
- commits were cherry-picked;
- the original reflog entry expired or exists only on another machine.

### Searching for it in GitHub

Put it in the GitHub repository URL

```plain text
https://github.com/laelgelc/cl_st1_sara/commit/b6596e0a32f59570019cea581a7aede82c8c8d93
```

## `rebase`

> User:
> What is `rebase`?

AI Assistant:

`git rebase` means:

> **Take the commits from one branch and replay them on top of another commit or branch.**

It is a way of moving the base of your branch.

That is why it is called **re-base**.

---

### Simple picture

Suppose you created a feature branch from `main`.

```plain text
A---B---C  main
     \
      D---E  feature
```

Here:

- `main` has commits `A`, `B`, `C`
- `feature` started from `B`
- `feature` has commits `D`, `E`

Now suppose you are on `feature` and run:

```shell script
git rebase main
```

Git will take your feature commits `D` and `E`, temporarily remove them, move your branch to the latest `main`, then replay those commits there:

```plain text
A---B---C  main
         \
          D'---E'  feature
```

Notice the primes: `D'` and `E'`.

They are not literally the same commits anymore. They are **new commits** with new commit hashes, because their parent changed.

---

### What problem does rebase solve?

It lets you update your branch with the latest changes from `main` while keeping the history linear.

Instead of this:

```plain text
A---B---C-------M  feature
     \         /
      D---E---F
```

You get this:

```plain text
A---B---C---D'---E'---F'  feature
```

That can make history easier to read.

---

### Rebase versus merge

There are two common ways to bring `main` into your branch.

#### Option 1: merge

```shell script
git switch feature
git merge main
```

This preserves the exact history and creates a merge commit if needed.

```plain text
A---B---C  main
     \   \
      D---E---M  feature
```

Meaning:

> “Feature branch incorporated main at this point.”

#### Option 2: rebase

```shell script
git switch feature
git rebase main
```

This rewrites your feature branch so it looks as if it started from the latest `main`.

```plain text
A---B---C  main
         \
          D'---E'  feature
```

Meaning:

> “Pretend I created this feature branch from the current tip of main.”

---

### Important: rebase rewrites history

Because rebase creates new commits, the commit hashes change.

Before rebase:

```plain text
D---E
```

After rebase:

```plain text
D'---E'
```

Same changes, but new commits.

This is why people say:

> **Do not rebase public/shared commits unless you know what you are doing.**

If you already pushed your branch and others are using it, rebasing can confuse their copies of the repository.

---

### Safe rule of thumb

Usually safe:

```shell script
git rebase main
```

on your own local feature branch that only you use.

Be careful:

```shell script
git rebase main
git push --force
```

on a branch that other people also use.

---

### Typical use case

You are working on a feature branch:

```shell script
git switch feature/promax_pattern
```

Meanwhile, `main` has moved forward. You want your branch to be based on the latest `main`.

You can do:

```shell script
git fetch origin
git rebase origin/main
```

This says:

> “Take my current branch’s commits and replay them on top of the latest `origin/main`.”

---

### What happens if there are conflicts?

During a rebase, Git may stop and say there is a conflict.

Then the flow is usually:

```shell script
# fix the conflicted files

git add conflicted-file
git rebase --continue
```

If you want to cancel the whole rebase:

```shell script
git rebase --abort
```

That returns you to where you were before the rebase started.

---

### A more intuitive analogy

Imagine `main` is a document:

```plain text
main:    version 1 -> version 2 -> version 3
```

You copied version 2 and wrote two edits:

```plain text
your branch: version 2 -> your edit 1 -> your edit 2
```

Then `main` got version 3.

Rebase means:

> “Take my edits and apply them again, but this time starting from version 3 instead of version 2.”

So your branch becomes:

```plain text
main version 3 -> your edit 1 -> your edit 2
```

---

### In short

`rebase` means:

> Move my branch so that my commits sit on top of another branch.

Or even shorter:

```plain text
rebase = replay my commits on a new base
```

It is powerful, but because it rewrites commit history, it should be used carefully.