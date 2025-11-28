# ⏳ Diagrama de Sequência UML - KetMaker

Este diagrama de sequência ilustra o fluxo de comunicação e a ordem das operações para a execução de um circuito quântico, desde a interação do usuário até a simulação no Backend.

```mermaid
sequenceDiagram
    actor Usuario
    participant Frontend as index.html (JS)
    participant Backend as app.py (Flask)
    participant Logic as ketmaker.py
    participant Simulator as Ket Library
    
    Usuario->>Frontend: 1. Monta o circuito (Arrastar/Soltar)
    Usuario->>Frontend: 2. Clica em "Run Circuit"
    
    Frontend->>Backend: 3. POST /api/process (JSON do Circuito)
    
    Backend->>Backend: 4. Valida e extrai dados do JSON
    
    Backend->>Logic: 5. executar_circuito_quantico(gates_matrix, initial_qubits)
    
    Logic->>Logic: 6. Ajusta para estado inicial (aplica Gate X se necessário)
    Logic->>Logic: 7. Converte strings de Gates para objetos Ket
    
    Logic->>Simulator: 8. process = Process()
    Logic->>Simulator: 9. qubits = process.alloc(n)
    
    loop Para cada coluna (tempo)
        Logic->>Simulator: 10. Aplica Gate(qubit)
    end
    
    Logic->>Simulator: 11. state = dump(qubits)
    
    Simulator-->>Logic: 12. Retorna objeto State
    
    Logic-->>Backend: 13. Retorna objeto State
    
    Backend->>Backend: 14. Formata State para JSON (state.get(), state.show(latex))
    
    Backend-->>Frontend: 15. Retorna JSON (Resultado da Simulação)
    
    Frontend->>Usuario: 16. Exibe o resultado (Texto e LaTeX)
```
