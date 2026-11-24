---
title: "Como Contribuir"
---

Esse ebook cresce com contribuição dos alunos. Por enquanto, tem duas formas diretas de contribuir, contudo o repositório visa ser uma contribução coletiva de muitas formas, então diversas outras maneiras aparecerão ao longo do bootcamp.

Antes de editar qualquer coisa, crie sua própria branch! Veja o passo 3 da página de [Setup](setup.md). Isso evita conflito com atualizações futuras do repositório.

## Contribuindo com o Awesome Geospatial

A página [Awesome Geospatial](../awesome-geospatial/index.md) é uma lista de ferramentas organizadas por plataforma (QGIS, Google Earth Engine, Machine Learning, AI, Databases, Cloud Computing).

Para adicionar uma ferramenta, edite [`awesome-geospatial/index.md`](../awesome-geospatial/index.md) e inclua um item na lista, sob a seção da plataforma correspondente:

```markdown
- [**Nome**](https://link.com) — descrição curta do que é / para que serve.
```

Se você não tem certeza que o link ou a descrição estão corretos/atualizados, adicione `⚠️ *verificar*` no fim da linha — assim outra pessoa sabe que precisa conferir antes de confiar no item. Sem essa marcação, o item é considerado confiável.

Se a plataforma que você quer ainda não tem uma seção, crie um novo `## Nome da Plataforma` no fim do arquivo.

## Contribuindo com o diagrama de provedores (bubble chart)

O diagrama de bolhas em [Provedores de Dados Geoespaciais](provedores.qmd) — temas de interesse ligados a provedores de dados geoespaciais — é gerado a partir de um único arquivo: [`course-info/data/provedores.json`](data/provedores.json). Não existe cópia duplicada dos dados em nenhum outro lugar — editar esse arquivo é suficiente para atualizar o gráfico.

Para adicionar um provedor a um tema já existente, inclua um novo objeto na lista `provedores` da categoria correspondente:

```json
{
  "nome": "Nome do provedor",
  "escopo": "BR",
  "url": "https://exemplo.gov.br/",
  "dado": "Uma frase curta: qual dado, para qual uso"
}
```

`escopo` é sempre `"BR"` ou `"GLOBAL"`. Para criar um tema novo inteiro, adicione um objeto à lista `categorias` (nível raiz do JSON) com `nome`, `votos` (pode deixar `0` se não veio do questionário original) e sua própria lista de `provedores`.

Antes de commitar, valide que o JSON continua válido:

``` bash
python3 -m json.tool course-info/data/provedores.json > /dev/null
```

Sem erro impresso = JSON válido.

## Adicionando seu Capstone Project

Todos os projetos finais ficam listados em um único arquivo: [`capstone_projects/projects.yml`](../capstone_projects/index.qmd). Cada item vira um card na página [Capstone Projects](../capstone_projects/index.qmd) — não precisa editar mais nada.

Adicione um item no fim do arquivo:

```yaml
- title: "Nome do Projeto"
  author: "Seu Nome"
  description: "Uma ou duas frases: qual problema, quais dados, qual resultado."
  categories: [Sensoriamento Remoto, Machine Learning]
  site: "https://seu-usuario.github.io/seu-projeto/"   # opcional, se o projeto tiver uma página pública
  repo: "https://github.com/seu-usuario/seu-projeto"   # opcional
  # image: images/nome-do-projeto.png                  # opcional: screenshot para o card
```

Informe pelo menos `site` ou `repo`. Com `site`, o card mostra uma prévia ao vivo da sua página; sem `site`, mostra um bloco com o link do repositório. Se o seu site for pesado (mapas grandes, muitos dados carregando ao vivo), salve um screenshot da página inicial em `capstone_projects/images/` e use o campo `image` — o card passa a mostrar a imagem em vez da prévia.

::: {.callout-note appearance="simple"}

## Dúvida?

Pergunta no canal do bootcamp antes de gastar muito tempo tentando resolver sozinho.
:::
