etapas
1) como colocar um erro em um bloco do fpga especificando o erro em uma porta lógica    
2) analisar a profundiade dos circuitos logicos teste c1355

## Resumo dos artigos

### A Framework for Reliability Analysis of Combinational Circuits Using Approximate Bayesian Inference

* O artigo enfatiza o problema mostrando que a crescente demanda dos CMOS nanos enfrentam problemas de funcionamento devido ao aumento de erros dinâmicos. Esses erros são transitórios, ocorrem temporariamente e são difíceis de detectar por métodos tradicionais de teste. Assim, os modelos tradicionais de computação determinística se tornam inadequados, e é mais apropriado tratar esses circuitos como sistemas probabilísticos. O artigo propõe o uso de **Redes Bayesianas (BN)** como uma abordagem eficiente para modelar computação probabilística em nano-domínios.

* Já foram usados outros meios para modelar os erros:
* * matrizes de transferência probabilisticas;
* * campos aleatorios de markov.

* as Redes Bayesianas foram escolhidas porque, diferentemente dos modelos anteriores, conseguem capturar a natureza causal dos circuitos lógicos de forma eficiente, reduzindo a complexidade por meio da estrutura gráfica orientada (grafo acíclico dirigido). As Redes Bayesianas também permitem uma representação probabilística exata e minimalista.

* No modelo proposto, cada porta lógica é representada por uma tabela de probabilidade condicional (CPT), que descreve a probabilidade da saída ser um estado lógico específico, dado o estado dos sinais de entrada. A tabela de probabilidade de uma porta lógica ideal sem erros é derivada da tabela verdade, enquanto a tabela de uma porta sujeita a erros é obtida considerando a probabilidade de erro dependente da entrada.

* Para calcular a probabilidade de erro de um circuito, o artigo propõe uma abordagem em que são conectados dois modelos: um modelo ideal (sem erros) e um modelo com erros dinâmicos. Esses dois modelos são conectados através de comparadores na saída, e o resultado do comparador indica a presença de erro. A probabilidade do comparador estar no estado "1" representa a probabilidade de erro na saída do circuito.


## Quartus

## **1. Testes de Falhas do Tipo Stuck-At**
### Descrição:
As falhas do tipo **stuck-at** modelam situações em que uma linha do circuito está permanentemente presa em 0 (S-a-0) ou 1 (S-a-1).

### Implementação:
- Introduza falhas manuais no testbench:
  ```verilog
  // Simulação de stuck-at-0 na linha g1
  assign g1 = 0; // Linha presa em 0
  ```
- Use ATPG (Automated Test Pattern Generation) para gerar padrões de teste que detectem stuck-at.

### Utilização:
- Cobertura de falhas é avaliada para garantir que os testes detectam falhas em todas as linhas.

---

## **2. Injeção de Falhas por Curto-Circuito**
### Descrição:
Simula um curto-circuito entre duas linhas, o que pode levar a comportamentos indesejados.

### Implementação:
- Modifique a lógica no circuito:
  ```verilog
  assign g3 = g1; // Simula um curto entre g3 e g1
  ```
- Teste como isso afeta a saída do circuito.

### Utilização:
- Identifica linhas críticas onde curtos podem comprometer a funcionalidade.

---

## **3. Testes de Temporização (Delay Fault Testing)**
### Descrição:
Avalia atrasos na propagação dos sinais devido a problemas físicos ou cargas capacitivas elevadas.

### Implementação:
- Use um testbench para observar atrasos nas saídas:
  ```verilog
  initial begin
      x1 = 0; x2 = 1; #5; // Atraso de 5 unidades
      x1 = 1; x2 = 0; #20; // Atraso maior
  end
  ```
- Configure o simulador para analisar a propagação de sinais e medir tempos.

### Utilização:
- Detecta atrasos críticos que podem causar falhas no sincronismo.

---

## **4. Fault Injection por Multiplexação**
### Descrição:
Introduz falhas utilizando um multiplexador para alternar entre o comportamento correto e um com falha.

### Implementação:
- Adicione um multiplexador no circuito para injetar falhas:
  ```verilog
  assign g1 = sel ? ~(x1 & x3) : 0; // Injeta falha quando sel = 1
  ```
- Controle o seletor (`sel`) no testbench para ativar ou desativar a falha.

### Utilização:
- Permite explorar diferentes cenários de falhas em tempo de simulação.

---

## **5. Teste de Redundância (Fault Masking)**
### Descrição:
Avalia se falhas são mascaradas por redundância ou lógica de voto no circuito.

### Implementação:
- Simule circuitos com redundância (ex.: 2 de 3 votos):
  ```verilog
  assign output = (input1 & input2) | (input2 & input3) | (input1 & input3);
  ```
- Injete falhas em uma ou mais entradas para verificar se o circuito continua funcional.

### Utilização:
- Explora a resiliência do circuito a falhas múltiplas.

---

## **6. Fault Grading**
### Descrição:
Estatísticas são usadas para avaliar a eficácia dos padrões de teste em cobrir falhas.

### Implementação:
- Use ferramentas de ATPG para calcular a cobertura de falhas.
- Simule o circuito com vetores de teste e compare o número de falhas detectadas versus não detectadas.

---

## **7. Testes de Falhas Sequenciais**
### Descrição:
Para circuitos sequenciais, as falhas podem ocorrer nos flip-flops ou na lógica combinacional entre eles.

### Implementação:
- Transforme flip-flops em entradas/saídas pseudo-primárias.
- Gere padrões de teste específicos para estados internos.

---

### Comparação das Técnicas

| Técnica                    | Facilidade de Implementação | Cobertura de Falhas | Custo Computacional |
|----------------------------|----------------------------|---------------------|---------------------|
| Stuck-At Fault             | Alta                      | Boa                 | Baixo               |
| Curto-Circuito             | Média                     | Boa                 | Médio               |
| Temporização               | Média                     | Média               | Alto                |
| Multiplexação              | Alta                      | Boa                 | Médio               |
| Redundância                | Média                     | Média               | Médio               |
| Fault Grading              | Alta                      | Alta                | Alto                |
| Falhas Sequenciais         | Média                     | Alta                | Alto                |


