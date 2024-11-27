# Sinuca
Simulador de sinuca em Python com PyGame

## Como jogar
- Clique no botão verde "jogar";
- Controle a força do taco com as teclas W e S;
- Clique e arraste para controlar a direção do taco;
- Solte para bater o taco;

## Conceitos físicos
O simulador de sinuca utiliza diversas noções de cinemática e dinâmica para realizar os cálculos das
trajetórias, colisões, transferências de momento, etc. Vejamos rapidamente algumas noções necessárias para compreender como a simulação funciona.
- **Momento**: Descreve a quantidade de movimento de um corpo. É uma função da massa e da velocidade, sendo dado por $\vec{p} = m \cdot \vec{v}$. Onde:
  - $\vec{p}$ é o momento linear (um vetor);
  - $m$  é a massa do corpo;
  - $\vec{v}$ é a velocidade do corpo (um vetor).
- *adicionar mais noções básicas de física*

### Conservação do Momento
Em colisões elásticas (como na sinuca), o momento total do sistema é conservado, ou seja, a soma dos momentos de todas as bolas antes da colisão é igual à soma dos momentos após a colisão:

$\sum \vec{p}_0 = \sum \vec{p}_1$,

onde $\vec{p}_0$ é a velocidade antes da colisão, e $\vec{p}_1$ é a velocidade depois da colisão.

Esse princípio é utilizado para calcular as velocidades resultantes de cada bola após as colisões.

## Forças e Aceleração
Quando uma bola sofre uma colisão ou está sujeita ao atrito da mesa, uma força está sendo aplicada sobre ela. Segundo a Segunda Lei de Newton, a força resultante $\vec{F}$ é dada por:

$\vec{F} = m \cdot \vec{a}$ (para massas constantes),

onde:
- $\vec{F}$ é a força aplicada;
- $\vec{a}$ é a aceleração (variação de velocidade).

O atrito da mesa age contra o movimento das bolas, diminuindo suas velocidades ao longo do tempo até que parem completamente.

## Colisões e Transferência de Momento
Quando duas bolas colidem, elas trocam de momento entre si. O ângulo da colisão diz como o momento vai ser distribuído entre elas.

*explicar com mais detalhes*

## Integração de Verlet
Para calcular a posição das bolas na mesa a cada instante de simulação, utilizamos um método numérico para resolver equações que envolvem a posição e a aceleração atual de cada corpo. Este método consiste em aproximar o resultado da chamada "equação diferencial" da posição do corpo. Essa equação pode ser resolvida por meios analíticos, ou numéricos, que são rapidamente computáveis e dão resultados aproximados.

O método de integração de Verlet aplicado no nosso problema, consiste do seguinte:
A posição da bola em um instante $t + \Delta t$ é calculada com base em sua posição atual e passada, usando a fórmula:

$\vec{r}(t + \Delta t) = 2\vec{r}(t) - \vec{r}(t - \Delta t) + \vec{a}(t)(\Delta t)^2$,

onde:
- $\vec{r}(t)$ é a posição atual da bola;
- $\vec{r}(t - \Delta t)$ é a posição anterior da bola;
- $\vec{a}(t)$ é a aceleração atual;
- $\Delta t$ é o intervalo de tempo entre os cálculos.

Existem métodos alternativos ao Verlet para calcular os mesmos resultados, como por exemplo, o método de Euler. Porém, o Verlet é particularmente eficaz para nós porque ele evita o acúmulo de erros numéricos e não exige o cálculo explícito das velocidades, o que o torna ideal para simulações como a nossa.

*adicionar visualização do método de Verlet*
