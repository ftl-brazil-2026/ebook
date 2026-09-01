# Como o nosso mapa "antes/depois" funciona por dentro?

Explicando pra quem nunca ouviu falar nisso — tipo um amigo de 13 anos.

## O problema: um mapa é um site, e sites vivem na internet

Um mapa como o Google Maps é, no fundo, uma página de internet: tem HTML,
tem CSS (a parte bonita), e tem JavaScript (a parte que se mexe quando você
arrasta ou dá zoom). Só que a gente não quer publicar nosso mapa na internet
de verdade — a gente só quer ver ele aparecer dentro do notebook, no nosso
próprio computador.

Então surgem 3 perguntas:

1. Como transformar nosso mapa em uma "mini página de internet" dentro do notebook?
2. Como mostrar uma foto de satélite gigante (nossa imagem CBERS) nesse mapa,
   sem travar o computador?
3. Como fazer o VS Code — que é meio teimoso — deixar essa página se comunicar
   com o Python que está rodando por trás?

Cada uma dessas perguntas é resolvida por uma ferramenta diferente.

## Pergunta 1: o `folium` — o pedreiro que constrói a mini página

Pensa no `folium` como um pedreiro. Você dá pra ele um monte de instruções em
Python ("bota um mapa aqui", "põe uma linha verde ali", "coloca esse ponto
vermelho") e ele constrói, escondidinho, uma página de internet completinha
— com HTML, CSS e JavaScript — só que tudo guardado dentro de uma "caixinha"
chamada `iframe`.

Um `iframe` é tipo uma televisão dentro da sua tela: é uma janelinha isolada,
com sua própria página rodando lá dentro, sem bagunçar o resto do notebook.
É por isso que o mapa do `folium` sempre funciona: ele nunca depende de
nenhum "protocolo esquisito" do Jupyter, ele é só... uma página normal,
dentro de uma TV pequena, dentro da sua célula do notebook.

O `leafmap` (que a gente também usou) é basicamente um ajudante do `folium`
que sabe fazer coisas mais avançadas, tipo o efeito de "arrastar a linha
para comparar duas fotos" (`split_map`).

## Pergunta 2: o `localtileserver` — a pizzaria que só faz o pedaço que você pede

Agora, o problema chato: nossa foto de satélite (o GeoTIFF) pode ter
milhões e milhões de pixels. Se a gente tentasse jogar essa foto inteira,
de uma vez, dentro do mapa, duas coisas ruins aconteceriam:

- Ia demorar uma eternidade pra carregar.
- Se você desse zoom, a foto ia ficar toda quadriculada e feia (tipo
  quando você aumenta demais uma foto do celular).

É aqui que entra o `localtileserver`. Pensa nele como uma **pizzaria**
que mora escondida dentro do seu próprio computador. Ela não entrega a
pizza inteira de uma vez — ela corta a pizza em **fatias** (as "tiles",
que são só pedacinhos quadrados da imagem, tipo 256x256 pixels) e só
entrega a fatia que você está olhando naquele momento, no zoom que você
está usando.

Quando você arrasta o mapa ou dá zoom, o mapa manda um pedido tipo:
"ei, me dá a fatia (z=12, x=843, y=1502)!" — e o `localtileserver`
corta bem aquele pedacinho na hora, na resolução certa, e manda de volta
como uma imagenzinha PNG. Se você olhar outro canto do mapa, ele corta
outra fatia. Nunca precisa entregar a foto inteira de uma vez — por isso
o zoom fica nítido e o computador não trava.

Tecnicamente, essa "pizzaria" é um **servidorzinho web** (rodando por
baixo dos panos com FastAPI/uvicorn) que mora dentro do mesmo programa
Python do seu notebook, escutando pedidos em um endereço tipo
`http://127.0.0.1:PORTA/...` — o `127.0.0.1` é o "endereço de casa" do
seu próprio computador (ninguém de fora consegue bater nessa porta, só
você mesmo).

**Importante:** essa pizzaria só existe enquanto o kernel do notebook
está ligado. Se você desligar/reiniciar o kernel, a pizzaria fecha as
portas — e o mapa para de carregar fatias novas.

## Pergunta 3: o "jupyter loopback" — o walkie-talkie secreto

Aqui está a parte mais esperta de tudo.

O mapa (aquela TV/`iframe` que o folium construiu) mora **dentro do VS
Code**. Só que o VS Code, por segurança, coloca essa TV dentro de uma
"bolha" bem fechada — ele não deixa qualquer coisa lá dentro simplesmente
sair batendo na porta `127.0.0.1:PORTA` da nossa pizzaria. Em um Jupyter
normal (aquele que abre no navegador Chrome/Firefox), essa bolha não
existe, e a TV consegue pedir fatia direto na pizzaria sem problema. Mas
no VS Code (e também no Google Colab, por exemplo), essa bolha existe —
e sem ajuda, o mapa ficaria cinza, sem nenhuma fatia de foto aparecendo.

A solução foi criar um **walkie-talkie escondido**: em vez da TV pedir a
fatia direto pra pizzaria (o que a bolha bloquearia), ela manda o pedido
por um canal secreto que **já existe** entre o notebook e o Python —
esse canal se chama "comm" (de "communication"), e é o mesmo tipo de
canal que os widgets interativos do Jupyter (tipo botões e sliders) já
usam pra conversar com o Python.

Então o fluxo vira:

1. A TV (o mapa) quer uma fatia da foto.
2. Ela manda o pedido pelo walkie-talkie (o "comm") em vez de bater
   direto na porta da pizzaria.
3. Do outro lado, dentro do Python, tem um "atendente" (o
   `jupyter_loopback`) que pega esse pedido, entrega pra pizzaria de
   verdade (`127.0.0.1:PORTA`), pega a fatia de volta, e manda de volta
   pelo mesmo walkie-talkie.
4. A TV recebe a fatia e mostra, sem nunca ter precisado furar a bolha
   de segurança do VS Code.

Esse "atendente" aparece no notebook como uma coisinha meio esquisita
chamada `CommBridge`. Ele não é a foto nem o mapa — ele é só o carteiro
que carrega as fatias de um lado pro outro. Ele é ligado automaticamente
sempre que a gente usa o `localtileserver` dentro do folium/leafmap, então
a gente nem precisa pensar nisso — ele só "faz o trabalho sujo" de furar a
bolha do VS Code de um jeito permitido e seguro.

## Resumindo com uma analogia só

Imagina um restaurante:

- O **folium** é quem constrói o salão do restaurante (mesas, cardápio,
  decoração) — é a parte visual, o "site" dentro do notebook.
- O **localtileserver** é a cozinha, que só prepara o prato (a fatia da
  foto) na hora que alguém pede, do jeitinho que a pessoa quer (no zoom
  certo).
- O **jupyter loopback** é o garçom disfarçado, que consegue entrar na
  cozinha mesmo quando tem uma porta trancada no meio do caminho (a bolha
  de segurança do VS Code), levando o pedido e trazendo o prato de volta
  pra mesa sem que ninguém perceba a porta trancada.

Juntando os três, a gente consegue ver, dentro do próprio notebook, duas
fotos de satélite gigantes, lado a lado, com um controle de "arrastar pra
comparar" — tudo isso sem precisar publicar nada na internet e sem travar
o computador.
