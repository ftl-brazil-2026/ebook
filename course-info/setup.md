---
title: "Standard Set Up"
---

Verifique de seguir esse guia antes de começar a explorar o bootcamp. Aqui ajudamos a como fazer as configurações corretas do Python enviroment e reproduzir os resultados em seu próprio computador. 

## 1. Pré-requisitos

- **Git** — <https://git-scm.com/downloads>
- **uv** (Python package/version manager) — <https://docs.astral.sh/uv/getting-started/installation/>
- **VS Code** (recommended editor, with the Python + Jupyter extensions) — <https://code.visualstudio.com/download>
- **Quarto** — *(optional, only if you want to preview the site itself, not just run notebooks)* <https://quarto.org/docs/get-started/>
- **PostgreSQL + PostGIS** — *(optional, only needed once we start working with a spatial database)* 

::: {.callout-note appearance="simple"}
Lembre-se de usar `uv sync` para baixar as bibliotecas que utilizamos no decorrer de nossos encontros.
:::

## 2. Clone the repository

``` bash
git clone https://github.com/emanuel-gf/spacetech-gis-ebook.git
cd spacetech-gis-ebook
```

## 3. Create your own branch

Este repositório será atualizado semanalmente. Portanto, se você modificar os arquivos diretamente na `branch main`, você terá um pouco de problema/dificuldade para baixar os novos capítulos que serão disponibilizados (`git pull`). Dessa forma, sugerimos que você crie sua própria branch e altere seus arquivos nessa branch, deixando sempre a `main` limpa.

``` bash
git checkout -b semana0
```

**OU**

``` bash
git checkout -b qualquer-nome-aqui
```

Dessa forma, sempre que o repositório for atualizado, você só precisa ir na branch `main` e dar um `git pull`.

``` bash
git checkout main
git pull
git checkout my-work
git merge main
```

Isto deixará a `main` limpa e isolada, evitando possiveis dores de cabeça num futuro não muito distante. 

## 4. Sync as bibliotecas de python

Certifique-se de antes ter um ambiente uv, através do `uv venv` e de que esse ambiente esteja **Ativo**.

``` bash
uv sync
```

This reads `pyproject.toml` / `uv.lock` and creates a local `.venv` with the exact package versions used in class (geopandas, cartopy, plotly, etc).

## 5. Pronto! 

Agora você já pode rodar o notebook, clique nesse e selecione o kernel, tudo rodará feito magia. 


## 6. Re-construindo o website com quarto

Essa é para você que deseja explorar um pouco mais as funcionalidades do Quarto. Primeiro de uma lida na documentação. Depois, dentro do projeto, rode isso no terminal.

``` bash
uv run quarto preview
```

::: {.callout-warning appearance="simple"}

## "Jupyter is not available" / Quarto can't find your kernel

Quarto sometimes finds a system Python instead of the one `uv` just created in `.venv`. If `quarto check jupyter` reports no Jupyter, point Quarto at the venv explicitly:

``` bash
export QUARTO_PYTHON=$(pwd)/.venv/bin/python
quarto check jupyter
```

:::

::: {.callout-note appearance="simple"}

## Empacou meu querido?

Pergunta lá no nosso canal do discord. Algum colega com toda a certeza conseguirá te ajudar. Noiz.
:::


