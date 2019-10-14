import math
import random
import time
import numpy as np
import copy

d = 30  # número de dimensões
m = 1000  # número de iterações
n = 50  # tamanho da população
top = 3  # quantos vagalumes com as maiores luminosidades serão considerados
gama = 1  # coeficiente de absorção da luz

popu = np.empty([n, d])


# Sphere function
# def brightness(x):
#     sum = 0
#     for i in range(0, d):  # para cada dimensão
#         sum = sum + (x[i] ** 2)
#
#     return -sum
#
# Rosenbrock function
# def brightness(x):
#     suma = 0
#     for i in range(0, d - 1):
#         xi = x[i]
#         xnext = x[i + 1]
#         suma = suma + (100 * (xnext - xi ** 2) ** 2 + (xi - 1) ** 2)
#     return -suma
#
# Ackley
def brightness(x):
    sum01 = 0
    sum02 = 0

    for i in range(0, d):  # para cada dimensão
        sum01 = sum01 + (x[i] ** 2)
        sum02 = sum02 + math.cos(2 * math.pi)

    term01 = -20 * math.exp(-0.2 * (sum01 / d) ** (1 / 2))
    term02 = -1 * math.exp(sum02 / d)

    return -round((term01 + term02 + 20 + math.exp(1)), 5)


# Griewank
# def brightness(x):
#     sum01 = 0
#     produ = 1
#     for i in range(0, d):
#         sum01 = sum01 + (x[i] ** 2 / 4000)
#         produ = produ * math.cos(x[i]/((i+1)**(1/2)))
#
#     return -(sum01 - produ + 1)


media = 0
mediai = 0
vezes = 50
iatual = np.zeros([vezes])
melatual = np.empty([vezes])  # mel é melhor, no mel atual cada dimensão guarda o melhor resultado daquela iteração
mel = 1000000
start_time = time.time()

for execu in range(vezes):
    inf = -32
    sup = 32
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
            novos = {}
            ordenado = sorted(list(conj.keys()))
            menorC = ordenado[i]
            menor = conj[menorC]
            for j in range(n - top, n):  # os TOP vagalumes
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
                beta = 1 + gama * r ** (1 / 2)
                for p in range(0, d):
                    novo[p] = round(menor[p] + (1 / (ab[p] * beta)), 5)
                    # Isso aqui embaixo melhora muito, mas talvez seja trapaça com a ideia original:
                    # if novo[p] < inf or novo[p] > sup:
                    #     novo[p] = round(random.uniform(inf, sup), 5)

                ordenado = sorted(list(conj.keys()))
                menorC = min(ordenado)

                luminosidaden = brightness(novo)
                novos[luminosidaden] = novo
            provavel = max(list(novos.keys()))
            if provavel > menorC:
                if provavel not in conj.keys():
                    conj.pop(menorC)
                    conj[provavel] = novos[provavel]

        maiorD = (max(list(conj.keys())))
        if maiorD > melhorChave:
            melhorChave = maiorD
            melhoresValores = conj[maiorD]
            if maiorD == 0:
                print(f"yeah, {k + 1}")
                mediai += 1
                iatual[execu] = k + 1
                break

        mediai = mediai + 1

    melatual[execu] = -1 * melhorChave
    media = media + melatual[execu]
    if melatual[execu] < mel:
        mel = melatual[execu]

    print(f"melhor solução da {execu + 1}º execução: {melatual[execu]}")
    print(f"melhor solução da {execu + 1}º execução: {melhoresValores}")
    print(f"{time.time() - start_time} segundos")

print(f"\n\n--- tempo médio: {(time.time() - start_time) / vezes} seconds")
media = media / vezes
mediai = mediai / vezes

variancia = 0
variancia02 = 0
desvioabsolutomedio = 0

for execu in range(vezes):
    if iatual[execu] == 0:
        iatual[execu] = m

for execu in range(vezes):
    variancia = variancia + (melatual[execu] - media) ** 2
    variancia02 = variancia02 + (iatual[execu] - mediai) ** 2
    desvioabsolutomedio = desvioabsolutomedio + abs(melatual[execu] - media)

desvio = (variancia / vezes) ** (1 / 2)
desvioabsolutomedio = desvioabsolutomedio / vezes
desvio02 = (variancia02 / vezes) ** (1 / 2)  # desvio padrão da quantidade de iterações

print(f"\nmédia iterações: {mediai}")
print(f"Desvio Padrão da quantidade de iterações: {desvio02}")

print(f"\nmelhor de todas execuções: {mel}")
print(f"média: {media}")
print(f"Desvio Padrão dos resultados: {desvio}")
print(f"Desvio absoluto médio dos resultados: {desvioabsolutomedio}")
