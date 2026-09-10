import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Processamento de Imagens

    Nessa aula vamos sair um pouco do sensoriamento remoto "puro" (bandas, índices espectrais) e voltar pro básico de **processamento de imagens**. No fundo, bem no fundo, toda imagem de satélite também é apenas... uma imagem. As mesmas ferramentas que processam uma foto do seu celular podem processar uma cena de satélite.

    Para a aula de hoje, vamos usar duas bibliotecas extremamente comuns no processamento de imagem.

    - **OpenCV** (`cv2`): a biblioteca mais usada em visão computacional, super rápida (em C++), mas com algumas pegadinhas bem conhecidas (spoiler: BGR).
    - **scikit-image** (`skimage`): mais "pythônica", integra bem com numpy/matplotlib, e tem uma ótima documentação.

    Roteiro de hoje:
    1. Imagem = array numpy (de novo porque sim)
    2. OpenCV vs scikit-image
    3. Cropping
    4. Escala de cinza (grayscale)
    5. Histograma e equalização
    6. Correção de brilho/contraste
    7. Resizing e rescaling
    8. Kernels e blurring (incluindo Gaussian blur)
    9. Detecção de bordas (Sobel, Canny)
    10. Connected Component Analysis
    11. Ligando tudo com o pré-processamento usado pra treinar redes neurais

    Vamos usar uma imagem de satélite real (um quicklook CBERS-4/MUX) como nossa "cobaia" — mas hoje ela vai ser tratada como uma imagem qualquer (PNG comum), sem `rasterio`, sem bandas espectrais. É só pixels.
    """)
    return


@app.cell
def _():
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    from skimage import io, color, exposure, filters, feature, measure, transform

    print("OpenCV:", cv2.__version__)
    import skimage
    print("scikit-image:", skimage.__version__)
    return color, cv2, exposure, filters, np, plt, skimage, transform


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Nossa imagem de hoje

    É um quicklook (PNG já pronto, tipo uma "foto" da cena) de uma cena CBERS-4/MUX sobre a região de Novo Progresso (PA). A mesma área do desmatamento que vimos na aula de STAC. Só que hoje, em vez de baixar bandas separadas com `rasterio`, vamos direto no PNG, como qualquer imagem.
    """)
    return


@app.cell
def _():
    import os
    import requests
    img_dir = 'images'
    os.makedirs(img_dir, exist_ok=True)
    img_path = os.path.join(img_dir, 'cbers4_novo_progresso_2023.png')
    if not os.path.exists(img_path):
        url = 'https://data.inpe.br/bdc/data/cbers4/2023_07/CBERS_4_MUX_DRD_2023_07_18.13_49_30_CB11/167_109_0/4_BC_UTM_WGS84/CBERS_4_MUX_20230718_167_109.png'
        _resp = requests.get(url, timeout=30)
        with open(img_path, 'wb') as f:
            f.write(_resp.content)
    print('arquivo:', img_path, '-', os.path.getsize(img_path) / 1024, 'KB')
    return img_path, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Imagem é nada menos que um array em numpy

    Vale a pena fixar essa ideia na cabeça de porongo. (baseado em: [scikit-image — Images are numpy arrays](https://scikit-image.org/docs/stable/user_guide/numpy_images.html)):

    - Uma imagem colorida é um array 3D: `(altura, largura, canais)` — normalmente 3 canais (R, G, B);
    - Cada pixel é um número de `0` a `255` (Quando a image é do tipo `uint8`, ou seja 8 bits);
    - `imagem[linha, coluna]` te dá um pixel (um array de 3 números); `imagem[linha, coluna, canal]` te dá um número só;
    - Como é numpy, tudo que você já sabe sobre slicing ou indexação funcionará, como cortar pedaços, pegar só um canal, inverter, etc.
    """)
    return


@app.cell
def _(img_path, skimage):
    img_rgb = skimage.io.imread(img_path)[:, :, :3]  # descarta o canal alpha, se tiver
    return (img_rgb,)


@app.cell
def _(img_rgb):
    img_rgb.shape
    return


@app.cell
def _(img_rgb):
    # Pegando um pixel - aqui vai mostrar os 3 canais (RGB)
    img_rgb[100,200]
    return


@app.cell
def _(img_rgb):
    img_rgb[100,200,1]
    return


@app.cell
def _(img_rgb, plt):
    plt.imshow(img_rgb)
    return


@app.cell
def _(img_rgb, plt):
    _fig, _axes = plt.subplots(1, 4, figsize=(16, 4))
    _axes[0].imshow(img_rgb)
    _axes[0].set_title('RGB completo')
    for _ax, ch, nome, cmap in zip(_axes[1:], range(3), ['Vermelho (R)', 'Verde (G)', 'Azul (B)'], ['Reds', 'Greens', 'Blues']):
        _ax.imshow(img_rgb[:, :, ch], cmap=cmap)
        _ax.set_title(nome)
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. A pegadinha do BGR

    Por razões históricas (câmeras antigas, bibliotecas de 20+ anos atrás), o OpenCV lê e escreve imagens coloridas em ordem **BGR** (azul, verde, vermelho), o que é ao contrário de praticamente todo o resto do mundo Python (`skimage`, `matplotlib`, `PIL`), que usa **RGB**.

    Isso é uma fonte clássica de bugs, fica ligado!  Se você ler com `cv2.imread` e mostrar direto com `matplotlib`, as cores saem trocadas (fica com um tom azulado estranho).
    """)
    return


@app.cell
def _(cv2, img_path, img_rgb, np, plt):
    img_bgr = cv2.imread(img_path)
    img_bgr_para_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    print('são iguais ao lido pelo skimage?', np.array_equal(img_bgr_para_rgb, img_rgb))
    fig_1, _axes = plt.subplots(1, 2, figsize=(10, 5))
    _axes[0].imshow(img_bgr)
    _axes[0].set_title('BGR')
    _axes[1].imshow(img_bgr_para_rgb)
    _axes[1].set_title('COLOR_BGR2RGB)')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. Cropping

    Cropping é basicamente uma operação de cortamos o pedaço que nos interessa da imagem. Ele pode ser feito de forma muito fácil e acessível através de uma simples indexação dos array.

    Tal como: `imagem[linha_inicio:linha_fim, coluna_inicio:coluna_fim]`.
    """)
    return


@app.cell
def _(img_rgb):
    img = img_rgb[220:480, 120:520]  # daqui pra frente, "img" é a nossa imagem de trabalho
    return


@app.cell
def _(img_rgb, plt):
    img_1 = img_rgb[220:480, 120:520]
    fig_2, _axes = plt.subplots(1, 2, figsize=(12, 5))
    _axes[0].imshow(img_rgb)
    _axes[0].set_title(f'Original {img_rgb.shape[:2]}')
    _axes[1].imshow(img_1)
    _axes[1].set_title(f'Cortada (crop) {img_1.shape[:2]}')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return (img_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Escala de cinza (grayscale)

    Se temos uma imagem em RGB e três canais, poderíamos converter ela para uma escala de cinza. Contudo, isso não é apenas calcular a média dos três canais pois isso não replica o comportamento do olho humano. Assim, precisamos fazer uma média ponderada, esses valores de peso já são bem estabelecidos na literatura e as duas bibliotecas possuem funções para converter de forma muito simples.

    O olho humano é mais sensível ao verde do que ao azul, por exemplo. Por isso se usa uma média **ponderada**:

    $$\text{cinza} = 0.299 \times R + 0.587 \times G + 0.114 \times B$$

    Tanto o OpenCV quanto o scikit-image já implementam isso pra você.
    """)
    return


@app.cell
def _(color, cv2, img_1):
    # primeiro le a imagem e converte pra cinza
    gray_cv = cv2.cvtColor(img_1, cv2.COLOR_RGB2GRAY)  # uint8, 0-255
    # ja le convertendo para cinza e escala normaliza entre 0-1 
    gray_sk = color.rgb2gray(img_1)  # float, 0.0-1.0
    return gray_cv, gray_sk


@app.cell
def _(gray_cv, gray_sk):
    print("cv2:     dtype =", gray_cv.dtype, "| min/max =", gray_cv.min(), gray_cv.max())
    print("skimage: dtype =", gray_sk.dtype, "| min/max =", round(gray_sk.min(), 3), round(gray_sk.max(), 3))
    return


@app.cell
def _(color, cv2, img_1, plt):
    gray_cv_1 = cv2.cvtColor(img_1, cv2.COLOR_RGB2GRAY)
    gray_sk_1 = color.rgb2gray(img_1)
    print('cv2:     dtype =', gray_cv_1.dtype, '| min/max =', gray_cv_1.min(), gray_cv_1.max())
    print('skimage: dtype =', gray_sk_1.dtype, '| min/max =', round(gray_sk_1.min(), 3), round(gray_sk_1.max(), 3))
    fig_3, _axes = plt.subplots(1, 2, figsize=(10, 5))
    _axes[0].imshow(gray_cv_1, cmap='gray')
    _axes[0].set_title('cv2.cvtColor (uint8, 0-255)')
    _axes[1].imshow(gray_sk_1, cmap='gray')
    _axes[1].set_title('skimage.color.rgb2gray (float, 0-1)')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return gray_cv_1, gray_sk_1


@app.cell
def _(img_rgb, plt, skimage):
    # tentamos fazer o mesmo com scikit-image
    gray_skimage = skimage.color.rgb2gray(img_rgb)
    plt.imshow(gray_skimage, cmap='gray')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Correção de brilho e constrate
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Convertendo para ponto flutuante em [0, 1]

    Pra facilitar a aritmética das próximas seções (brilho e contraste), vamos converter a imagem para ponto flutuante, com valores entre `0` e `1`, usando `img_as_float`. Isso evita os problemas de estouro (overflow) de inteiros que vimos antes, e deixa as fórmulas bem mais diretas de entender.
    """)
    return


@app.cell
def _(img_1, plt):
    from skimage import img_as_float
    image = img_as_float(img_1)
    # Convertendo para ponto flutuante, no intervalo [0, 1]
    plt.imshow(image)
    plt.axis('off')
    plt.show()
    return (image,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Correção de brilho

    O brilho é relacionado com a intensidade dos valores. Se nossa image é um `uint8`, sua escala vai de 0-255, onde zero seria uma intensidade mais escura e 255 mais clara. Se a gente quer aumentar o brilho, a gente está aumentando esses valores para se aproximar de 255.

    ```
    0       - black
    50      - dark gray
    128     - medium gray
    200     - light gray
    255     - white
    ```
    Portanto o brilho responde a questão se essa imagem é geralmente mais clara ou mais escura.

    A forma mais simples de mudar o brilho é somar (ou subtrair) uma constante de cada pixel:

    $$ I_{novo} = I + \beta $$

    onde $\beta$ controla o brilho.
    """)
    return


@app.cell
def _(image, np):
    brilho = 0.2

    mais_claro = np.clip(image + brilho, 0, 1)
    mais_escuro = np.clip(image - brilho, 0, 1)
    return mais_claro, mais_escuro


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `np.clip()` é essencial aqui: as intensidades válidas de uma imagem precisam ficar entre `0` e `1` — sem ele, valores como `1.1` ou `-0.05` quebrariam a visualização

    Podemos visualizar os resultados:
    """)
    return


@app.cell
def _(image, mais_claro, mais_escuro, plt):
    fig_4, _axes = plt.subplots(1, 3, figsize=(12, 4))
    _axes[0].imshow(image)
    _axes[0].set_title('Original')
    _axes[1].imshow(mais_claro)
    _axes[1].set_title('Mais claro')
    _axes[2].imshow(mais_escuro)
    _axes[2].set_title('Mais escuro')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Ponto de atenção:** para uma imagem em escala de cinza de 8 bits (`uint8`), a operação equivalente seria:

    ```python
    mais_claro = np.clip(image + 30, 0, 255)
    ```

    A ideia central não muda pois o brilho é uma mudança no **nível geral** de intensidade.
    """)
    return


@app.cell
def _(mais_claro, plt):
    # Uma vez que aumentamos o brilho de uma imagem, podemos mascarar apenas os pixels de alta intensidade
    mais_claro[mais_claro<0.7]=0
    plt.imshow(mais_claro)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Correção de contraste

    O constrate é uma alteração de valores para longe de um determinado valor central. Portanto, constrate responde a questão de quão diferente esses valores estão das regiões mais claras e escuras.

    O contraste pode ser alterado multiplicando os valores de pixel em torno de um valor central:

    $$ I_{novo} = \alpha(I - c) + c $$

    onde:

    - $\alpha > 1$ → aumenta o contraste
    - $0 < \alpha < 1$ → diminui o contraste
    - $c$ → intensidade de referência, geralmente `0.5`
    """)
    return


@app.cell
def _(image, np):
    _contraste = 1.5
    alto_contraste = np.clip(_contraste * (image - 0.5) + 0.5, 0, 1)
    return (alto_contraste,)


@app.cell
def _(image, np):
    # Para reduzir o contraste
    _contraste = 0.3
    baixo_contraste = np.clip(_contraste * (image - 0.5) + 0.5, 0, 1)
    return (baixo_contraste,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Por que subtrair e somar 0,5?**

    Suponha um pixel com valor `0.7`:

    ```
    0.7 - 0.5 = 0.2
    0.2 × 1.5 = 0.3
    0.3 + 0.5 = 0.8
    ```

    O pixel se afasta do ponto médio, aumentando o contraste.

    Da mesma forma, um pixel de `0.3` vira `0.2`, se afastando do ponto médio na direção oposta.
    """)
    return


@app.cell
def _(alto_contraste, baixo_contraste, image, plt):
    fig_5, _axes = plt.subplots(1, 3, figsize=(12, 4))
    _axes[0].imshow(image)
    _axes[0].set_title('Original')
    _axes[1].imshow(alto_contraste)
    _axes[1].set_title('Contraste alto (α=1.5)')
    _axes[2].imshow(baixo_contraste)
    _axes[2].set_title('Contraste baixo (α=0.5)')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Alongamento de contraste

    Uma técnica particularmente didática é o **contrast stretching**. O scikit-image já oferece isso pronto em `exposure.rescale_intensity()`:
    """)
    return


@app.cell
def _(exposure, image, plt):
    esticada = exposure.rescale_intensity(image, in_range=(0.2, 0.8), out_range=(0, 1))
    plt.imshow(esticada)
    plt.axis('off')
    plt.show()
    return (esticada,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Aqui, pixels próximos de `0.2` viram preto e pixels próximos de `0.8` viram branco.

    Isso é útil quando a imagem ocupa só uma pequena parte da faixa de intensidade disponível.

    ### Contrast stretching automático

    Em vez de escolher `0.2` e `0.8` na mão, dá pra calcular limites úteis a partir da própria imagem, por exemplo, usando percentis:
    """)
    return


@app.cell
def _(image, np):
    np.percentile(image, 2)
    return


@app.cell
def _(esticada, exposure, image, np, plt):
    baixo = np.percentile(image, 2)
    alto = np.percentile(image, 98)
    esticada_automatica = exposure.rescale_intensity(image, in_range=(baixo, alto), out_range=(0, 1))
    fig_6, _axes = plt.subplots(1, 3, figsize=(12, 4))
    _axes[0].imshow(image)
    _axes[0].set_title('Original')
    _axes[1].imshow(esticada)
    _axes[1].set_title('Stretching manual (0.2-0.8)')
    _axes[2].imshow(esticada_automatica)
    _axes[2].set_title('Stretching automático (percentis 2-98)')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    O 2º percentil vira aproximadamente preto e o 98º percentil vira aproximadamente branco.

    Isso costuma funcionar melhor do que usar o mínimo e o máximo absolutos, porque alguns poucos pixels extremos não acabam dominando toda a transformação.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Histograma e equalização

    Um **histograma** de imagem é só a contagem de quantos pixels têm cada valor de intensidade (0 a 255). Imagens com baixo contrast e meio embaçadas, (muito comum em imagens de satélite com neblina/bruma atmosférica) têm um histograma concentrado numa faixa estreita.

    Dessa forma, já vimos uma das maneiras de corrigir isso que é alterando o constrate e brilho de uma image.

    Uma outra forma bastante comum de corrigir é através da equalização do histograma.

    **Equalização de histograma** redistribui essas intensidades pra ocupar toda a faixa de 0-255, "esticando" o contraste. Vamos comparar três versões:
    - `cv2.equalizeHist` — equalização global clássica;
    - `skimage.exposure.equalize_hist` — equivalente do scikit-image;
    - `equalize_adapthist` (CLAHE) — equalização **adaptativa**, calculada em blocos da imagem. Geralmente funciona melhor quando o contraste varia de uma região pra outra (ex: nuvens de um lado, sombra do outro).
    """)
    return


@app.cell
def _(cv2, exposure, gray_cv_1, np, plt):
    eq_cv = cv2.equalizeHist(gray_cv_1)
    eq_sk = exposure.equalize_hist(gray_cv_1)
    eq_clahe = exposure.equalize_adapthist(gray_cv_1, clip_limit=0.03)
    fig_7, _axes = plt.subplots(2, 4, figsize=(16, 8))
    for _ax, imagem, titulo in zip(_axes[0], [gray_cv_1, eq_cv, eq_sk, eq_clahe], ['Original', 'cv2.equalizeHist', 'skimage.equalize_hist', 'CLAHE (adaptativo)']):
        _ax.imshow(imagem, cmap='gray')
        _ax.set_title(titulo)
        _ax.axis('off')
    for _ax, imagem, titulo in zip(_axes[1], [gray_cv_1, eq_cv, eq_sk, eq_clahe], ['Original', 'cv2.equalizeHist', 'skimage.equalize_hist', 'CLAHE (adaptativo)']):
        _ax.hist(np.asarray(imagem).ravel(), bins=64)
        _ax.set_title(f'histograma — {titulo}')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Qual a ideia matemática da normalização do histograma

    A equalização que acabamos de ver (`cv2.equalizeHist`, `equalize_hist`, CLAHE) não é mágica. Vamos reconstruir esse pipeline do zero, passo a passo, usando nossa imagem em escala de cinza e `uint8` com 0-255:

    ```
    Imagem
      ↓
    Histograma
      ↓
    Histograma normalizado (PMF)
      ↓
    CDF
      ↓
    Função de mapeamento
      ↓
    Novas intensidades
      ↓
    Imagem equalizada
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    O histograma conta quantos pixels têm cada intensidade $r_k$, para $k = 0, 1, \dots, L-1$ (com $L = 256$ níveis):

    $$ h(r_k) = \#\{(i,j) \;:\; I(i,j) = r_k\} $$

    Somando todos os bins do histograma, recuperamos o número total de pixels da imagem ($M \times N$):

    $$ \sum_{k=0}^{L-1} h(r_k) = M \times N $$
    """)
    return


@app.cell
def _(gray_cv_1, np, plt):
    M, N = gray_cv_1.shape
    L = 256
    histograma, bins = np.histogram(gray_cv_1.ravel(), bins=L, range=(0, L))
    print('total de pixels (M x N):', M * N)
    print('soma do histograma:     ', histograma.sum())
    plt.figure(figsize=(8, 4))
    plt.bar(np.arange(L), histograma, width=1, color='steelblue')
    plt.title('Histograma — $h(r_k)$')
    plt.xlabel('Intensidade $r_k$')
    plt.ylabel('Nº de pixels')
    plt.show()
    return L, M, N, histograma


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Dividindo cada $h(r_k)$ pelo total de pixels, transformamos contagens em uma **distribuição de probabilidade**. Essa distribuição de probabilidade é a chance de um pixel qualquer da imagem ter a intensidade $r_k$:

    $$ p(r_k) = \frac{h(r_k)}{M \times N} $$

    Como $h(r_k) \geq 0$ e a soma de todos os $h(r_k)$ é $M \times N$ (Passo 1), temos as duas propriedades de uma PMF válida:

    $$ p(r_k) \geq 0 \quad \text{e} \quad \sum_{k=0}^{L-1} p(r_k) = 1 $$
    """)
    return


@app.cell
def _(L, M, N, histograma, np, plt):
    pmf = histograma / (M * N)
    print("soma da PMF:", pmf.sum())  # deve dar (bem próximo de) 1.0

    plt.figure(figsize=(8, 4))
    plt.bar(np.arange(L), pmf, width=1, color="darkorange")
    plt.title("Histograma normalizado — $p(r_k)$")
    plt.xlabel("Intensidade $r_k$")
    plt.ylabel("Probabilidade")
    plt.show()
    return (pmf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A CDF acumula a probabilidade de um pixel ter intensidade **até** $r_k$:

    $$ c(r_k) = \sum_{j=0}^{k} p(r_j) $$

    Duas propriedades saem direto dessa soma:

    - **Monotonicamente não decrescente**: $c(r_k) \geq c(r_{k-1})$, já que só somamos termos $\geq 0$.
    - **Termina em 1**: $c(r_{L-1}) = \sum_{j=0}^{L-1} p(r_j) = 1$ (é a soma completa da PMF do Passo 2).
    """)
    return


@app.cell
def _(L, np, plt, pmf):
    cdf = np.cumsum(pmf)
    print("c(r_0)   =", round(cdf[0], 4))
    print("c(r_255) =", round(cdf[-1], 4))

    plt.figure(figsize=(8, 4))
    plt.plot(np.arange(L), cdf, color="seagreen", drawstyle="steps-post")
    plt.title("CDF — $c(r_k)$")
    plt.xlabel("Intensidade $r_k$")
    plt.ylabel("Probabilidade acumulada")
    plt.ylim(0, 1.05)
    plt.show()
    return (cdf,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A ideia da equalização é usar a própria CDF como função de transformação, reescalada para a faixa de intensidades

     $[0, L-1]$ (0-255):

    $$ T(r_k) = \text{round}\big((L-1)\, c(r_k)\big) $$

    Essa multiplicação da CDF pelo numero de bins, transforma a CDF em uma distribuição uniforme. Basicamente nessa etapa estamos aplicando uma função que mapeia a CDF numa distribuição uniforme.
    """)
    return


@app.cell
def _(L, cdf, np, plt):
    T = np.round((L - 1) * cdf).astype(np.uint8)

    plt.figure(figsize=(8, 4))
    plt.plot(np.arange(L), T, color="firebrick")
    plt.plot([0, L - 1], [0, L - 1], "--", color="gray", linewidth=1, label="identidade (sem mudança)")
    plt.title("Função de mapeamento — $T(r_k)$")
    plt.xlabel("Intensidade original $r_k$")
    plt.ylabel("Nova intensidade $T(r_k)$")
    plt.legend()
    plt.show()
    return (T,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Por fim, aplicamos $T$ pixel a pixel — trocando cada intensidade $r_k$ pela sua nova intensidade $T(r_k)$ (uma simples tabela de consulta, ou *lookup table*):

    $$ I_{eq}(i, j) = T\big(I(i, j)\big) $$
    """)
    return


@app.cell
def _(T, gray_cv_1, plt):
    gray_equalizado_na_mao = T[gray_cv_1]
    fig_8, _axes = plt.subplots(2, 2, figsize=(10, 8))
    _axes[0, 0].imshow(gray_cv_1, cmap='gray')
    _axes[0, 0].set_title('Original')
    _axes[0, 1].imshow(gray_equalizado_na_mao, cmap='gray')
    _axes[0, 1].set_title('Equalizada (na mão, passo a passo)')
    _axes[1, 0].hist(gray_cv_1.ravel(), bins=64, color='steelblue')
    _axes[1, 0].set_title('Histograma original')
    _axes[1, 1].hist(gray_equalizado_na_mao.ravel(), bins=64, color='firebrick')
    _axes[1, 1].set_title('Histograma equalizado (mais espalhado)')
    for _ax in _axes[0]:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pequeno exemplo numérico:

    Dada a matrix M(4x4) com 16 pixels:

    0  0  1  1
    1  2  2  2
    3  3  4  5
    5  5  6  7

    O histograma dessa matriz é:

    | Intensity \(r\) | Count \(n_r\) |
    | --------------: | ------------: |
    |               0 |             2 |
    |               1 |             3 |
    |               2 |             3 |
    |               3 |             2 |
    |               4 |             1 |
    |               5 |             3 |
    |               6 |             1 |
    |               7 |             1 |

    Normalizando essa matrix

    $ p(r)=n_r/16 $

    Logo a tabela vira:



    | \(r\) | \(p(r)\) |    CDF |
    | ----: | -------: | -----: |
    |     0 |    0.125 |  0.125 |
    |     1 |   0.1875 | 0.3125 |
    |     2 |   0.1875 | 0.5000 |
    |     3 |    0.125 | 0.6250 |
    |     4 |   0.0625 | 0.6875 |
    |     5 |   0.1875 | 0.8750 |
    |     6 |   0.0625 | 0.9375 |
    |     7 |   0.0625 | 1.0000 |

    Sabendo que o numero de bins de nosso histograma é 7, podemos calcular a transformada T

    $ T = 7×CDF(r)$

    e assim, nossa nova matriz equalizada fica:

    | Original \(r\) |   CDF | New \(s\) |
    | -------------: | ----: | --------: |
    |              0 |  .125 |      .875 |
    |              1 | .3125 |    2.1875 |
    |              2 |    .5 |       3.5 |
    |              3 |  .625 |     4.375 |
    |              4 | .6875 |    4.8125 |
    |              5 |  .875 |     6.125 |
    |              6 | .9375 |    6.5625 |
    |              7 |   1.0 |         7 |

    Aqui, precisaríamos só arredondar esses numeros que foram mapeados.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Resizing e rescaling

    Os dois fazem a mesma coisa no geral pois reamostram uma image para outra grade de pixels, mas possuem alguma pequena diferença:

    - **resize**: você diz o **tamanho final exato** (ex: `224x224`) — é o que quase toda rede neural espera como entrada;
    - **rescale**: você diz um **fator de escala** (ex: `0.5` = metade do tamanho) e a função mantém a proporção original.

    O resize necessita sempre um método de interpolação. Image que estamos saindo de um determinado numero de pixels para outro, portanto temos que interpolar esses pixels para pertencerem a uma nova grade.
    Também importa o **método de interpolação**: `INTER_NEAREST` ("quadriculado"), `INTER_LINEAR`/`INTER_CUBIC` (mais suave), `INTER_AREA` (melhor pra *diminuir* a imagem).
    """)
    return


@app.cell
def _(cv2, img_1, plt, transform):
    _resized = cv2.resize(img_1, (224, 224), interpolation=cv2.INTER_AREA)
    rescaled = transform.rescale(img_1, 0.5, channel_axis=-1, anti_aliasing=True)
    print('original:', img_1.shape)
    print('resize p/ 224x224:', _resized.shape)
    print('rescale por 0.5:', rescaled.shape)
    fig_9, _axes = plt.subplots(1, 3, figsize=(14, 5))
    _axes[0].imshow(img_1)
    _axes[0].set_title(f'Original {img_1.shape[:2]}')
    _axes[1].imshow(_resized)
    _axes[1].set_title(f'resize  {_resized.shape[:2]}')
    _axes[2].imshow(rescaled)
    _axes[2].set_title(f'rescale (x0.5)  {rescaled.shape[:2]}')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return (rescaled,)


@app.cell
def _(cv2, img_1, plt, rescaled):
    _resized = cv2.resize(img_1, (224, 224), interpolation=cv2.INTER_AREA)
    resized2 = cv2.resize(img_1, (512, 512), interpolation=cv2.INTER_AREA)
    print('original:', img_1.shape)
    print('resize p/ 224x224:', _resized.shape)
    print('rescale por 0.5:', rescaled.shape)
    fig_10, _axes = plt.subplots(1, 3, figsize=(14, 5))
    _axes[0].imshow(img_1)
    _axes[0].set_title(f'Original {img_1.shape[:2]}')
    _axes[1].imshow(_resized)
    _axes[1].set_title(f'{_resized.shape[:2]}')
    _axes[2].imshow(resized2)
    _axes[2].set_title(f' {resized2.shape[:2]}')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 8. Kernels

    Explicação visual de Kernels: [SETOSA](https://setosa.io/ev/image-kernels/)

    ## O que é um kernel?

    Um **kernel** (ou *filtro*) é só uma matriz pequena (tipo 3x3 ou 5x5) de números. A operação de **convolução** desliza esse kernel por cima de cada pixel da imagem e, em cada posição, faz uma "média ponderada" da vizinhança: multiplica cada pixel vizinho pelo número correspondente do kernel, soma tudo, e esse é o valor do pixel de saída.

    O que muda de um efeito pro outro é **só o conteúdo do kernel**:

    - Kernel de **borrão (box blur)**: todos os valores iguais (ex: `1/9` numa matriz 3x3). Com isso cada pixel vira a média dos vizinhos e ocasiona esse efeito de borrão.
    - Kernel de **nitidez (sharpen)**: valor bem alto no centro, negativo nas bordas. Isso exagera a diferença entre o pixel e seus vizinhos, o que ocasiona um realce dos detalhes.
    - Kernels de **borda** (Sobel, que vamos ver já já): detectam mudanças bruscas de intensidade.

    ## E o Gaussian Blur?

    O "box blur" dá o mesmo peso pra todos os vizinhos, o que pode deixar o resultado meio "quadriculado". O **Gaussian blur** usa um kernel cujos pesos seguem uma **curva em sino** (distribuição normal/gaussiana): o pixel central pesa mais, e os vizinhos pesam cada vez menos quanto mais longe estão. O resultado é um borrão mais suave e "natural".

    O parâmetro `sigma` controla a largura desse sino: `sigma` pequeno = sino estreito = borrão fraco; `sigma` grande = sino largo = borrão forte. O Gaussian blur é usado o tempo todo como um **pré-processamento pra reduzir ruído** antes de outras operações (como detecção de bordas, que veremos a seguir).
    """)
    return


@app.cell
def _():
    import marimo as mo
    from scipy.signal import convolve2d
    from skimage import data
    from PIL import Image
    import urllib.request

    return convolve2d, data, mo


@app.cell
def _(np):
    kernels_3x3 = {
        "Identity": np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=float),
        "Box Blur": np.ones((3, 3), dtype=float) / 9,
        "Gaussian Blur": np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=float) / 16,
        "Sharpen": np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=float),
        "Edge Detect": np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=float),
        "Emboss": np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]], dtype=float),
        "Sobel X": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float),
        "Sobel Y": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float),
    }

    kernels_5x5 = {
        "Identity": np.array(
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            dtype=float,
        ),
        "Box Blur": np.ones((5, 5), dtype=float) / 25,
        "Gaussian Blur": np.array(
            [
                [1, 4, 6, 4, 1],
                [4, 16, 24, 16, 4],
                [6, 24, 36, 24, 6],
                [4, 16, 24, 16, 4],
                [1, 4, 6, 4, 1],
            ],
            dtype=float,
        )
        / 256,
        "Sharpen": np.array(
            [
                [0, 0, -1, 0, 0],
                [0, -1, -1, -1, 0],
                [-1, -1, 13, -1, -1],
                [0, -1, -1, -1, 0],
                [0, 0, -1, 0, 0],
            ],
            dtype=float,
        ),
        "Edge Detect": np.array(
            [
                [-1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1],
                [-1, -1, 24, -1, -1],
                [-1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1],
            ],
            dtype=float,
        ),
        "Emboss": np.array(
            [
                [-2, -1, -1, 0, 0],
                [-1, -1, 0, 1, 0],
                [-1, 0, 1, 0, 1],
                [0, -1, 0, 1, 1],
                [0, 0, 1, 1, 2],
            ],
            dtype=float,
        ),
        "Sobel X": np.array(
            [
                [-1, -2, 0, 2, 1],
                [-4, -8, 0, 8, 4],
                [-6, -12, 0, 12, 6],
                [-4, -8, 0, 8, 4],
                [-1, -2, 0, 2, 1],
            ],
            dtype=float,
        ),
        "Sobel Y": np.array(
            [
                [-1, -4, -6, -4, -1],
                [-2, -8, -12, -8, -2],
                [0, 0, 0, 0, 0],
                [2, 8, 12, 8, 2],
                [1, 4, 6, 4, 1],
            ],
            dtype=float,
        ),
    }

    kernels = {"3x3": kernels_3x3, "5x5": kernels_5x5}
    return (kernels,)


@app.cell
def _(mo):
    kernel_size_dropdown = mo.ui.dropdown(
        options=["3x3", "5x5"],
        value="3x3",
        label="Kernel size",
    )
    return (kernel_size_dropdown,)


@app.cell
def _(kernel_size_dropdown, kernels, mo):
    kernel_dropdown = mo.ui.dropdown(
        options=list(kernels[kernel_size_dropdown.value].keys()),
        value="Identity",
        label="Kernel preset",
    )
    return (kernel_dropdown,)


@app.cell
def _(kernel_dropdown, kernel_size_dropdown, kernels, mo):
    selected_kernel = kernels[kernel_size_dropdown.value][kernel_dropdown.value]
    kernel_matrix = mo.ui.matrix(
        selected_kernel.tolist(),
        min_value=-50,
        max_value=50,
        step=0.25,
        precision=2,
        label=f"**{kernel_dropdown.value}** kernel",
    )
    return (kernel_matrix,)


@app.cell
def _(color, data, image_dropdown, img_rgb):
    loaders = {
        "Astronaut": lambda: color.rgb2gray(data.astronaut()),
        "Camera": lambda: data.camera() / 255.0,
        "Coins": lambda: data.coins() / 255.0,
        "Cat": lambda: color.rgb2gray(data.cat()),
        "Coffee": lambda: color.rgb2gray(data.coffee()),
        "PARA": lambda: color.rgb2gray(img_rgb)
    }


    loader = loaders.get(image_dropdown.value, loaders["Astronaut"])
    gray_image = loader()
    return (gray_image,)


@app.cell
def _(mo):
    image_options = ["Astronaut", "Camera", "Coins", "Cat", "Coffee", "PARA"]
    image_dropdown = mo.ui.dropdown(
        options=image_options,
        value="Astronaut",
        label="Image",
    )

    return (image_dropdown,)


@app.cell
def _(image_dropdown, url_input):
    controls = [image_dropdown]
    if image_dropdown.value == "Custom URL":
        controls.append(url_input)
    return (controls,)


@app.cell
def _(convolve2d, gray_image, kernel_matrix, np, plt):
    kernel = np.array(kernel_matrix.value)
    convolved = convolve2d(gray_image, kernel, mode="same", boundary="symm")
    convolved_clipped = np.clip(convolved, 0, 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 7))
    ax1.imshow(gray_image, cmap="gray", vmin=0, vmax=1)
    ax1.set_title("Original")
    ax1.axis("off")
    ax2.imshow(convolved_clipped, cmap="gray", vmin=0, vmax=1)
    ax2.set_title("Convolved")
    ax2.axis("off")
    plt.tight_layout()
    return (fig,)


@app.cell
def _(controls, fig, kernel_dropdown, kernel_matrix, kernel_size_dropdown, mo):
    mo.vstack(
        [mo.md('## Presets'), 
         mo.hstack([kernel_size_dropdown, kernel_dropdown] + controls), 
         mo.md('<br>'), 
         mo.md('## Effect of the Kernel'), 
         mo.hstack([kernel_matrix, 
                    mo.hstack([fig])])])
    return


@app.cell
def _(cv2, img_1, np, plt):
    kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(img_1, ddepth=-1, kernel=kernel_sharpen)
    fig_12, _axes = plt.subplots(1, 2, figsize=(10, 5))
    _axes[0].imshow(img_1)
    _axes[0].set_title('Original')
    _axes[1].imshow(sharpened)
    _axes[1].set_title('cv2.filter2D + kernel de nitidez')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(cv2, img_1, plt):
    sigmas = [1, 3, 8]
    fig_13, _axes = plt.subplots(1, len(sigmas) + 1, figsize=(16, 4))
    _axes[0].imshow(img_1)
    _axes[0].set_title('Original (sigma=0)')
    for _ax, sigma in zip(_axes[1:], sigmas):
        borrada = cv2.GaussianBlur(img_1, ksize=(0, 0), sigmaX=sigma)
        _ax.imshow(borrada)
        _ax.set_title(f'Gaussian blur, sigma={sigma}')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Borrando só um pedaço da imagem

    Até agora borramos a imagem **inteira**. Mas um kernel não sabe nada sobre "imagem inteira" ele só enxerga o array que você entrega pra ele. Se você entregar só um pedacinho (um slice do array), ele borra só aquele pedacinho. É exatamente assim que funciona o borrão de rosto/placa de carro que você vê no Google Street View: acha a região de interesse, aplica o blur só ali, e devolve pro lugar.

    Vamos fazer isso de verdade, com uma imagem aérea real, e de quebra, um motivo real pra fazer esse blur seletivo: **privacidade**. Imagens de drone/aéreas capturam gente e veículos sem querer, e blur seletivo é como se anonimiza isso antes de publicar.

    ### De onde vem a imagem: OpenAerialMap

    O [OpenAerialMap](https://openaerialmap.org/) (OAM) é um catálogo aberto de imagens aéreas/de drone. Vamos utilizar aqui uma API REST (`api.openaerialmap.org/meta`), através de requests.
    """)
    return


@app.cell
def _(requests):
    # bbox bem amplo cobrindo parte do Brasil (sudoeste do Pará)
    bbox_brasil = [-53, -11, -43, -1]
    _resp = requests.get('https://api.openaerialmap.org/meta', params={'bbox': ','.join(map(str, bbox_brasil)), 'limit': 5})
    resultados = _resp.json()['results']
    for _r in resultados:
        props = _r['properties']
        print(f"{_r['title']:15s} | gsd={props.get('resolution_in_meters', 0) * 100:.1f} cm | dimensões={props.get('dimensions')} | {_r['uuid']}")
    return (resultados,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Lendo só um pedaço, com rasterio

    `gb_voo13` é uma imagem de drone gigante com mais de 15.000 x 13.000 pixels (lembra do problema de RAM que vimos na aula de STAC?). De novo, vamos só acessar um pedacinho da image através `Window`, lemos só a região de interesse, direto da URL.

    Já procurei antes e sei que tem uma pessoa numa área de plantio, perto do pixel `(6320, 7020)`. Dessa forma, vamos ler uma janela de 500x500 pixels em volta desse ponto.
    """)
    return


@app.cell
def _(np, plt, resultados):
    import rasterio
    from rasterio.windows import Window

    oam_url = resultados[0]["uuid"]  # href direto do GeoTIFF no S3, sem precisar de STAC

    with rasterio.open(oam_url) as src:
        print("dimensões da imagem completa:", src.width, "x", src.height, f"({src.width * src.height / 1e6:.0f} milhões de pixels)")

        col_centro, row_centro = 6320, 7020
        janela = Window(col_centro - 250, row_centro - 250, 500, 500)
        aerea = src.read(window=janela)  # (bandas, linhas, colunas)
        aerea = np.transpose(aerea, (1, 2, 0))  # -> (linhas, colunas, bandas), formato que matplotlib espera

    print("shape do pedaço lido:", aerea.shape)

    plt.figure(figsize=(7, 7))
    plt.imshow(aerea)
    plt.title("Recorte da image")
    plt.axis("on")
    plt.show()
    return (aerea,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Aplicando o blur só na região da pessoa

    Para isso precisamos:
    1. Defina a caixa (linhas/colunas) que cobre a região sensível;
    2. Recorte só esse pedaço do array (`imagem[y0:y1, x0:x1]`);
    3. Aplique o Gaussian blur **só nesse recorte**;
    4. Reatribua o resultado de volta na mesma posição do array original.

    O resto da imagem nunca passa pelo kernel, apenas nossa região delimitada.
    """)
    return


@app.cell
def _(aerea, cv2, plt):
    y0, y1, x0, x1 = (170, 320, 130, 280)

    aerea_anonimizada = aerea.copy()

    regiao = aerea_anonimizada[y0:y1, x0:x1]
    regiao_borrada = cv2.GaussianBlur(regiao, ksize=(0, 0), sigmaX=15)
    aerea_anonimizada[y0:y1, x0:x1] = regiao_borrada
    fig_14, _axes = plt.subplots(1, 2, figsize=(12, 6))
    _axes[0].imshow(aerea)
    _axes[0].add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, edgecolor='red', linewidth=2))
    _axes[0].set_title('Original')
    _axes[1].imshow(aerea_anonimizada)
    _axes[1].set_title('Só a região da pessoa foi borrada')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return aerea_anonimizada, x0, x1, y0, y1


@app.cell
def _(aerea, aerea_anonimizada, plt, x0, x1, y0, y1):
    fig_15, _axes = plt.subplots(1, 2, figsize=(8, 4))
    _axes[0].imshow(aerea[y0:y1, x0:x1])
    _axes[0].set_title('Antes (de perto)')
    _axes[1].imshow(aerea_anonimizada[y0:y1, x0:x1])
    _axes[1].set_title('Depois (de perto)')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    print(f'pixels borrados: {(y1 - y0) * (x1 - x0)} de {aerea.shape[0] * aerea.shape[1]} ({(y1 - y0) * (x1 - x0) / (aerea.shape[0] * aerea.shape[1]) * 100:.1f}% da imagem)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Detecção de bordas

    Como vimos, o kernel nos dá a possibilidade de aplicarmos diferentes propriedades na imagem de uma forma muito simples e rápida. Com os kernel, conseguimos detectar bordas (edges). Existem dois kernels muito famosos que servem para detecção de bordas.

    ## Sobel

    Uma borda é, matematicamente, um lugar onde a intensidade muda **bruscamente**. O filtro de **Sobel** é um kernel que aproxima a derivada (o "gradiente") da imagem um pra detectar mudanças na horizontal, outro na vertical. Onde o gradiente é grande, tem borda.

    ## Canny

    O **Canny** é o detector de bordas mais usado na prática, ele faz Sobel só que com mais passos: (1) borra a imagem com Gaussian blur pra reduzir ruído, (2) calcula o gradiente (tipo Sobel), (3) afina as bordas pra ficarem com 1 pixel de largura, (4) usa dois limiares (um alto, um baixo) pra decidir o que é realmente borda.

    Por isso ele já "embute" a lição da seção anterior: **reduzir ruído com blur antes de procurar bordas** evita detectar um monte de bordas falsas (textura/ruído confundido com borda de verdade).
    """)
    return


@app.cell
def _(filters, gray_sk_1, plt):
    sobel_edges = filters.sobel(gray_sk_1)
    fig_16, _axes = plt.subplots(1, 2, figsize=(10, 5))
    _axes[0].imshow(gray_sk_1, cmap='gray')
    _axes[0].set_title('Escala de cinza')
    _axes[1].imshow(sobel_edges, cmap='gray')
    _axes[1].set_title('skimage.filters.sobel')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(cv2, gray_cv_1, plt):
    canny_sem_blur = cv2.Canny(gray_cv_1, threshold1=50, threshold2=150)
    gray_borrado = cv2.GaussianBlur(gray_cv_1, ksize=(0, 0), sigmaX=0.8)
    canny_com_blur = cv2.Canny(gray_borrado, threshold1=50, threshold2=150)
    fig_17, _axes = plt.subplots(1, 2, figsize=(10, 5))
    _axes[0].imshow(canny_sem_blur, cmap='gray')
    _axes[0].set_title(f'Canny sem blur ({(canny_sem_blur > 0).sum()} px de borda)')
    _axes[1].imshow(canny_com_blur, cmap='gray')
    _axes[1].set_title(f'Canny com blur antes (sigma=0.8) ({(canny_com_blur > 0).sum()} px de borda)')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Connected Component Analysis (CCA)

    Depois de transformar uma imagem em binária (preto/branco), o próximo passo natural seria compreender quantos objetos distintos existem e onde eles estão. Isso é o que a análise de componentes conectados faz, ela agrupa pixels brancos que se tocam num "blob" só, numerado.

    Isso é super útil em sensoriamento remoto, serve para por exemplo contar clareiras de desmatamento, identificar talhões agrícolas, isolar nuvens, contar edificações, etc.

    Vamos binarizar nossa imagem com **Otsu** (um método que escolhe o limiar de corte automaticamente, sem a gente precisar chutar um número) e rodar a CCA em cima.
    """)
    return


@app.cell
def _(cv2, gray_cv_1, plt):
    _, binary = cv2.threshold(gray_cv_1, 
                              0, 
                              255, 
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    num_labels, labels_im, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    print(f'componentes encontrados (sem contar o fundo): {num_labels - 1}')
    fig_18, _axes = plt.subplots(1, 3, figsize=(14, 5))
    _axes[0].imshow(gray_cv_1, cmap='gray')
    _axes[0].set_title('Escala de cinza')
    _axes[1].imshow(binary, cmap='gray')
    _axes[1].set_title('Binarizada (limiar de Otsu)')
    _axes[2].imshow(labels_im, cmap='nipy_spectral')
    _axes[2].set_title(f'{num_labels - 1} componentes (cada cor = 1 objeto)')
    for _ax in _axes:
        _ax.axis('off')
    plt.tight_layout()
    plt.show()
    return centroids, labels_im, num_labels, stats


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Repare que deu um número **enorme** de componentes. Muito provavelmente isso é textura/ruído virando "objetos" de 1-2 pixels, não objetos de verdade. Na prática, quase sempre filtramos por **área mínima** pra ficar só com os componentes relevantes.
    """)
    return


@app.cell
def _(centroids, cv2, gray_cv_1, labels_im, np, num_labels, plt, stats):
    area_minima = 50 # pelo menos 50 pixels compoem um objeto

    labels_limpo = labels_im.copy()
    for rotulo in range(1, num_labels):
        if stats[rotulo, cv2.CC_STAT_AREA] < area_minima:
            labels_limpo[labels_limpo == rotulo] = 0

        
    componentes_validos = [r for r in range(1, num_labels) if stats[r, cv2.CC_STAT_AREA] >= area_minima]

    print(f'componentes antes do filtro: {num_labels - 1}  |  depois (área >= {area_minima}px): {len(componentes_validos)}')
    fig_19, _ax = plt.subplots(figsize=(8, 5))
    _ax.imshow(gray_cv_1, cmap='gray')
    _ax.imshow(np.ma.masked_where(labels_limpo == 0, labels_limpo), cmap='nipy_spectral', alpha=0.7)
    _ax.set_title(f'{len(componentes_validos)} componentes relevantes (área >= {area_minima} px)')
    _ax.axis('off')
    plt.show()
    maiores = sorted(componentes_validos, key=lambda r: stats[r, cv2.CC_STAT_AREA], reverse=True)[:5]
    for r in maiores:
        area = stats[r, cv2.CC_STAT_AREA]
        cx, cy = centroids[r]
        print(f'componente {r}: área={area}px, centro=({cx:.0f}, {cy:.0f})')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Pré-processamento para redes neurais

    Se você já viu (ou vai ver) uma rede neural convolucional (CNN) sendo treinada, a etapa de "preparar os dados" **é literalmente** um monte das operações que acabamos de fazer:

    | O que fizemos hoje | Por que aparece antes de treinar uma rede |
    |---|---|
    | Resize | Toda CNN espera uma entrada de tamanho **fixo** (ex: 224x224) |
    | Normalização de brilho/contraste | Pixels em `float32` entre `0` e `1` (ou padronizados) treinam muito melhor do que `uint8` cru |
    | Crop | "Random crop" é uma técnica de *data augmentation* — recorta pedaços aleatórios pra rede não decorar a posição exata dos objetos |
    | Blur / brilho / contraste | Também viram *augmentation*: aplicar blur, mudar brilho aleatoriamente, etc. durante o treino ensina a rede a ser robusta a essas variações |
    | Grayscale/canais | Algumas arquiteturas trabalham com 1 canal só, outras esperam sempre 3 — sempre confira o que seu modelo espera |

    Na prática, isso tudo já vem empacotado em bibliotecas como `torchvision.transforms`, `albumentations.
    """)
    return


@app.cell
def _(cv2, img_1, np):
    def preprocess_para_cnn(imagem_rgb, tamanho=224):
        """Resize + normalização, do jeito que uma CNN pré-treinada (ex: ResNet) costuma esperar."""
        redimensionada = cv2.resize(imagem_rgb, (tamanho, tamanho), 
                                    interpolation=cv2.INTER_AREA)
        tensor = redimensionada.astype('float32') / 255.0  # 0-255 -> 0.0-1.0
        media = np.array([0.485, 0.456, 0.406], dtype='float32')
        desvio = np.array([0.229, 0.224, 0.225], dtype='float32')  # médias/desvios do ImageNet EXTREMAMENTE bem comuns quando se usa um modelo pré-treinado nele
        tensor = (tensor - media) / desvio
        return tensor

    
    tensor_final = preprocess_para_cnn(img_1)
    print('shape final:', tensor_final.shape, '| dtype:', tensor_final.dtype)
    print('média por canal:', tensor_final.mean(axis=(0, 1)).round(3))
    print('min/max:', round(float(tensor_final.min()), 2), round(float(tensor_final.max()), 2))

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Referências

    - [scikit-image — Images are numpy arrays](https://scikit-image.org/docs/stable/user_guide/numpy_images.html)
    - [Data Carpentry — Blurring Images](https://datacarpentry.github.io/image-processing/06-blurring.html)
    - [Data Carpentry — Image processing with Python](https://datacarpentry.org/image-processing/)
    - [OpenCV — Image Filtering docs](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html)
    - [OpenCV — Canny Edge Detection](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
    - [scikit-image — Connected component labeling](https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_label.html)
    """)
    return


if __name__ == "__main__":
    app.run()
