#!/usr/bin/env python3
"""
Módulo: circuito.py
Descrição:
  - Modelagem simples de circuitos digitais (classes para portas, entradas e wires).
  - Função tradutora que converte um netlist Verilog (ou BLIF com sintaxe similar) em um objeto Circuito.
    * Processa apenas o primeiro módulo encontrado no arquivo.
    * Suporta declarações simples de input, output e instâncias de portas (and, or, not).
    * A expressão regular aceita instâncias com ou sem nome explícito.
  - Função para gerar uma imagem do circuito (diagrama de blocos) utilizando Graphviz.  
"""

import re
from typing import List, Dict, Optional


class Gate:
    """
    Classe base para qualquer sinal ou porta lógica.
    Cada objeto possui um nome, uma lista de entradas e um método de avaliação.
    """
    def __init__(self, nome: str):
        self.nome = nome
        self.entradas: List['Gate'] = []
        self.valor: Optional[bool] = None

    def avaliar(self) -> bool:
        raise NotImplementedError("O método 'avaliar' deve ser implementado nas subclasses.")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.nome}>"

# abaixo estão as implementações das portas and, or e not (no futuro posso add mais portas, mas até então essas estão suprindo a necessidade)


class PortaAnd(Gate):
    def avaliar(self) -> bool:
        if not self.entradas:
            raise ValueError(f"A porta {self.nome} (AND) não possui entradas definidas.")
        self.valor = all(entrada.avaliar() for entrada in self.entradas)
        return self.valor

class PortaOr(Gate):
    def avaliar(self) -> bool:
        if not self.entradas:
            raise ValueError(f"A porta {self.nome} (OR) não possui entradas definidas.")
        self.valor = any(entrada.avaliar() for entrada in self.entradas)
        return self.valor

class PortaNot(Gate):
    def avaliar(self) -> bool:
        if len(self.entradas) != 1:
            raise ValueError(f"A porta {self.nome} (NOT) deve ter exatamente uma entrada.")
        self.valor = not self.entradas[0].avaliar()
        return self.valor

class Entrada(Gate):
    """
    representa uma entrada do circuito.
    """
    def __init__(self, nome: str, valor: Optional[bool] = None):
        super().__init__(nome)
        self.valor = valor

    def set_valor(self, valor: bool):
        self.valor = valor

    def avaliar(self) -> bool:
        if self.valor is None:
            raise ValueError(f"O valor da entrada {self.nome} não foi definido.")
        return self.valor

class Wire(Gate):
    """
    Representa um fio (net) intermediário.
    Geralmente criado como placeholder e depois associado a um driver (porta).
    """
    def __init__(self, nome: str):
        super().__init__(nome)
        self.driver: Optional[Gate] = None

    def set_driver(self, driver: Gate):
        self.driver = driver

    def avaliar(self) -> bool:
        if self.driver is None:
            raise ValueError(f"O wire {self.nome} não tem porta definido.")
        return self.driver.avaliar()

class Circuito:
    """
    Representa um circuito digital 
    """
    def __init__(self):
        self.portas: Dict[str, Gate] = {}
        self.entradas: List[str] = []  # Nomes dos sinais de entrada
        self.saidas: List[str] = []    # Nomes dos sinais de saída

    def adicionar_sinal(self, sinal: Gate):
        """
        Adiciona um sinal ao circuito.
        Se já existir um placeholder (Wire sem porta) com o mesmo nome, este é substituído.
        """
        if sinal.nome in self.portas:
            existente = self.portas[sinal.nome]
            if isinstance(existente, Wire) and existente.driver is None:
                self.portas[sinal.nome] = sinal
            else:
                return
        else:
            self.portas[sinal.nome] = sinal

    def conectar(self, origem: str, destino: str):
        """
        Conecta a saída do sinal 'origem' à entrada do sinal 'destino'.
        """
        if origem not in self.portas:
            raise KeyError(f"Sinal de origem '{origem}' não encontrado.")
        if destino not in self.portas:
            raise KeyError(f"Sinal de destino '{destino}' não encontrado.")
        self.portas[destino].entradas.append(self.portas[origem])

    def avaliar(self) -> Dict[str, bool]:
        """
        Avalia o circuito e retorna um dicionário com os valores lógicos dos sinais de saída.
        """
        resultados = {}
        for nome in self.saidas:
            resultados[nome] = self.portas[nome].avaliar()
        return resultados

    def desenhar(self, nome_arquivo: str = "circuito", max_size: str = "12,8"):
        try:
            from graphviz import Digraph
        except ImportError:
            print("Graphviz não está instalado. Instale com: pip install graphviz")
            return

        dot = Digraph(comment="Diagrama do Circuito", format="png")
        # Configura o layout horizontal e o tamanho máximo da imagem
        dot.attr(rankdir="LR", size=max_size, dpi="300")

        # Cria um subgrafo para as entradas (se definidas)
        with dot.subgraph(name="cluster_inputs") as c:
            c.attr(label="Entradas", color="lightblue")
            for nome in self.entradas:
                if nome in self.portas:
                    sinal = self.portas[nome]
                    label = f"{sinal.nome}\n({type(sinal).__name__})"
                    # Para entradas, usamos uma forma de caixa preenchida de azul claro
                    c.node(nome, label=label, shape="box", style="filled", fillcolor="lightblue")

        # Cria um subgrafo para as saídas (se definidas)
        with dot.subgraph(name="cluster_outputs") as c:
            c.attr(label="Saídas", color="lightgreen")
            for nome in self.saidas:
                if nome in self.portas:
                    sinal = self.portas[nome]
                    label = f"{sinal.nome}\n({type(sinal).__name__})"
                    # Para saídas, usamos uma forma de caixa preenchida de verde claro
                    c.node(nome, label=label, shape="box", style="filled", fillcolor="lightgreen")

        # Adiciona nós para os componentes que não são entradas nem saídas
        for nome, sinal in self.portas.items():
            if nome in self.entradas or nome in self.saidas:
                continue  # já foram adicionados nos subgráficos
            label = f"{sinal.nome}\n({type(sinal).__name__})"
            # Define a forma dos nós: usamos retângulo para portas lógicas e oval para wires
            if isinstance(sinal, Wire):
                shape = "oval"
            else:
                shape = "rectangle"
            dot.node(nome, label=label, shape=shape)

        # Adiciona as arestas para representar as conexões entre os nós
        for nome, sinal in self.portas.items():
            for entrada in sinal.entradas:
                dot.edge(entrada.nome, nome)

        # Renderiza e salva a imagem PNG
        dot.render('projeto/resultados/imagens_circuitos/'+nome_arquivo, view=True)
        print(f"Diagrama do circuito salvo como '{nome_arquivo}.png'.")

    def imprimir_circuito(self):
        print("=== CIRCUITO ===")
        print("Entradas:", self.entradas)
        print("Saídas:", self.saidas)
        print("Componentes:")
        for nome, componente in self.portas.items():
            entradas_nomes = [inp.nome for inp in componente.entradas]
            print(f" {nome} ({type(componente).__name__}): entradas -> {entradas_nomes}")
        print("================")


def carregar_verilog(file_path: str) -> Circuito:
    """
    netlist suportado:
    
      // Comentário
      module foobar(...);
         input A, B;
         output Y;
         not(i2, h1);
         and(j2, c1, g1);
         ...
      endmodule
    """
    circuito = Circuito()
    nets: Dict[str, Gate] = {}
    declared_inputs: List[str] = []
    declared_outputs: List[str] = []

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove comentários e espaços desnecessários
    clean_lines = []
    for line in lines:
        line = line.strip()
        if '//' in line:
            line = line.split('//')[0].strip()
        if line:
            clean_lines.append(line)

    # Processa apenas o primeiro módulo (entre "module" e "endmodule")
    in_module = False
    for line in clean_lines:
        if line.startswith("module"):
            in_module = True
            continue  # pula a linha de declaração do módulo
        if line.startswith("endmodule") and in_module:
            break  # encerra o processamento após o primeiro módulo
        if not in_module:
            continue

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

        # Processa instâncias de portas (suporta linhas com ou sem nome de instância)
        # Padrão: tipo [nome_instância] (sinal_saida, sinal1, sinal2, ...);
        m = re.match(r'^(\w+)(?:\s+(\w+))?\s*\((.*)\);$', line)
        if m:
            gate_type = m.group(1)
            instance_name = m.group(2)  # pode ser None
            port_list_str = m.group(3)
            ports_list = [p.strip() for p in port_list_str.split(',')]
            if len(ports_list) < 2:
                # Se houver menos de 2 sinais, não é uma instância válida para uma porta
                continue

            # Se o nome da instância não foi informado, define um nome padrão
            if instance_name is None:
                instance_name = f"{gate_type}_{ports_list[0]}"

            output_net = ports_list[0]
            input_nets = ports_list[1:]

            # Cria a instância da porta conforme o tipo suportado (and, or, not)
            gate_type_lower = gate_type.lower()
            if gate_type_lower == "and":
                gate_instance = PortaAnd(instance_name)
            elif gate_type_lower == "or":
                gate_instance = PortaOr(instance_name)
            elif gate_type_lower == "not":
                gate_instance = PortaNot(instance_name)
            else:
                # Se o tipo de porta não for suportado, ignora esta linha
                continue

            # Liga os sinais de entrada
            for net in input_nets:
                if net not in nets:
                    wire = Wire(net)
                    nets[net] = wire
                    circuito.adicionar_sinal(wire)
                gate_instance.entradas.append(nets[net])
            # Define a saída: se já existir um Wire, seta seu driver; senão, adiciona o sinal
            if output_net in nets:
                if isinstance(nets[output_net], Wire):
                    nets[output_net].set_driver(gate_instance)
                else:
                    continue
            else:
                nets[output_net] = gate_instance
                circuito.adicionar_sinal(gate_instance)
            continue
        continue

    circuito.portas = nets
    circuito.entradas = declared_inputs
    circuito.saidas = declared_outputs
    return circuito

if __name__ == "__main__":

    verilog_path = "projeto/testes/somador4bits.v"
    try:
        circuito = carregar_verilog(verilog_path)
        print("Circuito traduzido com sucesso!")
        print("Entradas:", circuito.entradas)
        print("Saídas:", circuito.saidas)
    except Exception as e:
        print("Erro ao traduzir o Verilog:", e)
        exit(1)

    # definindo valores a um somador completo (pensando em fazer uma função para deixar menos repetitivo a main)

    circuito.portas["a0"].set_valor(True) # a0 = 1 // 1
    circuito.portas["a1"].set_valor(False) # a1 = 0 // 2
    circuito.portas["a2"].set_valor(True) # a2 = 0 // 4
    circuito.portas["a3"].set_valor(False) # a3 = 0 // 8
    circuito.portas["b0"].set_valor(True) # b0 = 1 // 1
    circuito.portas["b1"].set_valor(False) # b1 = 0 // 2
    circuito.portas["b2"].set_valor(True) # b2 = 0 // 4
    circuito.portas["b3"].set_valor(False) # b3 = 0 // 8
    circuito.portas["cin"].set_valor(True) # c = 0 // 1

    resultado = circuito.avaliar() # esperado: s1: True ; s2: True ; s3: False ; s4: True
    print(resultado)
    circuito.imprimir_circuito()
    circuito.desenhar()
