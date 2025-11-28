from ket import *

# As portas ainda são strings aqui
def not_inicial(portas, qubits):
    for i in range(len(portas)):
        if qubits[i] == '1':
            portas[i].insert(0, 'X')
        else:
            portas[i].insert(0, '')
    return portas

def transforma_portas(lista_strings):
    '''transforma uma lista de string em uma lista de portas'''
    dic = {
        'X': X,
        'Y': Y,
        'Z': Z,
        'H': H,
        'I': I,
        'Target': 'Target',
        'Control': 'Control'
    }
    lista_portas = []
    for l in lista_strings:
        lista = []
        for i in l:
            if i in dic.keys():
                lista.append(dic[i])
            else:
                lista.append('')
        lista_portas.append(lista)
    return lista_portas

def ketmaker(portas, qubits):
    #ex portas = [['H', 'X', ''],['', 'X', 'Z'],['', '', 'Z']] --> sem controle
    #ex qubits = ['0', '1', '0']
    if '1' in qubits:
        portas = not_inicial(portas, qubits)
    portas = transforma_portas(portas)

    process = Process()
    qubits = process.alloc(len(qubits))

    for i in range(len(portas[0])): # i é a progressão temporal
        cnot = {'target': [], 'control': []}
        for j in range(len(qubits)): # j é a ordenação vertical de qubits, j's de um mesmo i são simultâneos
            if portas[j][i] == '':
                continue
            # LÓGICA PARA CNOT/TOFFOLI
            elif portas[j][i] in ['Target', 'Control']:
                if portas[j][i] == 'Target':
                    cnot['target'].append(j)
                elif portas[j][i] == 'Control':
                    cnot['control'].append(j)
                if cnot['target'] and cnot['control']:
                    controls = cnot['control']
                    targets = cnot['target']

                    control = controls[0]
                    for i in range(1,len(controls)):
                        control = control + controls[i]

                    target = targets[0]
                    for i in range(1,len(targets)):
                        target = target + targets[i]

                    ctrl(qubits[control], X)(qubits[target])
            else:
                portas[j][i](qubits[j])
    
    state = dump(qubits)
    return state