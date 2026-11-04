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

## PDF to PPTX manually with `PowerPoint for the Web` or `LibreOffice`

### Convert the PDF pages

```shell
pdftoppm -png presentation.pdf slide
```

This produces:

```shell
slide-1.png
slide-2.png
slide-3.png
...
```

Then create a presentation with `PowerPoint for the Web` or `LibreOffice` where each image becomes a slide.

The resulting `.pptx` is visually faithful but not editable.
