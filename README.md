![ftl-logo](assets/logos/Future_Tech_Leaders3-01.png)

# Future Tech Leaders Brasil 2026

## Space Tech Bootcamp 

This repository host the ebook of the programme, with content and materials following the Remote Sensing and 
Geographic Information Systems curriculum proposed by United Nations Office for Outer Space Affair (UNOOSA) and adapted for the Brazil's reality.

The programme and bootcamp is executed by UNDP and SDG AI lab in partnership with Brazilian Space Agency (AEB) and United Nations.

This e-book is an open-source and crowd contribution dedicated to all our students of FTL Brasil intake 2026, and enthusiasts of the geospatial sector. 

Weekly updates will be added here to improve the quality of the material and align with our online sessions and meetings. 

## What is Future Tech Leaders?

FTL is a joint United Nations initiative by the UNDP Istanbul International Center for Private Sector in Development (ICPSD) and the UN Technology Bank to train young people in emerging technologies and close the digital divide in vulnerable regions. Primarily targets youth and university students, encouraging active participation and tech careers.


## Structure


Our ebook is based on [Quarto](https://quarto.org), where the materials are splited into 3 big modules: Fundamentals of GIS and Remote Sensing. Fundamentals of Machine-Learning and Deep-Learning and State-of-Art. 

```text
_quarto.yml           site config (sidebar navigation, theme, execute options)
index.qmd             landing page
assets/logos/         institutional / partner logos shown on the landing page
course-info/          general-info.md, reading.md, setup.md
week1/ … week4/       one folder per week
pyproject.toml        Python dependencies (managed with uv)
```

## Getting Started

Please read our [course-info/setup.md](course-info/setup.md) page for a more detailed explanation in how to set up the environment in your own computer

### Local development

```bash
uv sync                # install the exact Python env (geopandas, cartopy, plotly, ...)
uv run quarto preview  # live-reload preview of the full site
```

If Quarto can't find Jupyter (it sometimes picks up a system Python instead of `.venv`), see the troubleshooting note in [course-info/setup.md](course-info/setup.md).


## Contributions

We have a page dedicated to whom is willing of contributing into our repo. Please read [contributions](course-info/how-to-contribute.md)


![logos](/assets/logos/union_logo.png)
