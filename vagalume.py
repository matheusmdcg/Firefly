import math
import random
import time
import numpy as np
import copy

d = 30  # número de dimensões
m = 1000  # número de iterações
n = 50  # tamanho da população
mpap = 0.25
gama = 1  # coeficiente de absorção da luz

popu = np.empty([n, d])

inf = -100
sup = 100

# Sphere function
def brightness(x):
    sum = 0
    for i in range(0, d):  # para cada dimensão
        sum = sum + (x[i] ** 2)

    return -sum

# Rosenbrock function
# def brightness(x):
#     sum = 0
#     for i in range(0, d - 1):
#         xi = x[i]
#         xnext = x[i + 1]
#         sum = sum + (100 * (xnext - xi ** 2) ** 2 + (xi - 1) ** 2)
#     return -sum
#
# #Ackley
# def brightness(x):
#     sum01 = 0
#     sum02 = 0
#
#     for i in range(0, d):  # para cada dimensão
#         sum01 = sum01 + (x[i] ** 2)
#         sum02 = sum02 + math.cos(2 * math.pi)
#
#     term01 = -20 * math.exp(-0.2 * (sum01 / d) ** (1 / 2))
#     term02 = -1 * math.exp(sum02/d)
#
#     return -round((term01 + term02 + 20 + math.exp(1)), 5)
# #Griewank
# def brightness(x):
#     sum01 = 0
#     produ = 1
#     for i in range(0, d):
#         sum01 = sum01 + (x[i] ** 2 / 4000)
#         produ = produ * math.cos(x[i]/((i+1)**(1/2)))
#
#     return -(sum01 - produ + 1)


media = 0
vezes = 10
melatual = np.empty([vezes])  # mel é melhor, no mel atual cada dimensão guarda o melhor resultado daquela iteração
mel = 1000000
start_time = time.time()

for execu in range(vezes):
    inf = -100
    sup = 100
    conj = {}
    for i in range(0, n):  # cada vagalume
        for j in range(0, d):  # tem d dimensões
            popu[i][j] = random.uniform(inf, sup)
        conj[brightness(popu[i])] = popu[i]

    melhorChave = max((list(conj.keys())))
    melhoresValores = conj[melhorChave]

    for k in range(0, m):  # iterações
        if (k + 1) % 50 == 0:
            # print(f"\n{time.time() - start_time} segundos")
            # print(f"resultado luminosidade na {k + 1} = {melhorChave}")
            popu = np.empty([n, d])
            ordenado = sorted(list(conj.keys()))
            maiorD = max(ordenado)
            maior = conj[maiorD]
            limites = list(maior)
            somas = 0
            for val in limites:
                somas += val
            somas = somas / len(limites)  # média

            inf = - abs(somas)
            sup = + abs(somas)
            # inf = - abs(somas) - abs(min(limites)) # piora os limites
            # sup = + abs(somas) + abs(max(limites)) # piora os limites

            for i in range(0, n):  # cada vagalume
                if random.random() < 0.5:
                    z = 1
                else:
                    z = -1
                for j in range(0, d):  # tem d dimensões
                    popu[i][j] = random.uniform(inf + z, sup + z)

                antigo = min(list(conj.keys()))
                luminous = brightness(popu[i])
                if luminous > antigo and luminous not in conj.keys():  # algum desses novos vagalumes, se for mais brilhante, entra
                    conj.pop(antigo)
                    conj[brightness(popu[i])] = popu[i]

        conjaux = copy.deepcopy(conj)
        ordenadoaux = sorted(list(conjaux.keys()))
        for i in range(0, n):  # qtd de vagalumes
            ordenado = sorted(list(conj.keys()))
            menorC = ordenado[i]
            menor = conj[menorC]
            for j in range(n - 5, n):
                if ordenado[i] == ordenadoaux[j]:
                    continue
                else:
                    maiorC = ordenadoaux[j]
                    maior = conjaux[maiorC]
                novo = np.zeros([d])
                ab = np.zeros([d])
                r = 0
                for p in range(0, d):  # em todas as dimensões
                    r = r + (menor[p] - maior[p]) ** 2
                    ab[p] = maior[p] - menor[p]
                r = r ** (1 / 2)
                beta = 1 + gama * r ** 2
                for p in range(0, d):
                    novo[p] = menor[p] + (1 / (ab[p] * beta))
                    if novo[p] < inf or novo[p] > sup:
                        novo[p] = random.uniform(inf, sup)

                ordenado = sorted(list(conj.keys()))
                menorC = ordenado[i]
                menor = conj[menorC]
                luminosidaden = brightness(novo)
                if luminosidaden > menorC:
                    if luminosidaden not in conj.keys():
                        conj.pop(menorC)
                        conj[luminosidaden] = novo

        maiorD = (max(list(conj.keys())))
        if maiorD > melhorChave:
            melhorChave = maiorD
            melhoresValores = conj[maiorD]

        if maiorD == 0:
            break

    melatual[execu] = -1 * melhorChave
    media = media + melatual[execu]
    if melatual[execu] < mel:
        mel = melatual[execu]

    print(f"melhor solução da {execu + 1}º execução: {melatual[execu]}")
    print(f"melhor solução da {execu + 1}º execução: {melhoresValores}")
    print(f"{time.time() - start_time} segundos")



print(f"\n\n--- tempo médio: {(time.time() - start_time) / vezes} seconds")
media = media / vezes

variancia = 0
variancia02 = 0
desvioabsolutomedio = 0
desvioabsolutomedio02 = 0

for execu in range(vezes):
    variancia = variancia + (melatual[execu] - media) ** 2
    desvioabsolutomedio = desvioabsolutomedio + abs(melatual[execu] - media)

desvio = (variancia / vezes) ** (1 / 2)
desvioabsolutomedio = desvioabsolutomedio / vezes

print(f"\nmelhor de todas execuções: {mel}")
print(f"média: {media}")
print(f"Desvio Padrão dos resultados: {desvio}")
print(f"Desvio absoluto médio dos resultados: {desvioabsolutomedio}")
