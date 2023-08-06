from collections import deque

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