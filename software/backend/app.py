from flask import Flask, jsonify, request
from flask_cors import CORS
from ket import *
from ketmaker import *

app = Flask(__name__)
CORS(app)

# Executar circuito aqui
@app.route('/api/process', methods=['POST'])
def processar_dados():
    # Flask captura o JSON enviado pelo Front
    dados = request.get_json()
    if not dados:
        return jsonify({"error": "Nenhum dado enviado!"}), 400
    
    # Processamento
    qubits = [v[1] for k,v in dados.get("qubits", {}).items()]
    gates = dados.get("gates", {})

    state = ketmaker(gates, qubits)
    state_formatado = {
        'state': {k: str(v) for k,v in state.get().items()},
        'latex': state.show(mode='latex').data
    }
    
    print(state_formatado)
    
    return jsonify(state_formatado)


if __name__ == "__main__":
    app.run(debug=True)