# psim - pool simulator
Simulador de sinuca em Python com PyGame

## Como jogar
- Clique no botão verde "jogar";
- Controle a força do taco com as teclas W e S;
- Clique e arraste para controlar a direção do taco;
- Solte para bater o taco;

Você também pode pausar o jogo pressionando P e plotar alguns gráficos da simulação clicando em "Gráficos".

## Conceitos físicos
O simulador de sinuca utiliza diversas noções de cinemática e dinâmica para realizar os cálculos das trajetórias, colisões, transferências de momento, etc. Vejamos rapidamente algumas noções necessárias para compreender como a simulação funciona.

## Momento Linear
O momento linear, ou quantidade de movimento de um corpo é uma função da massa e da velocidade, sendo dado por $\vec{p} = m \cdot \vec{v}$. Onde:
  - $\vec{p}$ é o momento linear;
  - $m$  é a massa do corpo;
  - $\vec{v}$ é a velocidade do corpo.

Podemos tanto estudar um momento de um corpo, quanto o momento de um sistema de corpos. Essa quantidade se torna interessante quando estudamos sua conservação ou variação.

## Forças e Aceleração

Podemos entender a força como a variação do momento pelo tempo, ou seja:

$$
\begin{align}
  \vec{F} = \displaystyle\frac{d\vec{p}}{dt}
\end{align}
$$

onde:
- $\vec{F}$ é a força aplicada;
- $\vec{p}$ é a o momento linear, que está sendo derivado em função do tempo.

Isso já nos dá uma boa intuição: uma força externa altera o momento do sistema. Um bom exemplo de uma força seria a interação causada pelo taco de sinuca: a bola, geralmente parada, muda sua velocidade - e consequentemente seu momento linear - ao ser atingida com o taco. 

Resolvendo a derivada acima, temos - para massas constantes:

$$
\begin{align}
  \vec{F} = m \cdot \vec{a}
\end{align}
$$

onde:
- $\vec{F}$ é a força aplicada;
- $\vec{a}$ é a aceleração (variação de velocidade).

Uma força é uma interação que altera o vetor velocidade de um corpo e, dessa forma, pode ditar sua trajetória. De fato, existem chamadas equações diferenciais, que conseguem descrever trajetórias completamente utilizando as forças que atual em um corpo e suas condições iniciais. Uma equação diferencial não é nada mais que uma equação que envolve derivadas.

### Colisões e Transferência de Momento

Um sistema cheio de bolas a velocidade constante não varia sua quantidade de movimento e, portanto, não tem forças "externas" o influenciando.
Mas e se duas dessas bolas colidirem? 

Intuitivamente, imaginamos que as bolas mudam de direção, velocidade e, por fim, momento. Mas então houve alguma força agindo no sistema? 

A resposta é que sim. No curto intervalo da colisão, as bolas interagiram e alteraram o momento uma da outra. Se não houve nenhuma outra interação, podemos dizer que o momento final igual é igual ao momento inicial (o momento se conserva):

$$
\begin{align}
  \sum \vec{p}_{0} = \sum \vec{p}_f,
\end{align}
$$

Por outro lado, o momento das duas bolas mudou, o que implica que as variações de momento se anulam:

$$
\begin{align}
  m_1 (\vec{v_{1f}} - \vec{v_{1f}}) + m_2 (\vec{v_{2f}} - \vec{v_{2i}}) = 0
\end{align}
$$

## Energia
Já discutimos que forças podem descrever a trajetória de um corpo. Se você está familiar com cálculo, você pode pensar sobre o que acontece quando se integra uma força por uma trajetória, já que os dois tem uma relação bem próxima.

### Energia Cinética

Integrar uma força sobre a trajetória que ela descreve nos dá a Energia Cinética, que depende apenas da massa do corpo e do quadrado da sua velocidade.

$$
\begin{align}
  E_c = \displaystyle \frac{mv^2}{2}
\end{align}
$$

Se fizermos o mesmo para qualquer trajetórias, temos a noção de Trabalho - que podemos interpretar como um "custo" do movimento.

É possivel classificar as forças em conservativas e não conservativas: Forças conservativas dependem apenas do ponto inicial e final, ou seja, independem da trajetória.

Também  

## Físicas da sinuca

Para nosso sistema estamos considerando:
* Interação entre o taco e a bola
* Interação entre as bolas
* Interação entre as bolas e as paredes
* Atrito

## Interação entre as bolas e a parede

Essa é a parte mais simples: consideramos que o ângulo de incidência de uma bola com a parede é o mesmo ângulo com que ela é ricocheteada.

### Atrito

A primeira força que vamos considerar em nosso sistema é o atrito. Ela é importante porque sem ela as bolas nunca parariam de se mover quando acertadas
O Atrito faz com que o sistema se "comporte" sem acumular energia com as jogadas.

Adicionar o atrito tornou nosso sistema não conservativo, ou seja, se a bola viajar por caminhos diferentes, seu trabalho provavelmente irá mudar.

Podemos calcular o atrito da seguinte forma:

$$
\begin{align}
  \vec{F_{at}} = -\hat{v} \cdot |\mu m g|
\end{align}
$$

onde:
* $\mu $ é o coeficiente de atrito da superfície (a mesa)
* $m$ é a massa do objeto (a bola)
* $g$ é a constante gravitacional
* $\hat{v}$ é a direção do movimento, ou seja, o atrito é contrário ao movimento que fazemos.

Juntando as constantes, podemos escrever a seguinte EDO a partir disso:

$$
\begin{align}
m \ddot r &= -\hat{\dot r} \cdot mA_t  \\
                      \ddot r &= -A_t \hat{\dot r}
\end{align}
$$

Podemos então calcular a aceleração das nossas bolas sabendo a direção de seu movimento e com uma constante.

### Interação entre a bola e o taco

Essa interação é o que deixa as coisas interessantes: a presença do taco é o que introduz uma força externa para alterar o nosso sistema. O taco adiciona uma acelaração e velocidade à bola branca, o que aumenta o momento e a energia cinética do sistema.

Nosso modelo simplifica consideravelmente essa parte: Em vez de considerarmos que a bola acelera por um breve momento ao ser acertada, consideramos diretamente que ela adiquire uma velocidade inicial quando atingida respeitando a direção do taco.
Por mais que essa abordagem não seja realista, ela produz bons resultados e simplifica a implementação consideravelmente.


### Interação entre as bolas
A bola branca, após ser atingida pelo taco, pode acertar outra(s) bola(s). Supondo que acerte apenas uma, essa bola pode por vez acertar outra e assim por diante (até o atrito eventualmente dispersar toda a energia).

Vamos modelar a interação entre duas bolas:

Suponha que a bola branca chegue com uma velocidade $v_0$ em contato com a bola 8. Vamos definir:

* $ r_b $ como a posição da bola branca
* $ r_8 $ como a posição da bola 8
* $\vec{d}$ como a direção da bola 8 após a trajetória.
* $v_0$ é a velocidade da bola branca antes da colisão
* $ v_b $ como a velocidade da bola branca pós colisão
* $ v_8 $ como a velocidade da bola 8 pós colisão

Podemos modelar nossa colisão entre duas bolas considerando que a direção da bola 8 é mesma da diferença entre as posições dela e da bola branca:

$$
\begin{align} \vec{d} = \displaystyle \frac{r_b - r_8}{|r_b - r_8|}
\end{align}
$$

Considerando que as bolas tem a mesma massa e que a energia e o momento do sistema se quase não se altera por esse momento:

$$
\begin{align}
  m\vec{v_0} &= m\vec{v_b} + m\vec{v_8} \\
  \vec{v_0} &= \vec{v_b} + \vec{v_8}
\end{align}
$$

Sejam $E_{c_i}$ e $E_{c_f}$ as enegias inicial e final, vamos considerar também, que por esse breve momento da colisão, elas não mudam:

$$
\begin{align}
  E_{c_i} = E_{c_f}
\end{align}
$$

$$
\begin{align}
  m {v_0}^2 = m {v_b}^2 + m {v_8}^2
\end{align}
$$

$$
\begin{align}
  {v_0}^2 = {v_b}^2 + {v_8}^2
\end{align}
$$

Juntando essas informações, temos:

$$
\begin{align}
  {(v_b + v_8)}^2 = {v_b}^2 + {v_8}^2 \implies  \vec{v_b} \cdot \vec{v_8} = 0
\end{align}
$$

As velocidades após a velocidade são perpendiculares. Além disso, como já sabemos a direção da bola 8, sabemos a direção das duas bolas agora. As intensidades vêm quando realizamos a decomoposição do vetor $\vec{v_0}$ em $\vec{v_b}$ e $\vec{v_8}$, sendo o seno e cosseno do vetor.

Esse é um método possível para calcular as velocidades das bolas após a colisão. Na pŕatica, o método de Verlet exige diversas correções que acabam modificando o processo, no entanto. Decidimos discutir essa versão mais simples porque ela possibilita facilita o código com as correções.

Caso queira ver uma análise muito mais profunda, considerando fatores como rotação e deslizamento das bolas, o que foi escrito acima foi um resumo desse recurso:
* https://ekiefl.github.io/2020/04/24/pooltool-theory/

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

# Referências e links úteis
* https://ekiefl.github.io/2020/04/24/pooltool-theory/
* https://phet.colorado.edu/en/simulations/collision-lab
* https://en.wikipedia.org/wiki/Momentum
* https://en.wikipedia.org/wiki/Verlet_integration
* https://www.algorithm-archive.org/contents/verlet_integration/verlet_integration.html

Baseado nas notas de aula do professor Esmerindo.
