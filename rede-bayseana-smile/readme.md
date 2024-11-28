## 1. Introdução

### **O que são Redes Bayesianas?**

Redes Bayesianas são modelos gráficos probabilísticos que representam um conjunto de variáveis e suas dependências condicionais através de um **grafo direcionado acíclico (DAG)**. Cada nó no grafo representa uma variável, e as arestas direcionadas indicam relações de dependência entre essas variáveis.

### **Importância das Redes Bayesianas**

- **Modelagem de Incertezas**: Permitem a representação explícita de incertezas e como elas se relacionam.
- **Tomada de Decisão**: Ajudam na tomada de decisões informadas em cenários complexos.
- **Aprendizado de Máquina**: Utilizadas para inferência e aprendizado em sistemas de inteligência artificial.
- **Interpretação Intuitiva**: A estrutura gráfica facilita a compreensão das relações entre variáveis.

### **Aplicações Comuns**

- **Diagnóstico Médico**: Determinação de doenças com base em sintomas.
- **Detecção de Fraudes**: Identificação de transações financeiras suspeitas.
- **Sistemas de Recomendação**: Sugestão de produtos ou conteúdos personalizados.
- **Processamento de Linguagem Natural**: Modelagem de relações semânticas em textos.

---

## 2. Cálculo

### **Princípios Fundamentais de Probabilidade**

Para compreender redes Bayesianas, é essencial ter uma base sólida em probabilidade. Aqui estão os conceitos-chave:

- **Probabilidade Marginal**: Probabilidade de um evento ocorrer sem considerar outros eventos.
  
  $P(A) = \text{Probabilidade de } A \text{ ocorrer}$

- **Probabilidade Condicional**: Probabilidade de um evento ocorrer dado que outro evento já ocorreu.
  
  $P(A|B) = \frac{P(A \cap B)}{P(B)}$

- **Independência Estatística**: Dois eventos são independentes se a ocorrência de um não afeta a probabilidade do outro.
  
  
  $P(A \cap B) = P(A) \times P(B) \quad \text{se } A \text{ e } B \text{ forem independentes}$
  

### **Regra da Multiplicação**

Para eventos dependentes, a probabilidade conjunta é calculada pela multiplicação da probabilidade condicional pelo marginal.


$P(A \cap B) = P(A|B) \times P(B)$


### **Teorema de Bayes**

O Teorema de Bayes relaciona probabilidades condicionais e marginais, fornecendo uma forma de atualizar crenças com base em novas evidências.


$P(A|B) = \frac{P(B|A) \times P(A)}{P(B)}$


---

## 3. Aplicando a Regra de Bayes

### **Entendendo o Teorema de Bayes**

O Teorema de Bayes é fundamental para a inferência em redes Bayesianas. Ele permite atualizar a probabilidade de uma hipótese à luz de novas evidências.

### **Fórmula do Teorema de Bayes**

$P(H|E) = \frac{P(E|H) \times P(H)}{P(E)}$

Onde:
- P(H|E) é a probabilidade posterior da hipótese H dado a evidência E.
- P(E|H) é a probabilidade da evidência E dado que a hipótese H é verdadeira.
- P(H) é a probabilidade a priori da hipótese H.
- P(E) é a probabilidade marginal da evidência E.

### **Exemplo Prático**

**Problema**: Suponha que 1% da população tem uma certa doença H. Um teste para essa doença tem 99% de sensibilidade (P(T|H) = 0.99) e 95% de especificidade (P(-T|-H) = 0.95 ). Qual a probabilidade de uma pessoa ter a doença dado que o teste foi positivo ( P(H|T) )?

**Aplicação do Teorema de Bayes**:


$P(H|T) = \frac{P(T|H) \times P(H)}{P(T)}$


Calculando \( P(T) \):


$P(T) = P(T|H) \times P(H) + P(T|\neg H) \times P(\neg H) = 0.99 \times 0.01 + (1 - 0.95) \times 0.99 = 0.0099 + 0.0495 = 0.0594$

Então,


$P(H|T) = \frac{0.99 \times 0.01}{0.0594} \approx 0.1667 \text{ ou } 16.67\%$


**Interpretação**: Mesmo com um teste positivo, a probabilidade de realmente ter a doença é de aproximadamente 16.67%, devido à baixa prevalência da doença e à taxa de falsos positivos.

---

## 4. Redes Bayesianas

### **Componentes das Redes Bayesianas**

1. **Nós (Nodes)**: Representam variáveis aleatórias.
2. **Arestas (Edges)**: Indicam relações de dependência causal ou probabilística entre os nós.
3. **Tabelas de Probabilidade Condicional (CPTs)**: Associam probabilidades condicionais a cada nó com base em seus pais no grafo.

### **Grafo Direcionado Acíclico (DAG)**

A estrutura gráfica das redes Bayesianas é um DAG, onde:
- **Direcionamento**: As arestas têm direção, indicando a influência de um nó sobre outro.
- **Acilicidade**: Não há ciclos, ou seja, não é possível retornar ao mesmo nó seguindo as arestas.

### **Construindo uma Rede Bayesiana**

**Passo a Passo**:

1. **Identificação das Variáveis**: Determine quais variáveis são relevantes para o modelo.
2. **Definição das Relações de Dependência**: Estabeleça como as variáveis estão inter-relacionadas.
3. **Construção do Grafo**: Desenhe os nós e as arestas conforme as dependências.
4. **Definição das CPTs**: Para cada nó, defina a distribuição de probabilidade condicional com base nos seus pais.

### **Exemplo: Problema do Alarme para Ladrão e Terremoto**

Considere os seguintes nós:
- **Burglary (B)**: Verdadeiro ou Falso.
- **Earthquake (E)**: Verdadeiro ou Falso.
- **Alarm (A)**: Verdadeiro ou Falso.
- **JohnCalls (J)**: Verdadeiro ou Falso.
- **MaryCalls (M)**: Verdadeiro ou Falso.

**Estrutura do Grafo**:

- **B** e **E** são nós raiz, sem pais.
- **A** tem **B** e **E** como pais.
- **J** e **M** têm **A** como pai.

![Exemplo de Rede Bayesiana](https://i.imgur.com/QnUiqvH.png)

*(Imagem ilustrativa: Rede Bayesiana para o problema do Alarme)*

### **Tabelas de Probabilidade Condicional (CPTs)**

Para cada nó, as CPTs são definidas da seguinte forma:

- **Burglary (B)**:
  
  \[
  P(B=True) = 0.001 \quad P(B=False) = 0.999
  \]

- **Earthquake (E)**:
  
  \[
  P(E=True) = 0.002 \quad P(E=False) = 0.998
  \]

- **Alarm (A)**:
  
  \[
  \begin{array}{cc|c|c}
  B & E & P(A=True|B,E) & P(A=False|B,E) \\
  \hline
  True & True & 0.95 & 0.05 \\
  True & False & 0.94 & 0.06 \\
  False & True & 0.29 & 0.71 \\
  False & False & 0.001 & 0.999 \\
  \end{array}
  \]

- **JohnCalls (J)**:
  
  \[
  \begin{array}{c|c|c}
  A & P(J=True|A) & P(J=False|A) \\
  \hline
  True & 0.90 & 0.10 \\
  False & 0.05 & 0.95 \\
  \end{array}
  \]

- **MaryCalls (M)**:
  
  \[
  \begin{array}{c|c|c}
  A & P(M=True|A) & P(M=False|A) \\
  \hline
  True & 0.70 & 0.30 \\
  False & 0.01 & 0.99 \\
  \end{array}
  \]

---

## 5. Inferência nas Redes

### **O Que é Inferência?**

A inferência em redes Bayesianas refere-se ao processo de calcular probabilidades condicionais de um ou mais nós, dado um conjunto de evidências. Isso permite responder perguntas como "Qual a probabilidade de um alarme disparar dado que um ladrão foi detectado?"

### **Tipos de Inferência**

1. **Inferência Marginal**: Determina a probabilidade de uma única variável sem considerar outras variáveis.
   
   \[
   P(A) = \sum_{B} P(A, B)
   \]

2. **Inferência Condicional**: Calcula a probabilidade de uma variável dado o estado de outras variáveis.
   
   \[
   P(A|B) = \frac{P(A, B)}{P(B)}
   \]

3. **Inferência Total**: Considera todas as variáveis no modelo para responder a uma pergunta específica.

### **Métodos de Inferência**

1. **Eliminação de Variáveis (Variable Elimination)**
   
   - Método exato.
   - Elimina variáveis não relacionadas ao cálculo atual para simplificar a rede.
   - Passos:
     1. Identificar variáveis relevantes.
     2. Multiplicar as CPTs.
     3. Somar sobre as variáveis eliminadas.

2. **Propagação de Crenças (Belief Propagation)**
   
   - Pode ser exata ou aproximada.
   - Envolve passar mensagens entre os nós para atualizar as crenças sobre suas probabilidades.
   - Utilizada em redes com estruturas específicas, como árvores.

3. **Amostragem (Sampling)**
   
   - Método aproximado.
   - Inclui técnicas como **Monte Carlo** e **Amostragem de Gibbs**.
   - Gera amostras da distribuição conjunta para estimar as probabilidades condicionais.

4. **Algoritmos de Junção de Árvores (Junction Tree Algorithm)**
   
   - Método exato.
   - Transforma a rede em uma árvore de junção para facilitar cálculos complexos.
   - Eficaz para redes com alta conectividade.

### **Exemplo de Inferência**

**Pergunta**: Qual a probabilidade de haver um arrombamento (\( B=True \)) dado que o alarme disparou (\( A=True \))?

**Aplicação do Teorema de Bayes**:

\[
P(B=True | A=True) = \frac{P(A=True | B=True) \times P(B=True)}{P(A=True)}
\]

Calculando \( P(A=True) \):

\[
P(A=True) = P(A=True | B=True, E=True) \times P(B=True) \times P(E=True) + P(A=True | B=True, E=False) \times P(B=True) \times P(E=False) + P(A=True | B=False, E=True) \times P(B=False) \times P(E=True) + P(A=True | B=False, E=False) \times P(B=False) \times P(E=False)
\]

Substituindo os valores:

\[
P(A=True) = 0.95 \times 0.001 \times 0.002 + 0.94 \times 0.001 \times 0.998 + 0.29 \times 0.999 \times 0.002 + 0.001 \times 0.999 \times 0.998 \approx 0.001878
\]

Então,

\[
P(B=True | A=True) = \frac{0.95 \times 0.001}{0.001878} \approx 0.506 \text{ ou } 50.6\%
\]

**Interpretação**: Dado que o alarme disparou, a probabilidade de haver um arrombamento é de aproximadamente 50.6%.