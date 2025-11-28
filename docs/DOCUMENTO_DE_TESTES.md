# 🧪 Documento de Testes - KetMaker

Este documento descreve o plano de testes, os casos de teste e os resultados esperados para a aplicação **KetMaker**.

## 1. Objetivo

O objetivo deste documento é garantir que o sistema **KetMaker** atenda aos requisitos funcionais e não-funcionais definidos, assegurando a correta simulação dos circuitos quânticos e a estabilidade da aplicação web.

## 2. Estratégia de Testes

A estratégia de testes será focada em **Testes Funcionais** (para verificar a correta simulação do circuito) e **Testes de Integração** (para garantir a comunicação entre Frontend e Backend).

| Tipo de Teste | Foco | Ferramentas |
| :--- | :--- | :--- |
| **Testes Unitários** | Funções de manipulação de Gates e lógica de simulação no `ketmaker.py`. | Python `unittest` (a ser implementado) |
| **Testes de Integração** | Comunicação API (`/api/process`) entre Frontend e Backend. | Python `requests` (a ser implementado) |
| **Testes de Aceitação (Manual)** | Interface do usuário (arrastar e soltar, visualização de resultados). | Navegador Web |

## 3. Casos de Teste Funcionais (Backend)

Os testes funcionais visam verificar a correta simulação de circuitos quânticos conhecidos.

### Caso de Teste 3.1: Qubit Simples (Gate X)

| ID | CT-001 |
| :--- | :--- |
| **Objetivo** | Verificar a aplicação correta do Gate X (NOT) em um qubit. |
| **Pré-condição** | Servidor Flask em execução. |
| **Passos** | 1. Enviar requisição POST para `/api/process` com 1 qubit no estado `|0⟩`. 2. Aplicar o Gate X. |
| **Requisição** | `{"qubits": {"q0": [0, 0]}, "gates": {"0": [{"type": "X", "qubit": "q0"}]}}` |
| **Resultado Esperado** | Estado final `|1⟩`. Resposta JSON com `state: {"|1>": "1.0"}` e `latex: "|1\\rangle"`. |

### Caso de Teste 3.2: Superposição (Gate H)

| ID | CT-002 |
| :--- | :--- |
| **Objetivo** | Verificar a criação de superposição com o Gate Hadamard (H). |
| **Pré-condição** | Servidor Flask em execução. |
| **Passos** | 1. Enviar requisição POST para `/api/process` com 1 qubit no estado `|0⟩`. 2. Aplicar o Gate H. |
| **Requisição** | `{"qubits": {"q0": [0, 0]}, "gates": {"0": [{"type": "H", "qubit": "q0"}]}}` |
| **Resultado Esperado** | Estado final de superposição `(|0⟩ + |1⟩) / √2`. Resposta JSON com `state: {"|0>": "0.7071067811865475", "|1>": "0.7071067811865475"}` e `latex: "\\frac{1}{\\sqrt{2}} \\left( |0\\rangle + |1\\rangle \\right)"`. |

### Caso de Teste 3.3: Estado de Bell (CNOT)

| ID | CT-003 |
| :--- | :--- |
| **Objetivo** | Verificar a criação do estado de Bell `(|00⟩ + |11⟩) / √2` (Emaranhamento). |
| **Pré-condição** | Servidor Flask em execução. |
| **Passos** | 1. Enviar requisição POST para `/api/process` com 2 qubits no estado `|00⟩`. 2. Aplicar Gate H no qubit 0. 3. Aplicar Gate CNOT (Control no qubit 0, Target no qubit 1). |
| **Requisição** | `{"qubits": {"q0": [0, 0], "q1": [0, 0]}, "gates": {"0": [{"type": "H", "qubit": "q0"}], "1": [{"type": "Control", "qubit": "q0"}, {"type": "Target", "qubit": "q1"}]}}` |
| **Resultado Esperado** | Estado final `(|00⟩ + |11⟩) / √2`. Resposta JSON com `state: {"|00>": "0.7071067811865475", "|11>": "0.7071067811865475"}` e `latex: "\\frac{1}{\\sqrt{2}} \\left( |00\\rangle + |11\\rangle \\right)"`. |

## 4. Casos de Teste de Aceitação (Frontend)

Estes testes devem ser executados manualmente no navegador.

| ID | CT-004 |
| :--- | :--- |
| **Objetivo** | Verificar a funcionalidade de arrastar e soltar Gates. |
| **Passos** | 1. Abrir `index.html` no navegador. 2. Arrastar o Gate 'H' da paleta para a primeira célula do Qubit 0. |
| **Resultado Esperado** | O Gate 'H' deve ser posicionado corretamente na célula. A célula deve aceitar o Gate. |

| ID | CT-005 |
| :--- | :--- |
| **Objetivo** | Verificar a execução do circuito e a exibição do resultado. |
| **Passos** | 1. Montar o circuito do Caso de Teste 3.2 (Gate H). 2. Clicar no botão "Run Circuit". |
| **Resultado Esperado** | A seção de resultados deve ser atualizada, exibindo o estado de superposição em formato de texto e LaTeX. |
