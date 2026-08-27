---
name: qmd-notebook-convert
description: Convert this book's Quarto .qmd files to .ipynb and back, cell-for-cell, without breaking Quarto structure or nbformat compliance. Use whenever asked to generate/sync a notebook from a .qmd, or turn a notebook back into a .qmd.
---

# qmd ⇄ ipynb conversion

Convert 1:1, never summarize or "clean up" content. If the user says "exact content," the diff against the source must show only format changes.

## Cell splitting (qmd → ipynb)

- A ```` ```{python} ... ``` ```` fence becomes one **code** cell. Its body — including every `#| ` option line (`label`, `fig-cap`, `include`, etc.) — goes verbatim into `source`. Never strip or move `#|` lines out of the code cell.
- Everything between fences (prose, `##` headings, `:::` callout/div blocks, images, lists) becomes **markdown** cells. Don't split one markdown block into several unless a code fence interrupts it — match the qmd's actual paragraph/blank-line breaks.
- YAML frontmatter (`title`, `subtitle`, `author`, `date`) becomes a single leading markdown cell:
  ```
  # {title}
  ### {subtitle}

  *{author} — {date}*
  ```
  Keep `date: today` as the literal word "today" — do not resolve it to a real date.
- Two code fences back-to-back with no prose between them → two separate code cells, no markdown cell inserted between.

## nbformat compliance — build it right the first time

Never hand-roll cell dicts + `json.dump`. That skips id assignment and produces `MissingIDFieldWarning`. Instead:

```python
import nbformat as nbf

nb = nbf.v4.new_notebook()
nb.cells.append(nbf.v4.new_markdown_cell(md_source))
nb.cells.append(nbf.v4.new_code_cell(code_source))
...
nbf.validate(nb)   # must pass with zero warnings before writing
nbf.write(nb, out_path)
```

If a notebook is already built as raw dicts, run `nbf.from_dict(...)` then `nbf.validate(nb, repair_duplicate_cell_ids=True)`, or assign `cell.id = uuid.uuid4().hex[:8]` yourself — every cell needs a unique id, no exceptions.

`metadata.kernelspec` / `metadata.language_info`: copy from another notebook already in the same folder (e.g. `AUX_week1.ipynb`). Don't invent a kernel name or Python version.

## Reverse direction (ipynb → qmd)

- Rebuild the YAML header from the first markdown cell's `#`/`###`/italic-author line; drop that cell from the body.
- Each code cell → ```` ```{python}\n{source}\n``` ````, keeping `#|` option lines exactly where they are in `source`.
- Each markdown cell → pasted as-is, one blank line before and after.
- Strip nothing Quarto-specific: `:::` divs, `{fig-align=...}` attrs, `#| label`/`#| fig-cap`, cross-refs (`@fig-...`) must all survive unchanged.

## Compliance checklist before handing back a file

- [ ] `nbformat.validate()` (or equivalent) passes with no warnings
- [ ] Every cell has a unique `id`
- [ ] No `#|` option line moved, dropped, or turned into a comment inside markdown
- [ ] No callout `:::` block split across cells
- [ ] Round-tripping qmd → ipynb → qmd reproduces the original qmd byte-for-byte (modulo the YAML-header cell transform)
