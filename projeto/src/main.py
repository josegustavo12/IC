# main.py
from .circuit_parser import Circuit
from .DAlgebra import D_Value

def set_primary_input_values(circuit, input_values):
    """
    Atribui valores aos pinos de entrada primária conforme o dicionário input_values.
    input_values: dicionário onde a chave é o nome do pino (ex.: "A0") e o valor é 0 ou 1.
    """
    for gate in circuit.primary_input_gates:
        if gate.outputpin in input_values:
            gate.value = D_Value.ONE if input_values[gate.outputpin] == 1 else D_Value.ZERO

def evaluate_gate_recursive(gate, visited=None):
    """
    Avalia recursivamente uma porta, garantindo que os sinais de entrada já foram avaliados.
    """
    if visited is None:
        visited = set()
    # Se a porta já foi avaliada, retorna seu valor
    if gate in visited:
        return gate.value
    # Se for porta de entrada, não há cálculo a ser feito
    if gate.type == "input_pin":
        visited.add(gate)
        return gate.value
    # Avalia recursivamente todas as portas de entrada
    for in_gate in gate.input_gates:
        evaluate_gate_recursive(in_gate, visited)
    # Agora, avalia a porta atual
    gate.evaluate()
    visited.add(gate)
    return gate.value

def evaluate_circuit_recursive(circuit):
    """
    Avalia o circuito iniciando pelas portas de saída.
    """
    for gate in circuit.gates.values():
        if gate.type == "output_pin":
            evaluate_gate_recursive(gate)

def get_input_vector(circuit):
    """
    Retorna um vetor dos valores das entradas primárias, ordenado alfabeticamente.
    """
    inputs = {gate.outputpin: gate.value for gate in circuit.primary_input_gates}
    ordered_keys = sorted(inputs.keys())
    return [inputs[k] for k in ordered_keys]

def get_output_vector(circuit):
    """
    Retorna um vetor dos valores das saídas primárias, ordenado alfabeticamente.
    """
    outputs = {}
    for gate in circuit.gates.values():
        if gate.type == "output_pin":
            outputs[gate.outputpin] = gate.value
    ordered_keys = sorted(outputs.keys())
    return [outputs[k] for k in ordered_keys]

def print_vector(label, vector):
    """
    Imprime um vetor com o rótulo fornecido.
    """
    vector_str = ", ".join(str(v).replace("D_Value.", "") for v in vector)
    print(f"{label}: [{vector_str}]")

def print_detailed_results(circuit, title):
    """
    Exibe os vetores de entrada e saída do circuito com um título.
    """
    print("===" + title + "===")
    input_vector = get_input_vector(circuit)
    output_vector = get_output_vector(circuit)
    print_vector("Vetor de Entrada", input_vector)
    print_vector("Vetor de Saída", output_vector)
    print()

if __name__ == "__main__":
    # Caminho para o arquivo bench (verifique se o arquivo está no local correto)
    bench_file = "somador4bits.bench"

    # Definição dos valores de entrada (por exemplo, A = 1010 e B = 0110)
    input_values = {
        "A0": 0, "A1": 0, "A2": 0, "A3": 1,
        "B0": 1, "B1": 0, "B2": 0, "B3": 0
    }

    # --- Teste SEM Falhas ---
    circuit_ok = Circuit(bench_file)
    set_primary_input_values(circuit_ok, input_values)
    evaluate_circuit_recursive(circuit_ok)
    print_detailed_results(circuit_ok, "Teste SEM Falhas")

    # --- Teste COM Falhas ---
    circuit_err = Circuit(bench_file)
    set_primary_input_values(circuit_err, input_values)
    evaluate_circuit_recursive(circuit_err)

    # Injeta uma falha na porta S1 (por exemplo, forçando o valor D)
    perturbed_gate_name = "S1"
    gate_to_perturb = circuit_err.gates.get(perturbed_gate_name)
    if gate_to_perturb:
        gate_to_perturb.faulty = True
        gate_to_perturb.fault_value = D_Value.D

    # Reavalia o circuito após injetar a falha
    evaluate_circuit_recursive(circuit_err)
    print_detailed_results(circuit_err, "Teste COM Falhas")
    if gate_to_perturb:
        print(f"Porta Perturbada: {gate_to_perturb.outputpin} ({gate_to_perturb.type})")
