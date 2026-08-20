![ftl-logo](assets/logos/Future_Tech_Leaders3-01.png)

# Future Tech Leaders Brasil 2026

Nossa pagina [Ebook page](https://ftl-brazil-2026.github.io/ebook/)


## Space Tech Bootcamp 

This repository host the ebook of the programme, with content and materials following the Remote Sensing and 
Geographic Information Systems curriculum proposed by United Nations Office for Outer Space Affair (UNOOSA) and adapted for the Brazil's reality.

The programme and bootcamp is executed by UNDP and SDG AI lab in partnership with Brazilian Space Agency (AEB) and United Nations.

This e-book is an open-source and crowd contribution dedicated to all our students of FTL Brasil intake 2026, and enthusiasts of the geospatial sector. 

Weekly updates will be added here to improve the quality of the material and align with our online sessions and meetings. 

## What is Future Tech Leaders?

FTL is a joint United Nations initiative by the UNDP Istanbul International Center for Private Sector in Development (ICPSD) and the UN Technology Bank to train young people in emerging technologies and close the digital divide in vulnerable regions. Primarily targets youth and university students, encouraging active participation and tech careers.


## Structure


Our ebook is based on [Quarto](https://quarto.org), where the materials are split into 3 big modules: Fundamentals of GIS and Remote Sensing, Fundamentals of Machine Learning and Deep Learning, and State-of-the-Art. Each module lives in its own top-level folder, with weekly content nested inside where that applies (currently only the GIS/RS module).

```text
ebook/
├── _quarto.yml                site config (sidebar navigation, theme, execute options)
├── index.qmd                  landing page
├── custom.scss                site theme overrides
├── pyproject.toml / uv.lock   Python dependencies (managed with uv)
│
├── assets/
│   └── logos/                 institutional / partner logos shown on the landing page
│
├── course-info/
│   ├── general-info.md
│   ├── reading.md
│   ├── setup.md
│   ├── cli-utils.md
│   └── how-to-contribute.md
│
├── fundamentals_gis_rs/        Módulo 1 — Fundamentos em GIS e Sensoriamento Remoto
│   ├── week0/
│   │   ├── index.qmd
│   │   ├── provedores.qmd            diagrama de bolhas: temas x provedores de dados
│   │   ├── space_tech_ecossystem.ipynb
│   │   └── data/                     xlsx/json/csv usados pelos notebooks da semana
│   ├── week1/
│   │   ├── index.qmd
│   │   ├── week1_introductionGIS.ipynb
│   │   └── images/
│   └── week2/ … week4/         index.md (conteúdo a ser adicionado)
│
├── ml-dl/                      Módulo 2 — Fundamentos em ML e Deep Learning (em construção)
├── state-of-art/               Módulo 3 — Estado da Arte (em construção)
├── guest-sessions/             Sessões de convidados (em construção)
├── awesome-geospatial/         lista de ferramentas do ecossistema, curada pelos alunos
│
└── .github/workflows/publish.yml   render + deploy automático pro GitHub Pages
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


![logos](assets/logos/union_logo.png)
