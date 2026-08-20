---
title: "Utilitários de CLI"
---

Antes de escrever qualquer código em Python, você precisa estar confortável navegando em um terminal — você vai usá-lo para ativar ambientes, rodar scripts e gerenciar arquivos durante todo o bootcamp. Aqui estão os comandos que você vai usar o tempo todo.

::: {.callout-tip appearance="simple"}
## O comando mais importante desta página

`man <comando>` (ou `<comando> --help`) — todo comando abaixo tem um manual. Na dúvida, pergunte para a própria ferramenta antes de procurar na internet.
:::

## Pedindo ajuda

| Comando | O que faz |
|---|---|
| `man ls` | Abre a página de manual do `ls` (pressione `q` para sair) |
| `ls --help` | Resumo rápido de uso, sem precisar do manual |
| `which python` | Mostra qual executável roda de fato quando você digita `python` |

## Se localizando no sistema

| Comando | O que faz |
|---|---|
| `pwd` | Mostra o diretório atual — "onde eu estou?" |
| `ls` | Lista os arquivos do diretório atual |
| `ls -la` | Lista todos os arquivos (incluindo os ocultos, com `.`) com detalhes |
| `cd <caminho>` | Muda de diretório |
| `cd ..` | Sobe um nível de diretório |
| `cd ~` | Vai para o seu diretório home |

## Trabalhando com arquivos e diretórios

| Comando | O que faz |
|---|---|
| `cat <arquivo>` | Imprime o conteúdo de um arquivo na tela |
| `less <arquivo>` | Percorre o conteúdo de um arquivo (pressione `q` para sair) |
| `mkdir <nome>` | Cria um novo diretório |
| `touch <arquivo>` | Cria um arquivo vazio |
| `cp <origem> <destino>` | Copia um arquivo |
| `mv <origem> <destino>` | Move ou renomeia um arquivo |
| `rm <arquivo>` | Apaga um arquivo — sem desfazer, sem lixeira, cuidado |
| `rm -r <dir>` | Apaga um diretório e tudo dentro dele — mesmo aviso, em dobro |

## Buscando

| Comando | O que faz |
|---|---|
| `grep "texto" <arquivo>` | Busca por um trecho de texto dentro de um arquivo |
| `find . -name "*.py"` | Busca arquivos por padrão de nome, a partir do diretório atual |

## Atalhos essenciais desde o primeiro dia

| Atalho / Comando | O que faz |
|---|---|
| `Tab` | Autocompleta nomes de arquivos e pastas — use sempre, evita erros de digitação |
| `↑` / `↓` | Percorre os comandos anteriores |
| `Ctrl + C` | Interrompe o que estiver rodando no momento |
| `Ctrl + R` | Busca no histórico de comandos |
| `clear` | Limpa a tela do terminal |
| `history` | Lista os comandos executados recentemente |

## Combinando comandos

| Sintaxe | O que faz |
|---|---|
| `comando1 \| comando2` | Pipe: envia a saída do `comando1` como entrada do `comando2` |
| `comando > arquivo.txt` | Redireciona a saída para um arquivo (sobrescreve) |
| `comando >> arquivo.txt` | Redireciona a saída para um arquivo (adiciona ao final) |

::: {.callout-note appearance="simple"}
## Praticando

Abra um terminal, dê `cd` para dentro deste repositório e tente: `ls -la`, `cat README.md`, `man ls` e `history`.
:::
