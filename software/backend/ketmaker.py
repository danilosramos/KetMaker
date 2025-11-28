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
        'I': I
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
        for j in range(len(qubits)): # j é a ordenação vertical de qubits, j's de um mesmo i são simultâneos
            if portas[j][i] != '':
                portas[j][i](qubits[j])
    
    state = dump(qubits)
    return state