from galeshapley import algorithm

def test_match_comerciante_influenciador():
    comerciante_influenciador_pref = {
        'Cunha SA': ['Gildárcio', 'Shigemura', 'Henrique', 'Jean'], 
        'Vieira SA': ['Jean', 'Shigemura', 'Gildárcio', 'Henrique'], 
        'Lineu SA': ['Shigemura', 'Henrique', 'Gildárcio', 'Jean'], 
        'Loubach SA': ['Shigemura', 'Henrique', 'Gildárcio', 'Jean']
    }
    influenciador_comerciante_pref = {
        'Gildárcio': ['Cunha SA', 'Vieira SA', 'Lineu SA', 'Loubach SA'], 
        'Shigemura': ['Loubach SA', 'Lineu SA', 'Cunha SA', 'Vieira SA'], 
        'Henrique': ['Cunha SA', 'Loubach SA', 'Vieira SA', 'Lineu SA'], 
        'Jean': ['Vieira SA', 'Cunha SA', 'Loubach SA', 'Lineu SA']
    }

    pareamento = algorithm.match(
        A_pref = comerciante_influenciador_pref, 
        B_pref = influenciador_comerciante_pref
    )
    esperado = [('Loubach SA', 'Shigemura'), ('Cunha SA', 'Gildárcio'), ('Vieira SA', 'Jean'), ('Lineu SA', 'Henrique')]

    for obtido in pareamento:
        assert obtido in esperado, f'Resultado obtido "{obtido}" não existe na lista esperada "{esperado}"\n'

def test_match_produto_influenciador():
    produto_influenciador_pref = {
        'Armário': ['Gildárcio', 'Shigemura', 'Henrique', 'Jean'], 
        'Bolsa': ['Jean', 'Shigemura', 'Gildárcio', 'Henrique'], 
        'Camarão': ['Shigemura', 'Henrique', 'Gildárcio', 'Jean'], 
        'Dentadura': ['Shigemura', 'Henrique', 'Gildárcio', 'Jean']

    }
    influenciador_produto_pref = {
        'Gildárcio': ['Armário', 'Bolsa', 'Camarão', 'Dentadura'], 
        'Shigemura': ['Camarão', 'Armário', 'Bolsa', 'Dentadura'], 
        'Henrique': ['Armário', 'Dentadura', 'Camarão', 'Bolsa'], 
        'Jean': ['Bolsa', 'Camarão', 'Dentadura', 'Armário']    
    }

    pareamento = algorithm.match(
        A_pref = produto_influenciador_pref, 
        B_pref = influenciador_produto_pref
    )
    esperado = [('Armário', 'Gildárcio'), ('Camarão', 'Shigemura'), ('Bolsa', 'Jean'), ('Dentadura', 'Henrique')]

    for obtido in pareamento:
        assert obtido in esperado, f'Resultado obtido "{obtido}" não existe na lista esperada "{esperado}"\n'