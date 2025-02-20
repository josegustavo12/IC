from .gate import Gate
import re # expressões regulares


class Circuit:

    index_id = 0 # atribuir valor unico aos ids

    def __init__(self, filename):
        """
        Inicializa um objeto Circuit com atributos padrão. O circuito é 
        representado por uma lista de portas (objetos Gate), uma lista de 
        portas de entrada primária, uma lista de portas de saída primária, um 
        dicionário de informações do circuito e um dicionário que mapeia 
        cada entrada primária para as portas correspondentes.

        Returns:
            None
        """
        # Dictionary of all gates in the circuit mapped to the ID of their output pins
        # This mapping is very useful for when searching for neighbouring gates
        self.gates = {}

        # List of all primary input gates
        self.primary_input_gates = []

        # List of all primary output gates
        self.primary_output_gates = []

        # Dictionary that maps each primary input to the corresponding gates
        self.get_gates_from_PI = {}

        # List of all faults in the circuit
        self.faults = []

        self.bench_file(filename) # le o arquivo e cria as portas
        # circuit.parse_fault_file(fault_file)
        self.generate_fault_vector() # gera o vetor de falhas 

        return

    def bench_file(self, filename): # Analisa um arquivo de texto que descreve um circuito e adiciona as portas ao circuito.

        with open(filename, "r") as file:
            lines = file.readlines()
    
            # usa o re para procurar as linhas com INPUT, OUTPUT e os gates
            input_pattern = re.compile(r"INPUT\(([\w_.\[\]0-9]+)\)")
            output_pattern = re.compile(r"OUTPUT\(([\w_.\[\]0-9]+)\)")
            gate_pattern = re.compile(r"([\w_.\[\]0-9]+) = (\w+)\(([\w_.\[\]0-9 ,]+)\)")

            for line in lines: # itera linha por linha
                line = line.strip()

                if line.startswith("#"): # retira todos os comentários
                    continue

                # procura as linhas de input e chama a função add_gate, onde nela coloca "input_pin" ou "output_pin" para se referir se é entrada ou saída 

                elif input_match := input_pattern.match(line):
                    self.add_gate("input_pin", [], str(input_match.group(1)).strip())

                elif output_match := output_pattern.match(line):
                    self.add_gate("output_pin",[str(output_match.group(1)).strip(),],"output_pin_" + str(output_match.group(1)).strip(),)


                # Extrai o ID de saída, o tipo da porta e suas entradas (dividindo a lista por vírgulas). Em seguida, adiciona a porta chamando add_gate.
                # Check if the line matches a gate pattern
                elif gate_match := gate_pattern.match(line):
                    # Extract the gate information
                    gate_output = str(gate_match.group(1)).strip()
                    gate_type = gate_match.group(2).strip()
                    gate_inputs = list(
                        map(lambda x: x.strip(), gate_match.group(3).split(","))
                    )
                    # Add the gate to the circuit
                    self.add_gate(gate_type, gate_inputs, gate_output)

        self.build_graph() # essa função constroi o grafo, para conectar as portas entre si formando a estrutura do grafo do circuito
        return

    def add_gate(self, type, inputs, output_pin_id):
        """
        Adiciona uma porta ao circuito. Recebe o tipo da porta, as entradas e o identificador do pino de saída.

        Args:
            type (str): The type of the gate.
            inputs (List[int]): The inputs of the gate.
            output (int): The output of the gate.

        Returns:
            None
        """

        # Create a new gate with the given parameters
        gate = Gate(self.index_id, type, inputs, output_pin_id)

        if type == "input_pin":
            self.primary_input_gates.append(gate)
        elif type == "output_pin":
            self.primary_output_gates.append(gate)

        # Add the gate to the dictionary of gates based on the output id
        self.gates[str(output_pin_id)] = gate

        self.index_id += 1 # incrementa +1 no id para garantir q n tenha 2 iguais
        return

    def build_graph(self):
        """
        Constrói a representação em grafo do circuito, conectando as portas com base nos pinos de entrada e saída.

        This function iterates over all the gates in the circuit and connects them based on their input pins.
        For each gate, it retrieves its input pins and clears the list of input gates.
        Then, for each input pin, it retrieves the corresponding gate from the circuit's dictionary of gates,
        and connects the current gate to it as an input gate.
        It also connects the previous gate to the current gate as an output gate.

        Returns:
            None
        """
        for current_gate in self.gates.values(): # percorre todas as portas dentro do dicionario self.gate
            # Get the input pins of the gate
            input_ids = current_gate.input_gates[:]
            # Clear the list of input gates
            current_gate.input_gates.clear()
            # Iterate over each input pin
            for input_id in input_ids:
                # Retrieve the corresponding previous gate from the circuit's dictionary of gates
                previous_gate = self.gates[input_id]
                # Connect the current gate to the previous gate as an input gate
                current_gate.input_gates.append(previous_gate)
                # Connect the previous gate to the current gate as an output gate
                previous_gate.output_gates.append(current_gate)

    def print_circuit(self):

        print("--------------------------- ---------------------------")
        for gate in self.gates.values():
            print(gate.outputpin)
            print(gate.type)
            print(gate.value)
            print()
        print("---------------------------")

    def parse_fault_file(self, fault_file):
        """
        Parses a fault file and stores the fault information in the circuit object.

        Args:
            fault_file (str): The path to the fault file.

        Returns:
            None
        """
        # Open the fault file
        with open(fault_file, "r") as file:
            # Read all the lines from the file
            lines = file.readlines()

            # Iterate through the lines two at a time
            for i in range(0, len(lines), 2):
                # Get the net name from the first line
                net_name = lines[i].strip()
                # Get the fault value from the second line and convert it to an integer
                fault_value = int(lines[i + 1].strip())
                # Append the net name and fault value to the circuit's faults list
                self.faults.append((net_name, fault_value))

        # Return None, as this function does not return anything
        return
    
    # Funções para o calculo do SCOAP

    """     
    CC0: Quantos “níveis” de entrada são necessários para forçar uma linha a 0.
    CC1: Quantos níveis são necessários para forçar uma linha a 1.
    CCb: Quantos níveis são necessários para observar uma determinada linha na saída. 
    """

    def calculate_SCOAP(self):
        self.calculate_SCOAP_controlability()
        self.reset_explored()
        self.calculate_SCOAP_observability()

    def calculate_SCOAP_controlability(self):
        for pi in self.primary_input_gates:
            self._SCOAP_controlability_recursive(pi)
        return

    def _SCOAP_controlability_recursive(self, gate):
        if gate.explored:
            return
        if any(not g.explored for g in gate.input_gates):
            return

        gate.calculate_CC0()
        gate.calculate_CC1()
        gate.explored = True

        for g in gate.output_gates:
            self._SCOAP_controlability_recursive(g)
        return

    def calculate_SCOAP_observability(self):
        for po in self.primary_output_gates:
            self._SCOAP_observability_recursive(po)
        return

    def _SCOAP_observability_recursive(self, gate):
        if gate.explored:
            return
        if any(not g.explored for g in gate.output_gates):
            return

        gate.calculate_CCb()
        gate.explored = True

        for g in gate.input_gates:
            self._SCOAP_observability_recursive(g)

        return

    def reset_explored(self):
        for gate in self.gates.values():
            gate.explored = False

        return

    def generate_fault_vector(self):
        """
        Generates a list of all possible faults in the circuit.

        A fault is a tuple containing the name of a gate's output pin and a value of either 0 or 1. For example, if the circuit has a gate with output pin 'a', the fault vector would include the tuples ('a', 0) and ('a', 1).

        The list of faults is stored in the 'faults' attribute of the Circuit object.

        Returns:
            None
        """
        # Iterate over all gates in the circuit
        for gate in self.gates.values():
            # For each gate, add two tuples to the fault vector: one with the gate's output pin and a value of 0, and one with the gate's output pin and a value of 1
            self.faults.append((gate.outputpin, 0))
            self.faults.append((gate.outputpin, 1))
        return