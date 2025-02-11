
# Módulo `circuito.py` – Documentação

Este módulo foi desenvolvido para modelar circuitos digitais com o objetivo de auxiliar na geração e verificação de vetores de teste (ATPG). Ele permite traduzir um netlist em formato Verilog (ou BLIF com sintaxe similar) para uma representação interna do circuito, possibilitando a avaliação, visualização gráfica e injeção de falhas.

## Índice

- [Visão Geral](#vis%C3%A3o-geral)
- [Estrutura do Código](#estrutura-do-c%C3%B3digo)
  - [1. Classes de Modelagem do Circuito](#1-classes-de-modelagem-do-circuito)
    - [a. Classe `Gate`](#a-classe-gate)
    - [b. Classes de Portas Lógicas (`PortaAnd`, `PortaOr`, `PortaNot`)](#b-classes-de-portas-l%C3%B3gicas-portaand-portaor-portanot)
    - [c. Classe `Entrada`](#c-classe-entrada)
    - [d. Classe `Wire`](#d-classe-wire)
    - [e. Classe `Circuito`](#e-classe-circuito)
  - [2. Função Tradutora (`traduzir_verilog`)](#2-fun%C3%A7%C3%A3o-tradutora-traduzir_verilog)
  - [3. Funções de Visualização e Impressão](#3-fun%C3%A7%C3%B5es-de-visualiza%C3%A7%C3%A3o-e-impress%C3%A3o)
    - [a. Função `desenhar`](#a-fun%C3%A7%C3%A3o-desenhar)
    - [b. Função `imprimir_circuito`](#b-fun%C3%A7%C3%A3o-imprimir_circuito)
- [Exemplo de Uso e Fluxo de Trabalho](#exemplo-de-uso-e-fluxo-de-trabalho)
- [Considerações sobre Nomenclatura](#considera%C3%A7%C3%B5es-sobre-nomenclatura)
- [Dependências e Execução](#depend%C3%AAncias-e-execu%C3%A7%C3%A3o)
- [Conclusão](#conclus%C3%A3o)

---

## Visão Geral

O módulo `circuito.py` possui as seguintes funcionalidades principais:

- **Modelagem de Componentes Digitais:** Define classes para representar cada componente do circuito (portas lógicas, entradas e wires).
- **Tradução de Netlist:** A função `traduzir_verilog` converte um netlist escrito em Verilog (ou BLIF) para um objeto do tipo `Circuito`, identificando entradas, saídas e instâncias de portas.
- **Visualização Gráfica:** A função `desenhar` gera um diagrama em formato PNG do circuito utilizando o Graphviz, com opções para limitar o tamanho da imagem.
- **Impressão Textual:** A função `imprimir_circuito` mostra, no console, uma visão simplificada do circuito, listando cada componente e suas conexões.
- **Exemplo de Injeção de Falhas:** O código demonstra como sobrescrever o método `avaliar` de um sinal para simular uma falha (por exemplo, um sinal “stuck-at‑0”).

---

## Estrutura do Código

### 1. Classes de Modelagem do Circuito

#### a. Classe `Gate`

A classe `Gate` é a base para todos os componentes do circuito. Ela define os atributos e métodos básicos que serão herdados pelas subclasses.

```python
class Gate:
    def __init__(self, nome: str):
        self.nome = nome
        self.entradas: List['Gate'] = []
        self.valor: Optional[bool] = None

    def avaliar(self) -> bool:
        raise NotImplementedError("O método 'avaliar' deve ser implementado nas subclasses.")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.nome}>"
```

**Explicação:**  
- **`nome`**: Identifica o sinal ou a porta.  
- **`entradas`**: Lista com as conexões (outros objetos `Gate`) que alimentam este componente.  
- **`valor`**: Armazena o resultado da avaliação lógica (True ou False).  
- O método `avaliar()` é abstrato e deverá ser implementado nas classes derivadas.

#### b. Classes de Portas Lógicas (`PortaAnd`, `PortaOr`, `PortaNot`)

Essas classes implementam a lógica específica de cada porta.

```python
class PortaAnd(Gate):
    def avaliar(self) -> bool:
        if not self.entradas:
            raise ValueError(f"A porta {self.nome} (AND) não possui entradas definidas.")
        self.valor = all(entrada.avaliar() for entrada in self.entradas)
        return self.valor
```

- **PortaAnd:**  
  Usa a função `all()` para retornar `True` se todas as entradas forem verdadeiras.

```python
class PortaOr(Gate):
    def avaliar(self) -> bool:
        if not self.entradas:
            raise ValueError(f"A porta {self.nome} (OR) não possui entradas definidas.")
        self.valor = any(entrada.avaliar() for entrada in self.entradas)
        return self.valor
```

- **PortaOr:**  
  Usa a função `any()` para retornar `True` se pelo menos uma entrada for verdadeira.

```python
class PortaNot(Gate):
    def avaliar(self) -> bool:
        if len(self.entradas) != 1:
            raise ValueError(f"A porta {self.nome} (NOT) deve ter exatamente uma entrada.")
        self.valor = not self.entradas[0].avaliar()
        return self.valor
```

- **PortaNot:**  
  Inverte o valor da única entrada. Se houver mais ou menos de uma entrada, lança um erro.

#### c. Classe `Entrada`

Representa uma entrada do circuito com valor definido externamente.

```python
class Entrada(Gate):
    def __init__(self, nome: str, valor: Optional[bool] = None):
        super().__init__(nome)
        self.valor = valor

    def set_valor(self, valor: bool):
        self.valor = valor

    def avaliar(self) -> bool:
        if self.valor is None:
            raise ValueError(f"O valor da entrada {self.nome} não foi definido.")
        return self.valor
```

**Exemplo de uso:**  
```python
entrada_a = Entrada("a")
entrada_a.set_valor(True)
```

#### d. Classe `Wire`

Utilizado como placeholder para sinais que serão definidos posteriormente por um driver (geralmente uma porta).

```python
class Wire(Gate):
    def __init__(self, nome: str):
        super().__init__(nome)
        self.driver: Optional[Gate] = None

    def set_driver(self, driver: Gate):
        self.driver = driver

    def avaliar(self) -> bool:
        if self.driver is None:
            raise ValueError(f"O wire {self.nome} não tem driver definido.")
        return self.driver.avaliar()
```

**Explicação:**  
Se um net não for declarado como entrada e for referenciado por uma instância de porta, um `Wire` é criado e, posteriormente, o driver é atribuído por meio de `set_driver()`.

#### e. Classe `Circuito`

Esta classe agrega todos os componentes (sinais) do circuito.

```python
class Circuito:
    def __init__(self):
        self.portas: Dict[str, Gate] = {}
        self.entradas: List[str] = []
        self.saidas: List[str] = []
```

**Métodos Importantes:**

- **`adicionar_sinal(sinal)`**  
  Adiciona um componente ao dicionário, usando seu nome como chave. Se houver um `Wire` sem driver, ele é substituído.
  
- **`conectar(origem, destino)`**  
  Adiciona uma conexão: o sinal identificado por `origem` é adicionado à lista de entradas do sinal `destino`.
  
- **`avaliar()`**  
  Percorre a lista de saídas e avalia cada uma, retornando um dicionário com os resultados.

- **`desenhar()`**  
  Gera um diagrama do circuito usando Graphviz (explicado na próxima seção).

- **`imprimir_circuito()`**  
  Imprime uma representação textual do circuito, listando cada componente e suas conexões.

---

### 2. Função Tradutora (`traduzir_verilog`)

Esta função lê um arquivo de netlist e constrói o objeto `Circuito`.

```python
def traduzir_verilog(file_path: str) -> Circuito:
    # Inicializa o objeto Circuito e estruturas auxiliares
    circuito = Circuito()
    nets: Dict[str, Gate] = {}
    declared_inputs: List[str] = []
    declared_outputs: List[str] = []

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Limpeza: remove comentários e espaços em branco
    clean_lines = []
    for line in lines:
        line = line.strip()
        if '//' in line:
            line = line.split('//')[0].strip()
        if line:
            clean_lines.append(line)

    # Processa somente o primeiro módulo (entre "module" e "endmodule")
    in_module = False
    for line in clean_lines:
        if line.startswith("module"):
            in_module = True
            continue
        if line.startswith("endmodule") and in_module:
            break
        if not in_module:
            continue

        # Processa inputs
        if line.startswith("input"):
            line = line.rstrip(';')
            parts = line.replace("input", "").strip()
            ports = [p.strip() for p in parts.split(',')]
            for port in ports:
                declared_inputs.append(port)
                entrada = Entrada(port)
                nets[port] = entrada
                circuito.adicionar_sinal(entrada)
            continue

        # Processa outputs
        if line.startswith("output"):
            line = line.rstrip(';')
            parts = line.replace("output", "").strip()
            ports = [p.strip() for p in parts.split(',')]
            for port in ports:
                declared_outputs.append(port)
                if port not in nets:
                    wire = Wire(port)
                    nets[port] = wire
                    circuito.adicionar_sinal(wire)
            continue

        # Processa instâncias de portas (suporta nome opcional)
        m = re.match(r'^(\w+)(?:\s+(\w+))?\s*\((.*)\);$', line)
        if m:
            gate_type = m.group(1)
            instance_name = m.group(2)  # pode ser None
            port_list_str = m.group(3)
            ports_list = [p.strip() for p in port_list_str.split(',')]
            if len(ports_list) < 2:
                continue

            # Se não houver nome, define um nome padrão (ou use o próprio net de saída)
            if instance_name is None:
                instance_name = ports_list[0]

            output_net = ports_list[0]
            input_nets = ports_list[1:]

            gate_type_lower = gate_type.lower()
            if gate_type_lower == "and":
                gate_instance = PortaAnd(instance_name)
            elif gate_type_lower == "or":
                gate_instance = PortaOr(instance_name)
            elif gate_type_lower == "not":
                gate_instance = PortaNot(instance_name)
            else:
                continue

            # Liga as entradas à instância
            for net in input_nets:
                if net not in nets:
                    wire = Wire(net)
                    nets[net] = wire
                    circuito.adicionar_sinal(wire)
                gate_instance.entradas.append(nets[net])
            # Define a saída: se já existir um Wire, seta o driver; senão, adiciona a instância
            if output_net in nets:
                if isinstance(nets[output_net], Wire):
                    nets[output_net].set_driver(gate_instance)
                else:
                    continue
            else:
                nets[output_net] = gate_instance
                circuito.adicionar_sinal(gate_instance)
            continue

    circuito.portas = nets
    circuito.entradas = declared_inputs
    circuito.saidas = declared_outputs
    return circuito
```

**Exemplo do Netlist Processado:**  
Se o arquivo contiver a linha  
```verilog
not(h2, v15);
```  
- O tradutor dividirá essa linha em:
  - `gate_type = "not"`
  - Como não há nome de instância explícito, definirá `instance_name = "h2"` (ou outro padrão, conforme ajuste).  
  - `ports_list = ["h2", "v15"]`  
- Em seguida, criará uma instância `PortaNot("h2")` e associará `v15` como entrada.  
- Essa instância será armazenada no dicionário com a chave `"h2"`.

---

### 3. Funções de Visualização e Impressão

#### a. Função `desenhar`

Gera um diagrama do circuito usando Graphviz. Para circuitos grandes, limita o tamanho da imagem.

```python
def desenhar(self, nome_arquivo: str = "circuito", max_size: str = "8,10"):
    try:
        from graphviz import Digraph
    except ImportError:
        print("Graphviz não está instalado. Instale com: pip install graphviz")
        return

    dot = Digraph(comment="Diagrama do Circuito", format="png")
    # Define atributos para limitar o tamanho e organizar o layout horizontal
    dot.attr(size=max_size, dpi="300", rankdir="LR")
    for nome, sinal in self.portas.items():
        label = f"{sinal.nome}\n({type(sinal).__name__})"
        shape = "box" if isinstance(sinal, Entrada) else "oval" if isinstance(sinal, Wire) else "rectangle"
        dot.node(nome, label=label, shape=shape)
    for nome, sinal in self.portas.items():
        for entrada in sinal.entradas:
            dot.edge(entrada.nome, nome)
    dot.render(nome_arquivo, view=True)
    print(f"Diagrama do circuito salvo como '{nome_arquivo}.png'.")
```

**Explicação:**  
- **`dot.attr(size=max_size, dpi="300", rankdir="LR")`:** Define o tamanho máximo da imagem, resolução (DPI) e organiza os nós da esquerda para a direita.  
- **Criação de nós:** Cada componente recebe um rótulo com seu nome e tipo, e um formato de forma adequado (caixa para entradas, oval para wires, retângulo para portas).  
- **Conexões:** São desenhadas arestas entre os nós, de acordo com as entradas de cada componente.

#### b. Função `imprimir_circuito`

Imprime uma visão textual do circuito.

```python
def imprimir_circuito(self):
    print("=== CIRCUITO ===")
    print("Entradas:", self.entradas)
    print("Saídas:", self.saidas)
    print("Componentes:")
    for nome, componente in self.portas.items():
        entradas_nomes = [inp.nome for inp in componente.entradas]
        print(f" {nome} ({type(componente).__name__}): entradas -> {entradas_nomes}")
    print("================")
```

**Exemplo de Saída:**  
```
=== CIRCUITO ===
Entradas: ['a', 'b', 'c']
Saídas: ['h2']
Componentes:
 h2 (PortaNot): entradas -> ['v15']
 v15 (Wire): entradas -> []
 a (Entrada): entradas -> []
 b (Entrada): entradas -> []
 c (Entrada): entradas -> []
================
```

Essa saída permite verificar se os sinais, conexões, entradas e saídas foram interpretados corretamente.

---

## Exemplo de Uso e Fluxo de Trabalho

No bloco `if __name__ == "__main__":` do código, o fluxo de trabalho é demonstrado:

1. **Tradução do Netlist:**  
   ```python
   verilog_path = "C880.blif"
   circuito = traduzir_verilog(verilog_path)
   print("Entradas:", circuito.entradas)
   print("Saídas:", circuito.saidas)
   ```
   O netlist é lido e um objeto `Circuito` é criado.

2. **Impressão do Circuito:**  
   ```python
   circuito.imprimir_circuito()
   ```
   Imprime a representação textual para depuração.

3. **Definição de Valores e Avaliação:**  
   Você pode definir valores para as entradas:
   ```python
   if "a" in circuito.portas and isinstance(circuito.portas["a"], Entrada):
       circuito.portas["a"].set_valor(True)
   ```
   Em seguida, o circuito é avaliado:
   ```python
   resultado = circuito.avaliar()
   print("Resultado da avaliação do circuito:", resultado)
   ```

4. **Geração do Diagrama:**  
   ```python
   circuito.desenhar("diagrama_circuito", max_size="8,10")
   ```
   Gera o arquivo `diagrama_circuito.png` com o diagrama.

5. **Injeção de Falha:**  
   Para simular uma falha, o método `avaliar` de um sinal pode ser sobrescrito:
   ```python
   if "i1" in circuito.portas:
       original_avaliar = circuito.portas["i1"].avaliar
       circuito.portas["i1"].avaliar = lambda: False
       print("Falha injetada: 'i1' ficou stuck-at-0.")
   ```
   Após isso, o circuito é reavaliado para verificar o efeito da falha.

---

## Considerações sobre Nomenclatura

No exemplo do netlist, se a linha for:
```verilog
not(h2, v15);
```
e não houver nome de instância, o tradutor define um nome padrão usando o primeiro net da lista. Por padrão, neste código ajustado, usamos:
```python
if instance_name is None:
    instance_name = ports_list[0]
```
Isso preserva o nome `h2` para a instância. Em versões anteriores, nomes concatenados (como `not_h2` ou `or_s15`) podiam ser gerados. Ajustar o tradutor para usar o próprio nome do net de saída ajuda a manter os nomes conforme o netlist original.

---

## Dependências e Execução

- **Python 3.x**
- **Pacote Python Graphviz:** Instale com `pip install graphviz`.
- **Graphviz Executáveis:** Baixe e instale a partir de [Graphviz Download](https://graphviz.org/download/). Certifique-se de adicionar o diretório `bin` ao PATH do sistema.

### Para Executar:

1. Prepare um arquivo de netlist (por exemplo, `C880.blif`) com os módulos necessários.
2. No terminal, execute:
   ```bash
   python circuito.py
   ```
3. O script traduz o netlist, imprime o circuito, gera o diagrama e demonstra a injeção de falhas.

---