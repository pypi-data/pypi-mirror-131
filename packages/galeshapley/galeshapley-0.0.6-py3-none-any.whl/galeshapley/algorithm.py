from collections import deque
import queue

def _pref_prioridade(pref):
    return {
        a: {b: idx for idx, b in enumerate(a_pref)}
        for a, a_pref in pref.items()
    }

def match(*, A_pref, B_pref):
    A = list(A_pref.keys())
    B = list(B_pref.keys())
    B_prioridade = _pref_prioridade(B_pref)
    lista_espera = {a: deque(bs) for a, bs in A_pref.items()}
    par = {}
    
    restante_A = set(A)
    while len(restante_A) > 0:
        a = restante_A.pop()
        b = lista_espera[a].popleft()
        if b not in par:
            par[b] = a
        else:
            a0 = par[b]
            b_prefer_a0 = B_prioridade[b][a0] < B_prioridade[b][a]
            if b_prefer_a0:
                restante_A.add(a)
            else:
                restante_A.add(a0)
                par[b] = a
    
    return [(a, b) for b, a in par.items()]

def multipleMatch(*, A_pref, B_pref, B_restricoes):
    A = list(A_pref.keys())
    B = list(B_pref.keys())
    apontador = {}
    A_prefDict = {}
    ABDict = {}
    pos_abertas = queue.Queue()

    for i in range(len(B)):
        # coloca todos A livres na fila
        for j in range(B_restricoes[B[i]]):
            pos_abertas.put(B[i])
        apontador[B[i]] = 0
    for i in range(len(A)):
        # Nenhum A ainda
        ABDict[A[i]] = None
        # Dicionário para pegar as preferências
        A_prefDict[A[i]] = {}
        for j in range(len(B)):
            # Salvar no dict uma lista para cada A que mapeia um B na posição preferida que ele está
            A_prefDict[A[i]][A_pref[A[i]][j]] = j
    # Loop de A que não achou um par ainda
    while not pos_abertas.empty():
        vaga = pos_abertas.get()
        # O próximo na lista de preferências de A
        B_preferencia = B_pref[vaga][apontador[vaga]]
        apontador[vaga] = apontador[vaga] + 1
        # Já foi dado o espaço em B?
        ocupado = ABDict[B_preferencia]
        if ocupado != None:
            # B prefere este A?
            posicao_atual = A_prefDict[B_preferencia][ocupado]
            posicao_proposta = A_prefDict[B_preferencia][vaga]
            if posicao_atual > posicao_proposta:
                # O A atual é mais cotado para B, então troca
                pos_abertas.put(ocupado)
                ABDict[B_preferencia] = vaga
            else:
                # O A atual não é o mais cotado, então coloca de volta na fila
                pos_abertas.put(vaga)
        else:
            # Não foi escolhido ainda - faz um par por enquanto
            ABDict[B_preferencia] = vaga

    # return ABDict
    return [(a, b) for b, a in ABDict.items()]