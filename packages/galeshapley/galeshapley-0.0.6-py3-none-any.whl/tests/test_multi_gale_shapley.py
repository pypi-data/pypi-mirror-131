from galeshapley import algorithm

def test_match_comerciante_influenciador():
    influenciadores_pref = {
        'Gildárcio': ['Cunha SA', 'Vieira SA', 'Lineu SA', 'Loubach SA'],
        'Shigemura': ['Vieira SA', 'Lineu SA', 'Loubach SA', 'Cunha SA'],
        'Henrique': ['Lineu SA', 'Loubach SA', 'Cunha SA', 'Vieira SA'],
        'Jean': ['Lineu SA', 'Vieira SA', 'Loubach SA', 'Cunha SA'],
        'Vinicius': ['Lineu SA', 'Vieira SA', 'Cunha SA', 'Loubach SA'],
        'Bresley': ['Vieira SA', 'Cunha SA', 'Lineu SA', 'Loubach SA'],
        'Marcos': ['Cunha SA', 'Vieira SA', 'Lineu SA', 'Loubach SA'],
        'Antonio': ['Lineu SA', 'Cunha SA', 'Vieira SA', 'Loubach SA']
    }
    comerciantes_pref = {
        'Cunha SA': ['Shigemura', 'Henrique', 'Jean', 'Gildárcio', 'Antonio', 'Marcos', 'Vinicius', 'Bresley'],
        'Vieira SA': ['Vinicius', 'Marcos', 'Bresley', 'Henrique', 'Gildárcio', 'Shigemura', 'Jean', 'Antonio'],
        'Lineu SA': ['Shigemura', 'Jean', 'Gildárcio', 'Henrique', 'Vinicius', 'Antonio', 'Bresley', 'Marcos'],
        'Loubach SA': ['Bresley', 'Marcos', 'Antonio', 'Vinicius', 'Jean', 'Gildárcio', 'Shigemura', 'Henrique']
    }
    comerciantes_restricoes = {
        'Cunha SA': 3,
        'Vieira SA': 2,
        'Lineu SA': 1,
        'Loubach SA': 1
    }

    pareamento = algorithm.multipleMatch(
        A_pref = influenciadores_pref,
        B_pref = comerciantes_pref,
        B_restricoes = comerciantes_restricoes
    )
    esperado = [
        ('Cunha SA', 'Gildárcio'),
        ('Cunha SA', 'Henrique'),
        ('Cunha SA', 'Jean'),
        ('Lineu SA', 'Shigemura'),
        ('Vieira SA', 'Vinicius'),
        ('Vieira SA', 'Marcos'),
        ('Loubach SA', 'Bresley'),
        (None, 'Antonio')
    ]

    for obtido in pareamento:
        assert obtido in esperado, f'Resultado obtido "{obtido}" não existe na lista esperada "{esperado}"\n'