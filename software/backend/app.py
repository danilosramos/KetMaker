from flask import Flask, jsonify, request
from flask_cors import CORS
from ketmaker import executar_circuito_quantico # Importa a função refatorada

app = Flask(__name__)
CORS(app)

@app.route('/api/process', methods=['POST'])
def processar_circuito():
    """
    Endpoint para receber a definição do circuito quântico e executar a simulação.
    """
    dados = request.get_json()
    
    if not dados:
        return jsonify({"error": "Nenhum dado de circuito enviado!"}), 400
    
    # Extração e validação dos dados
    try:
        # O frontend envia o estado inicial dos qubits como uma lista de '0' ou '1'
        initial_qubits = [v[1] for k, v in dados.get("qubits", {}).items()]
        
        # O frontend envia a estrutura do circuito (gates)
        circuit_gates = dados.get("gates", {})
        
        # O circuito é enviado como um dicionário onde a chave é a coluna (tempo)
        # e o valor é uma lista de gates. Precisamos reestruturar para 
        # uma lista de listas onde a linha é o qubit e a coluna é o tempo.
        
        # 1. Determinar o número de qubits e o número de colunas (tempo)
        num_qubits = len(initial_qubits)
        num_cols = max(map(int, circuit_gates.keys())) + 1 if circuit_gates else 0
        
        # 2. Inicializar a matriz de gates (qubit x tempo)
        # Preenche com strings vazias para manter o alinhamento
        gates_matrix = [['' for _ in range(num_cols)] for _ in range(num_qubits)]
        
        # 3. Preencher a matriz com os gates
        for col_index_str, gates_list in circuit_gates.items():
            col_index = int(col_index_str)
            for gate_data in gates_list:
                qubit_index = int(gate_data['qubit'].replace('q', ''))
                gate_type = gate_data['type']
                
                if 0 <= qubit_index < num_qubits and 0 <= col_index < num_cols:
                    gates_matrix[qubit_index][col_index] = gate_type
                
    except Exception as e:
        return jsonify({"error": f"Erro na estrutura dos dados: {str(e)}"}), 400

    # Execução da simulação
    try:
        state = executar_circuito_quantico(gates_matrix, initial_qubits)
        
        # Formatação da resposta
        state_formatado = {
            'state': {k: str(v) for k, v in state.get().items()},
            'latex': state.show(mode='latex').data
        }
        
        return jsonify(state_formatado)
        
    except Exception as e:
        # Captura erros durante a simulação (ex: gate inválido, erro de biblioteca)
        return jsonify({"error": f"Erro durante a simulação do circuito: {str(e)}"}), 500


if __name__ == "__main__":
    # O modo debug deve ser desativado em produção
    app.run(debug=True)
