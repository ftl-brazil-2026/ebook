---
title: "Awesome Brasil Geoespatial Ecosystem"
---

Uma lista curada de ferramentas, dados e bibliotecas do ecossistema geoespacial, organizada por categoria. Cresce aos poucos ao longo do bootcamp — qualquer aluno pode contribuir.

::: {.callout-note appearance="simple"}

## Formato de cada item

``` markdown
- [**Nome**](https://link.com) — descrição curta do que é / para que serve.
```

Só adicione `⚠️ *verificar*` no fim da linha se o link ou a descrição ainda precisam ser conferidos por alguém — sem a marcação, o item é considerado confiável. Passo a passo completo em [Como Contribuir](../course-info/how-to-contribute.md).
:::

## Dados Geoespaciais Brasileiros

### Censitário / Demografia / Socioeconômico

- [**GeoBR**](https://github.com/ipeaGIT/geobr) — dados espaciais oficiais do Brasil (malhas municipais/estaduais, setores censitários, biomas etc.), disponível em R e Python.
- [**ipeaData**](https://www.ipeadata.gov.br/) — séries históricas macroeconômicas, financeiras e regionais do Ipeadata.
- **Atlas do Estado Brasileiro** — indicadores institucionais e territoriais do Estado brasileiro. ⚠️ *verificar link*

### Saúde / Epidemiologia 

- [**DataSUS**](https://github.com/rfsaldanha/microdatasus) - Dados compilados e pre-processados do SUS. 
- [**Sistema de Informação em Saúde no Brasil.**] (https://rfsaldanha.github.io/sis/) - Livro que apresenta os principais Sistemas de Informação em Saúde no Brasil. **R**

### Hidrologia / Clima

- [**ANA / HidroWeb**](https://www.snirh.gov.br/hidroweb/) — séries históricas de vazão e chuva da Agência Nacional de Águas.
- [**CPTEC / INPE**](https://www.cptec.inpe.br/) — previsão numérica do tempo e projeções climáticas regionalizadas.

## QGIS Plugins

- [**NetFlora**](https://plugins.qgis.org/plugins/Netflora/) — plugin para inventário florestal com drones, geotecnologias e inteligência artificial.
- [**QuickMapServices**](https://github.com/nextgis/quickmapservices) — adiciona dezenas de basemaps prontos (Google, Bing, OSM, etc.) direto no QGIS.

## Google Earth Engine (GEE)

- [**geemap**](https://geemap.org/) — biblioteca Python para visualização interativa e análise com o Google Earth Engine.
- [**Awesome Google Earth Engine**](https://github.com/gee-community/awesome-google-earth-engine) — lista curada de tutoriais, datasets e recursos para GEE.

## AI

- [**Hugging Face Hub**](https://huggingface.co/) — modelos, datasets e demos de IA prontos para usar, incluindo visão computacional geoespacial.
- [**Kaggle**](https://kaggle.com) - datasets, exemplos e 10 horas semanais de GPU de "graça" para treinar os modelos.
- [**Lightning**](https://lightning.ai/clusters) - clusters and cota de GPU para treinar os modelos. 

## Databases

- [**PostGIS**](https://postgis.net/) — extensão espacial para PostgreSQL, o padrão de facto para banco de dados geoespacial.
- [**DuckDB (spatial extension)**](https://duckdb.org/docs/extensions/spatial) — banco analítico local com suporte a geometrias e leitura direta de GeoParquet/Shapefile.

## Cloud Computing

- [**Zarr**](https://zarr.dev/) — formato de arrays multidimensionais em chunks, muito usado para cubos de dados climáticos/satelitais.
- [**COG (Cloud Optimized GeoTIFF)**](https://www.cogeo.org/) — GeoTIFF organizado para leitura parcial eficiente direto da nuvem.
- [**GeoParquet**](https://geoparquet.org/) — formato colunar (Parquet) para dados vetoriais, otimizado para análise em escala.
- [**STAC (SpatioTemporal Asset Catalog)**](https://stacspec.org/) — especificação aberta para catalogar dados geoespaciais na nuvem; base do Planetary Computer, Earth Engine Catalog e Brazil Data Cube.

## R libraries

- [**terra**](https://rspatial.github.io/terra/) — manipulação de dados raster e vetoriais em R.
- [**sf**](https://r-spatial.github.io/sf/) — pacote "simple features" para manipulação de dados vetoriais em R.
- [**ggplot2**](https://ggplot2.tidyverse.org/) — gráficos e mapas estáticos, incluindo `geom_sf` para dados espaciais.
- [**stars**](https://r-spatial.github.io/stars/) — arrays espaço-temporais (raster multibanda, cubos de dados) em R.
- [**SITS**](https://github.com/e-sensing/sits) — pacote brasileiro para análise de séries temporais de imagens de satélite.

## Python Libraries

### Geospatial Data

- [**Rasterio**](https://rasterio.readthedocs.io/) — biblioteca Python para leitura, escrita e processamento de dados raster geoespaciais, como imagens de satélite e modelos de terreno.

### Machine Learning

- [**scikit-learn**](https://scikit-learn.org/) — machine learning "tradicional" em Python: regressão, clustering, classificação.

### Computer Vision

- [**OpenCV**](https://opencv.org/) — manipulação e processamento de imagens.
- [**scikit-image**](https://scikit-image.org/) — processamento de imagens científico, integrado ao ecossistema NumPy/SciPy.

### Deep Learning

- [**PyTorch**](https://pytorch.org/) — framework de deep learning mais usado em pesquisa.
- [**transformers**](https://huggingface.co/docs/transformers) — biblioteca da Hugging Face, fácil de integrar modelos pré-treinados (incluindo visão).
- [**torchgeo**](https://torchgeo.readthedocs.io/) — biblioteca para deep learning com dados geoespaciais sobre PyTorch (datasets, samplers, modelos prontos).

## References

Awesome-pages de referência:

- [**Awesome Geospatial**](https://github.com/sacridini/Awesome-Geospatial) — lista extensa de bibliotecas, dados e ferramentas geoespaciais (não é Brasil-específica).
- **Awesome-Index** — ⚠️ *completar* (nome anotado sem link ainda)
