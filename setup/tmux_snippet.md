# `tmux`

## Initiate a `tmux` session

```shell
tmux new -s cl_st1_melina
```

## Enable mouse support

```shell
tmux set -g mouse on
```

## Split horizontally

```text
Ctrl+B
"
```

## Split vertically

```text
Ctrl+B
%
```

## Detach from a `tmux` session
```text
Ctrl+B
D
```

## List the active sessions

```shell
tmux ls
```

## Attach to a `tmux` session

```shell
tmux attach -t cl_st1_melina
```

## Copy text in `tmux` using the mouse

### Linux

- Hold `Shift` while clicking and dragging the mouse, then press `Ctrl + Shift + c` to copy to your system clipboard.
