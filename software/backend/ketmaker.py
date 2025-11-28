from ket import *

# Mapeamento de strings para objetos Gate da biblioteca Ket
GATE_MAP = {
    'X': X,
    'Y': Y,
    'Z': Z,
    'H': H,
    'I': I
}

def aplicar_estado_inicial(circuit_gates: list, initial_qubits: list) -> list:
    """
    Ajusta o circuito para refletir o estado inicial dos qubits.
    Se um qubit começa em '1', insere um gate X (NOT) no início da sua linha.
    
    Args:
        circuit_gates: Lista de listas representando o circuito (portas por qubit e tempo).
        initial_qubits: Lista de strings ('0' ou '1') representando o estado inicial.
        
    Returns:
        A lista de gates do circuito ajustada.
    """
    for i in range(len(circuit_gates)):
        if initial_qubits[i] == '1':
            # Insere o gate X (NOT) no início da linha do qubit
            circuit_gates[i].insert(0, 'X')
        else:
            # Insere um gate vazio para manter o alinhamento temporal
            circuit_gates[i].insert(0, '')
    return circuit_gates

def converter_strings_para_gates(circuit_gates: list) -> list:
    """
    Converte as strings de portas lógicas em objetos Gate da biblioteca Ket.
    
    Args:
        circuit_gates: Lista de listas de strings de portas.
        
    Returns:
        Lista de listas de objetos Gate ou strings vazias.
    """
    converted_gates = []
    for qubit_line in circuit_gates:
        line = []
        for gate_str in qubit_line:
            # Usa o GATE_MAP para obter o objeto Gate, ou mantém a string vazia
            line.append(GATE_MAP.get(gate_str, ''))
        converted_gates.append(line)
    return converted_gates

def executar_circuito_quantico(circuit_gates: list, initial_qubits: list) -> State:
    """
    Executa a simulação do circuito quântico.
    
    Args:
        circuit_gates: Lista de listas de strings de portas.
        initial_qubits: Lista de strings ('0' ou '1') representando o estado inicial.
        
    Returns:
        O objeto State resultante da simulação.
    """
    # 1. Ajustar o circuito para o estado inicial
    if '1' in initial_qubits:
        circuit_gates = aplicar_estado_inicial(circuit_gates, initial_qubits)
        
    # 2. Converter strings para objetos Gate
    converted_gates = converter_strings_para_gates(circuit_gates)

    # 3. Alocar qubits e iniciar o processo
    process = Process()
    qubits = process.alloc(len(initial_qubits))

    # 4. Aplicar os gates sequencialmente
    # i é a progressão temporal (colunas)
    for i in range(len(converted_gates[0])): 
        # j é a ordenação vertical de qubits (linhas)
        for j in range(len(qubits)): 
            gate = converted_gates[j][i]
            if gate != '':
                # Aplica o gate ao qubit correspondente
                gate(qubits[j])
    
    # 5. Obter o estado final
    state = dump(qubits)
    return state
