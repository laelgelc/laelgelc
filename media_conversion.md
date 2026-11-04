# Media Conversion

## `pandoc`

### Convert a `.docx` document into a Markdown document

```shell
pandoc input.docx -t markdown -o output.md
```

### Convert a Markdown document into a `.docx` document

```shell
pandoc input.md -o output.docx
```

### Convert a `.tex` document into a plain text document

The `-s` option (standalone mode) tells Pandoc to treat the input as a full document, not just a fragment.

```shell
pandoc -s <yourfile>.tex -o <cleaned_text>.txt
```

### Convert a `.md` document into a PDF document

#### Portrait orientation

```shell
pandoc <yourfile>.md -o <yourfile>.pdf \
    --pdf-engine=xelatex \
    -V papersize:a4paper \
    -V geometry:margin=2cm
```

#### Landscape orientation

```shell
pandoc <yourfile>.md -o <yourfile>.pdf \
    --pdf-engine=xelatex \
    -V papersize:a4paper \
    -V geometry:margin=2cm,landscape
```

## `ffmpeg`

### 

```shell
ffmpeg -i input.ogg output.mp3
```