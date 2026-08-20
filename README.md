# SpaceTech Bootcamp — GIS Ebook

Source for the GIS module course ebook, built with [Quarto](https://quarto.org). Published at:

**<https://emanuel-gf.github.io/spacetech-gis-ebook/>**

## Structure

```text
_quarto.yml           site config (sidebar navigation, theme, execute options)
index.qmd             landing page
assets/logos/         institutional / partner logos shown on the landing page
course-info/          general-info.md, reading.md, setup.md
week1/ … week4/       one folder per week
pyproject.toml        Python dependencies (managed with uv)
```

### Adding material to a week

Drop a file into `weekN/` and add it to that week's `contents:` list in `_quarto.yml`:

- **Narrative page** — a `.md` or `.qmd` file.
- **Hands-on notebook** — a `.ipynb` file. It renders as a page and stays downloadable as-is.
- **Slides** — a `.qmd` file with `format: revealjs` in its own front matter (this overrides the site's default HTML format for that page only — don't add `revealjs` to the site-wide `format:` key or every plain page will try to render twice).

## Local development

```bash
uv sync                # install the exact Python env (geopandas, cartopy, plotly, ...)
uv run quarto preview  # live-reload preview of the full site
```

If Quarto can't find Jupyter (it sometimes picks up a system Python instead of `.venv`), see the troubleshooting note in [course-info/setup.md](course-info/setup.md).

## Deployment

A GitHub Actions workflow (`.github/workflows/publish.yml`) renders the site and publishes it to the `gh-pages` branch on every push to `main`. No manual render/commit step is needed — just push source files.

## For students

See the **Course Information → Standard Set Up** page on the site for clone/setup instructions.
