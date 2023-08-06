# Implementação de uma biblioteca para o algoritmo Gale-Shapley


## COMO USAR

Definir duas listas com elementos que serão pareados:

```python
    comerciantes = {'Cunha SA', 'Vieira SA', 'Lineu SA', 'Loubach SA'}
    influenciadores = {'Gildárcio', 'Shigemura', 'Henrique', 'Jean'}
```

Definir as preferências de cada elemento de cada lista relativas aos elementos da outra lista:

```python
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
```

Obter os melhores pares de acordo com o algoritmo:

```python
from galeshapley import algorithm

pareamento = algorithm.match(
    A = comerciantes,
    B = influenciadores,
    A_pref = comerciante_influenciador_pref,
    B_pref = influenciador_comerciante_pref
)
```

> Obs.: _O algoritmo de Gale-Shapley retorna uma das soluções ótimas possíveis_


## REFERÊNCIAS

1. Gale, David, and Lloyd S. Shapley. "College admissions and the stability of marriage." The American Mathematical Monthly 69.1 (1962): 9-15.