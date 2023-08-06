from gale_shapley import algorithm

def test_match_comerciante_influenciador():
    comerciantes = {'Cunha SA', 'Vieira SA', 'Lineu SA', 'Loubach SA'}
    influenciadores = {'Gildárcio', 'Shigemura', 'Henrique', 'Jean'}

    comerciante_influenciador_pref = {
        'Cunha SA': ['Gildárcio', 'Shigemura', 'Henrique', 'Jean'], 
        'Vieira SA': ['Jean', 'Shigemura', 'Gildárcio', 'Henrique'], 
        'Lineu SA':['Shigemura', 'Henrique', 'Gildárcio', 'Jean'], 
        'Loubach SA':['Shigemura', 'Henrique', 'Gildárcio', 'Jean']
    }
    influenciador_comerciante_pref = {
        'Gildárcio': ['Cunha SA', 'Vieira SA', 'Lineu SA', 'Loubach SA'], 
        'Shigemura': ['Loubach SA', 'Lineu SA', 'Cunha SA', 'Vieira SA'], 
        'Henrique': ['Cunha SA', 'Loubach SA', 'Vieira SA', 'Lineu SA'], 
        'Jean': ['Vieira SA', 'Cunha SA', 'Loubach SA', 'Lineu SA']
    }

    pareamento = algorithm.match(A = comerciantes, B = influenciadores, A_pref = comerciante_influenciador_pref, B_pref = influenciador_comerciante_pref)
    resultado_esperado = [('Loubach SA', 'Shigemura'), ('Cunha SA', 'Gildárcio'), ('Vieira SA', 'Jean'), ('Lineu SA', 'Henrique')]
    print(F'Resultado {pareamento} não foi igual ao esperado {resultado_esperado}')

    for resultado in resultado_esperado:
        assert resultado in pareamento

def test_match_produto_influenciador():
    influenciadores = {'Gildárcio', 'Shigemura', 'Henrique', 'Jean'}
    produtos = {'Armário', 'Bolsa', 'Camarão', 'Dentadura'}

    produto_influenciador_pref = {
        'Armário': ['Gildárcio', 'Shigemura', 'Henrique', 'Jean'], 
        'Bolsa': ['Jean', 'Shigemura', 'Gildárcio', 'Henrique'], 
        'Camarão':['Shigemura', 'Henrique', 'Gildárcio', 'Jean'], 
        'Dentadura':['Shigemura', 'Henrique', 'Gildárcio', 'Jean']

    }
    influenciador_produto_pref = {
        'Gildárcio': ['Armário', 'Bolsa', 'Camarão', 'Dentadura'], 
        'Shigemura': ['Camarão', 'Armário', 'Bolsa', 'Dentadura'], 
        'Henrique': ['Armário', 'Dentadura', 'Camarão', 'Bolsa'], 
        'Jean': ['Bolsa', 'Camarão', 'Dentadura', 'Armário']    
    }

    pareamento = algorithm.match(A = produtos, B = influenciadores, A_pref = produto_influenciador_pref, B_pref = influenciador_produto_pref)
    resultado_esperado = [('Armário', 'Gildárcio'), ('Camarão', 'Shigemura'), ('Bolsa', 'Jean'), ('Dentadura', 'Henrique')]
    print(F'Resultado {pareamento} não foi igual ao esperado {resultado_esperado}')

    for resultado in resultado_esperado:
        assert resultado in pareamento