
from timeit import default_timer as timer
from cyk import Cyk
from cyk_modificado import Cyk_modificado
import decimal

with open('input.txt') as f:
    palavras = f.read().splitlines()
for palavra in palavras:
    print("palavra: {}".format(palavra))

    cyk = Cyk()
    r_variaveis, r_terminais = cyk.ler_gramatica()
    start_cyk = timer()
    cyk.cyk(r_variaveis, r_terminais, palavra)
    end_cyk = timer()

    cyk_mod = Cyk_modificado()
    regras, inverse = cyk_mod.ler_gramatica()
    start_cyk_mod = timer()
    cyk_mod.cyk(regras, inverse, palavra)
    end_cyk_mod = timer()
    print("cyk tradicional: {} ms".format(end_cyk - start_cyk))
    print("cyk modificado : {} ms".format(end_cyk_mod - start_cyk_mod))
