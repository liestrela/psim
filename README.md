# psim - pool simulator
Simulador de sinuca em Python com PyGame

## Como jogar
- Clique no botão verde "jogar";
- Controle a força do taco com as teclas W e S;
- Clique e arraste para controlar a direção do taco;
- Solte para bater o taco;

## Conceitos físicos
O simulador de sinuca utiliza diversas noções de cinemática e dinâmica para realizar os cálculos das trajetórias, colisões, transferências de momento, etc. Vejamos rapidamente algumas noções necessárias para compreender como a simulação funciona.

## Momento Linear
O momento linear, ou quantidade de movimento de um corpo é uma função da massa e da velocidade, sendo dado por $\vec{p} = m \cdot \vec{v}$. Onde:
  - $\vec{p}$ é o momento linear;
  - $m$  é a massa do corpo;
  - $\vec{v}$ é a velocidade do corpo.

Podemos tanto estudar um momento de um corpo quanto o momento de um sistema de corpos e, essa quantidade se torna interessante quando estudamos sua conservação ou variação.

## Forças e Aceleração

Podemos entender a força como a variação do momento pelo tempo, ou seja:

$\vec{F} = \displaystyle\frac{d\vec{p}}{dt}$

onde:
- $\vec{F}$ é a força aplicada;
- $\vec{p}$ é a o momento linear, que está sendo derivado em função do tempo.

Isso já nos dá uma boa intuição: uma força externa altera o momento do sistema. Um bom exemplo de uma força seria o próprio taco de sinuca: a bola, geralmente parada, muda sua velocidade - e consequentemente seu momento linear - ao ser atingida com o taco. 

Resolvendo a derivada acima, temos:

$\vec{F} = m \cdot \vec{a}$ (para massas constantes),

onde:
- $\vec{F}$ é a força aplicada;
- $\vec{a}$ é a aceleração (variação de velocidade).

Uma força é uma interação que altera o vetor velocidade de um corpo e, dessa forma, pode ditar sua trajetória. De fato, existem chamadas equações diferenciais, que conseguem descrever trajetórias completamente utilizando as forças que atual em um corpo e suas condições iniciais. Uma equação diferencial não é nada mais uma equação que envolve derivadas.

### Colisões e Transferência de Momento

Como a força descreve a variação da quantidade de movimento do sistema, podemos pensar no que acontece quando não há força.

Um sistema cheio de bolas a velocidade constante não varia sua quantidade de movimento e, portanto, não tem forças "externas" o influenciando.
Mas e se duas dessas bolas colidirem? 

Intuitivamente, imaginamos que as bolas mudam de direção, velocidade e, por fim, momento. Mas então houve alguma força agindo no sistema?

A resposta é que sim. No curto intervalo da colisão, as bolas interajiram e alteraram o momento uma da outra. Se não houve nenhuma outra interação, podemos dizer que o momento igual é igual ao momento inicial (o momento se conserva):

$\sum \vec{p}_{0} = \sum \vec{p}_1$,

Por outro lado, o momento das duas bolas mudou, o que implica que as variações de momento se anulam:

$m_1 (\vec{v_{1f}} - \vec{v_{1f}}) + m_2 (\vec{v_{2f}} - \vec{v_{2i}}) = 0$

### Colisões e Transferência de Momento
Já discutimos que forças podem descrever a trajetória de um corpo. Se você está familiar com calculo, você pode pensar sobre o que acontece quando se integra uma força por uma trajetória, já que os dois tem uma relação bem próxima.

De forma resumida, integrar uma força sobre a trajetória que ela descreve nos dá a Energia Cinética, que depende apenas da massa do corpo e do quadrado da sua velocidade.

Se fizermos o mesmo para qualquer trajetórias, temos a noção de Trabalho - um custo

Notamos também que é possivel classificar as forças em conservativas e não conservativas, quando elas são conservativas podemos definir a Energia Potencial.

Também poedmos dizer nesse caso que (Energia Mecanica)

## Integração de Verlet
Para calcular a posição das bolas na mesa a cada instante de simulação, utilizamos um método numérico para resolver equações que envolvem a posição e a aceleração atual de cada corpo. Este método consiste em aproximar o resultado da chamada "equação diferencial" da posição do corpo. Essa equação pode ser resolvida por meios analíticos, ou numéricos, que são rapidamente computáveis e dão resultados aproximados.

Utilizamos o método de integração de Verlet no nosso problema, cuja ideia consiste do seguinte:
Podemos aproximar a posição de um objeto em função das suas derivadas usando a Expansão de Taylor em torno de $t+\Delta t$:

$\vec{r}(t+\Delta t) = \vec{r}(t) + \vec{v}(t)\Delta t + \frac{1}{2}\vec{a}(t)\Delta t^2 + \frac{1}{6}\vec{b}(t)\Delta t^3 + \mathcal{O}(\Delta t^4)$.

Onde $v$, $a$, e $b$ são, resepctivamente, a primeira, segunda e terceira derivada da posição em relação ao tempo, e o termo $\mathcal{O}(\Delta t^4)$ é o termo de ordem $4$ restante da expansão de Taylor.

Obtendo agora, de maneira análoga, uma estimativa para a posição num tempo $t-\Delta t$, temos

$\vec{r}(t-\Delta t) = \vec{r} - \vec{v}(t)\Delta t + \frac{1}{2}\vec{a}(t)\Delta t^2 - \frac{1}{6}\vec{b}(t)\Delta t^3 + \mathcal{O}(\Delta t^4)$.

Resolvendo o sistema composto por estas duas equações para $\vec{r}(t+\Delta t)$, obtemos que

$\vec{r}(t+\Delta t) = 2\vec{r}(t)-\vec{r}(t-\Delta t)+\vec{a}\Delta t^2 + \mathcal{O}(\Delta t^4)$,

o que significa que podemos estimar a posição apenas sabendo a posição anterior, a posição atual e a aceleração, com um erro de ordem $4$.

Existem métodos alternativos ao Verlet para calcular os mesmos resultados, como por exemplo, o método de Euler. Porém, o Verlet é particularmente eficaz para nós porque ele evita o acúmulo de erros numéricos e não exige o cálculo explícito das velocidades, o que o torna ideal para simulações como a nossa.
