# Roteiro Completo de Apresentação (30 Minutos) - Grupo 4
## Projeto de Sistema de Controle para Servomecanismo

**Participantes:** Gabriel, Felipe, Cintia, Dierson, Guilherme, Nicolas.
**Tempo Estimado:** 30 Minutos.
**Estimativa por Seção:** ~4-5 min por apresentador.

---

### Slide 0: Capa / Introdução
**Apresentador:** Gabriel
**Tempo:** 2 min

*   **Abertura:**
    *   "Bom dia a todos. Nós somos o Grupo 4 e hoje vamos apresentar o desenvolvimento completo de um sistema de controle para um servomecanismo de posição."
    *   "Este projeto não é apenas teórico; nosso objetivo foi simular o desafio real de controlar um braço robótico ou uma antena de radar, onde precisão e velocidade são vitais."
*   **A Agenda:**
    *   "Nossa apresentação está dividida em 5 etapas: Modelagem, Controle Proporcional (o básico), Compensação de Erro (Lag), Compensação de Velocidade (Lead) e, finalmente, a Análise de Robustez e PID."

---

### Slide 1: Análise do Modelo (Matrizes)
**Apresentador:** Gabriel
**Tempo:** 3 min

*   **Contexto Matemático:**
    *   "Tudo começa pelo modelo. Estamos lidando com um motor DC controlado por armadura. A entrada é Tensão (Volts) e a saída é Posição (Radianos)."
    *   "Aqui temos a representação em **Espaço de Estados**. As variáveis de estado $x_1, x_2, x_3$ representam, fisicamente: posição, velocidade e corrente de armadura."
*   **O Desafio do Ganho:**
    *   "Gostaria de chamar a atenção para a Função de Transferência. O numerador é $1.2$, mas o termo independente do denominador é $12.540$. Isso nos dá um ganho estático natural na ordem de $10^{-4}$."
    *   "Isso significa que o motor é 'pesado' eletricamente. Para movê-lo, nosso controlador precisará injetar muito ganho. Isso será um tema recorrente na apresentação: a necessidade de ganhos altos ($K_p > 10.000$)."

### Slide 2: Mapa de Polos e Zeros
**Apresentador:** Gabriel
**Tempo:** 2 min

*   **Análise de Estabilidade:**
    *   "Olhando o mapa de polos, temos um cenário clássico de estabilidade marginal."
    *   "Temos um polo na origem ($s=0$). Isso classifica nosso sistema como **Tipo 1**. Na prática, isso é excelente para controle de posição, pois garante que, se aplicarmos um degrau de tensão, o motor vai girar (integrar a velocidade) indefinidamente."
    *   "Os outros polos são $s=-13.2$ (Mecânico) e $s=-950$ (Elétrico)."

### Slide 3: Validação Malha Aberta
**Apresentador:** Gabriel
**Tempo:** 1 min

*   **Visualização:**
    *   "A simulação do degrau em malha aberta confirma nossa análise. Aplicamos 1V e a posição cresce linearmente (Rampa). O sistema funciona, mas sem controle, ele não 'para' na posição desejada. Ele apenas gira."

### Slide 4: Interpretação Física
**Apresentador:** Gabriel
**Tempo:** 2 min

*   **Conexão com a Realidade:**
    *   "Antes de passar para o controle, vamos entender o que esses números significam no mundo real."
    *   "O polo em **-950** é a constante de tempo elétrica ($\tau = L/R$). É rapidíssimo, a corrente sobe quase instantaneamente."
    *   "O polo em **-13.2** é a constante de tempo mecânica ($\tau = J/B$). É a inércia do rotor."
    *   "Nosso desafio de controle será 'lutar' contra essa inércia mecânica para fazer o motor parar na posição certa rapidamente."

---

### Slide 5: Controlador Proporcional - Conceito
**Apresentador:** Felipe
**Tempo:** 3 min

*   **Lógica de Controle:**
    *   "Obrigado, Gabriel. Eu assumo agora a tarefa de fechar a malha. Começamos pelo clássico **Controlador Proporcional**."
    *   "A lógica é intuitiva: o erro é a diferença entre onde eu quero ir e onde estou. Se estou longe, aplico força máxima. Se estou perto, diminuo a força."
*   **Root Locus:**
    *   "Mas, na engenharia, intuição não basta. Olhando o Lugar das Raízes, vemos o comportamento dinâmico."
    *   "À medida que aumento o ganho $K$, os polos reais se encontram e 'sobem' para o plano complexo. Isso significa que, invariavelmente, um ganho alto vai causar oscilação (polos imaginários)."

### Slide 6: Resultados Proporcional
**Apresentador:** Felipe
**Tempo:** 3 min

*   **A "Parede" de Desempenho:**
    *   "Nós exploramos esse *trade-off* exaustivamente."
    *   "Com um ganho baixo ($K \approx 138$), o sistema não oscila, mas leva 'uma eternidade' para chegar na posição. É inaceitável para um robô."
    *   "Tivemos que ser agressivos. Subimos o ganho para **77.000**."
    *   "Conseguimos velocidade ($t_s = 0.6s$), mas pagamos o preço na oscilação ($M_p \approx 6\%$). Até aí, tudo bem."
*   **O Grande Problema:**
    *   "O verdadeiro problema apareceu quando testamos uma entrada de **Rampa** (seguimento de trajetória)."
    *   "O erro estacionário ficou em **13.5%**. Nosso requisito é **1%**. O Proporcional, por ser apenas um ganho constante, não tem 'memória' suficiente para corrigir esse erro acumulado. Precisamos de algo mais inteligente."

---

### Slide 7: Compensador Lag (Atraso) - Teoria
**Apresentador:** Dierson
**Tempo:** 3 min

*   **A Solução para o Erro:**
    *   "Bom dia. Como o Felipe demonstrou, temos um déficit de ganho em erro estacionário. Precisamos aumentar o ganho do sistema, mas *apenas* para sinais lentos (baixa frequência), sem afetar a estabilidade rápida que o Felipe conseguiu."
    *   "Para isso, utilizamos o **Compensador Lag (Atraso de Fase)**."
    *   "A ideia é introduzir um polo e um zero muito próximos da origem. Isso cria um ganho alto em DC (frequência zero), mas 'cancela' seu próprio efeito em altas frequências."

### Slide 8: Otimização de Parâmetros
**Apresentador:** Dierson
**Tempo:** 3 min

*   **Design Rigoroso:**
    *   "Matematicamente, definimos que precisávamos de um ganho extra de aproximadamente **10x** para baixar o erro de 13% para 1%."
    *   "Escolhi a relação $\beta = z/p = 10$."
    *   "Posicionei o zero em $-0.1$ e o polo em $-0.01$. Por que tão perto de zero? Para garantir que o ângulo de fase não fosse afetado na frequência de corte (cruzamento de ganho), o que preserva a margem de fase e a estabilidade."
    *   "O resultado: Erro de rampa caiu para **1.35%**. Missão quase cumprida."

### Slide 9: Análise Frequencial
**Apresentador:** Dierson
**Tempo:** 1 min

*   **Validação via Bode:**
    *   "O diagrama de Bode confirma nossa teoria. Vejam como a magnitude (linha sólida) sobe na esquerda (baixa frequência), mas se sobrepõe perfeitamente à curva original na direita. Isso é engenharia de precisão."

---

### Slide 10: Compensador Lead (Avanço) - Teoria
**Apresentador:** Cintia
**Tempo:** 3 min

*   **O Novo Gargalo:**
    *   "Olá a todos. O Dierson resolveu o erro, mas o Compensador Lag tem um efeito colateral: ele tende a deixar a resposta temporal um pouco 'arrastada'."
    *   "Meu foco foi: **Velocidade Pura**. Para isso, usei o **Compensador Lead**."
    *   "Diferente do Lag, o Lead 'adianta' a informação, injetando fase positiva. É como se o controlador previsse o futuro, reagindo à taxa de variação do erro."

### Slide 11: Estratégia de Cancelamento
**Apresentador:** Cintia
**Tempo:** 3 min

*   **Técnica de Cancelamento de Polos:**
    *   "Ao analisar a planta, identifiquei que o 'vilão' da lentidão era o polo mecânico do motor em $-13.2$."
    *   "Decidi usar uma estratégia clássica de controle: **Cancelamento de Polos**."
    *   "Projetei o Zero do meu compensador Lead exatamente em cima desse polo ($-13.2$). Isso anula a dinâmica lenta."
    *   "Em contrapartida, coloquei o polo do compensador lá longe, em $-150$. Isso nos dá uma largura de banda muito maior."

### Slide 12: Resultados Lead
**Apresentador:** Cintia
**Tempo:** 2 min

*   **Perfeição no Transiente:**
    *   "O resultado gráfico fala por si. Conseguimos um tempo de acomodação de **0.98s**."
    *   "Mas o mais impressionante não é a velocidade, é a qualidade. Tivemos **0% de Overshoot**. O braço robótico se move rápido e para *exatamente* no ponto, sem vibrar. É o comportamento ideal."

### Slide 13: Solução Integrada (Lead-Lag)
**Apresentador:** Cintia
**Tempo:** 1 min

*   **A "Jóia da Coroa":**
    *   "Para o projeto final, não escolhemos um ou outro. Somamos forças. O controlador **Lead-Lag** combina o erro quase zero do Dierson com a velocidade perfeita do meu Lead. Essa é a solução que recomendamos para implementação."

---

### Slide 14: Controlador PID
**Apresentadores:** Guilherme & Nicolas
**Tempo:** 4 min

*   **Abordagem Alternativa:**
    *   "Paralelamente ao design em frequência, desenvolvemos um controlador **PID** no domínio do tempo."
    *   "PIDs são o padrão da indústria, mas sintonizá-los é uma arte."
    *   "Usamos o método de Ziegler-Nichols como ponto de partida, mas ele resultou em um sistema muito oscilatório ($M_p > 60\%$) devido ao ganho ultra-elevado necessário."
*   **Refinamento Manual:**
    *   "Realizamos um ajuste fino manual. Reduzimos o ganho proporcional para $K_p=60.000$ e aumentamos significativamente a ação derivativa ($K_d=1.000$) para atuar como um 'freio' eletrônico."
    *   "O resultado foi um controlador extremamente robusto, capaz de zerar erros rapidamente graças à ação integral."

---

### Slide 15: Análise de Robustez
**Apresentador:** Nicolas
**Tempo:** 4 min

*   **Teste de Estresse:**
    *   "Na simulação tudo é perfeito. Mas no mundo real, motores esquentam, engrenagens desgastam e cargas mudam."
    *   "Criamos simuladores de 'Piores Casos':"
        *   "**Cenário Pesado:** Motor fraco ($K_m=0.8$) e muito atrito. O sistema tende a ficar lento."
        *   "**Cenário Agressivo:** Motor superpotente ($K_m=1.2$) e sem atrito. O sistema tende a oscilar violentamente."
*   **Análise Comparativa:**
    *   "Vejam os gráficos. O **Proporcional** (esquerda) falha catastroficamente no cenário Agressivo, entrando em instabilidade."
    *   "Já os nossos controladores finais, **Lead-Lag** e **PID**, mantiveram a estabilidade em todos os casos. O overshoot muda um pouco, mas o sistema nunca perde o controle. Isso prova a qualidade do nosso design de margem de fase."

---

### Slide 16: Comparativo Final (Tabela)
**Apresentador:** Nicolas
**Tempo:** 2 min

*   **Resumo Executivo:**
    *   "Na tabela final, fica claro:"
    *   "Se você quer simplicidade e baixo custo computacional: **Use o Proporcional** (mas aceite o erro)."
    *   "Se você quer o movimento mais suave possível: **Use o Lead**."
    *   "Se você precisa de robustez absoluta e erro zero sob qualquer carga: **Use o PID ou Lead-Lag**."

### Slide 17: Conclusão
**Apresentador:** Grupo (Todos)
**Tempo:** 1 min

*   **Fechamento:**
    *   "Concluímos que o objetivo foi atingido. O sistema proposto é estável, preciso ($e_{ss} \approx 0\%$) e rápido ($t_s < 1s$)."
    *   "Agradecemos a atenção. Estamos abertos a perguntas."


