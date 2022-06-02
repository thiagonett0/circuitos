import sys
from cmath import cos, sin, atan, pi

"""A função conversor converte o arquivo txt (nome_arquivo) em uma matriz contendo as informações do circuito
(matriz) como segue:
    i) nó 'de';
    ii) nó 'para';
    iii) inicial do componente;
    iv) valor conforme o SI.
Ao final, deixe uma linha em branco."""


def conversor(nome_arquivo):
    conteudo = open(nome_arquivo, 'r', encoding='utf-8')  # Abre o arquivo;
    print('\nLembra-te de que Zc = -j/(wC) = -jXc e Zl = jwL = jXl!! Caso esteja já na impedância, basta '
          'qualquer w diferente de zero!!\n')
    frequencia = float(input('Por favor, insira a frequência angular que o circuito se encontra (w): '))
    matriz = list()  # Declara a matriz que receberá as informações;
    for linha in conteudo:
        if str(linha.split()[2])[0].lower() == 'v' or str(linha.split()[2])[0].lower() == 'a':
            matriz.append([int(linha.split()[0]), int(linha.split()[1]),
                           str(linha.split()[2]), float(linha.split()[3]), float(linha.split()[4])])  # Transforma cada
            # linha do texto (conteúdo) em um vetor. Seus elementos são as 5 informações caso sejam fontes de tensão ou
            # corrente (4ª é amplitude e a 5ª sua fase em radianos). Assim, por meio da iteração acima, realizada no
            # vetor, adiciona esses elementos na matriz (matriz).
        else:
            matriz.append([int(linha.split()[0]), int(linha.split()[1]),
                           str(linha.split()[2]), complex(linha.split()[3])])  # Transforma cada linha do texto (conteúdo)
            # em um vetor. Seus elementos são as 4 informações. Assim, por meio da iteração acima, realizada no vetor,
            # adiciona esses elementos na matriz (matriz).
    conteudo.close()  # Fecha o arquivo
    return matriz, frequencia  # Retorna a matriz pronta para a realização de cálculos


"""Função transforma coordenadas polares em retangulares."""


def polret(modulo, argumento):
    return modulo*(cos(argumento*pi/180) + 1j*sin(argumento*pi/180))


"""Função transforma coordenadas retangulares em polares. É a famosa função atan2(x,y)."""


def atan2(real, imaginario):
    if real > 0:
        return atan(imaginario/real)
    elif imaginario > 0:
        return pi/2 - atan(real/imaginario)
    elif imaginario < 0:
        return -pi/2 - atan(real/imaginario)
    elif real < 0:
        return atan(imaginario/real) + ((-1)**imaginario)*pi
    else:
        return 0


"""Troca a coordenada retangular por polar. Vale a pena notar que o argumento de saída do atan2, que usualmente é 
-pi< argumento <= pi, foi modificado para 0 < argumento <= 2pi."""


def retpolar(real, imaginario):
    return [round(((real**2 + imaginario**2)**0.5), 3), round(atan2(real, imaginario).real*(180/pi), 3)]


"""Para uma saída vetorial, é necessário fazer uso da próxima função."""


def vetorpol(vetor):
    vetorpol = []
    for linhas in range(len(vetor)):
        vetorpol.append(retpolar(vetor[linhas].real, vetor[linhas].imag))
    return vetorpol


"""Essa próxima ajusta os elementos para o circuito do tipo estacionário senoidal."""


def estacionario_senoidal(lista):
    for linhas in range(len(lista[0])):
        if str(lista[0][linhas][2])[0].lower() == 'c':
            lista[0][linhas][3] = complex(-1j/(lista[1]*lista[0][linhas][3]))
            lista[0][linhas][2] = 'r'
        elif str(lista[0][linhas][2])[0].lower() == 'l':
            lista[0][linhas][3] = complex(lista[1]*1j*lista[0][linhas][3])
            lista[0][linhas][2] = 'r'
        elif str(lista[0][linhas][2])[0].lower() == 'v':
            lista[0][linhas] = [lista[0][linhas][0], lista[0][linhas][1], lista[0][linhas][2],
                                polret(lista[0][linhas][3], lista[0][linhas][4])]
        elif str(lista[0][linhas][2])[0].lower() == 'a':
            lista[0][linhas] = [lista[0][linhas][0], lista[0][linhas][1], lista[0][linhas][2],
                                polret(lista[0][linhas][3], lista[0][linhas][4])]
    return lista[0]


# circuitodc(conversor())

# ______________________________________________________________________________________________________________________


'''CORRENTE DA FONTE DE TENSÃO: (ENTRADA, SAÍDA)'''

"""Essa função imprime vetores linha e sua versão de complexos."""


def imprime_vetor(vetor, nome):
    print(f'Esse é o vetor {nome}.')
    for i in range(len(vetor)):
        print(f'{vetor[i]:.4f}')
    print('')
    return None


def imprime_vetorcomplexo(vetor, nome):
    print(f'Esse é o vetor {nome}.')
    for i in range(len(vetor)):
        print(f'{vetor[i]}')
    print('')
    return None


"Essa função imprime matrizes."


def imprime_matriz(valores, nome):
    print(f'Essa é a matriz {nome}.')
    for i in range(len(valores)):
        for j in range(len(valores[i])-1):
            if valores[i][j] is float:
                print(f'{valores[i][j]:.4f}', end=" ")
            print(f'{valores[i][j]}', end=" ")
        if valores[i][len(valores[i])-1] is float:
            print(f'{valores[i][len(valores[i])-1]:.4f}', end="\n")
        print(f'{valores[i][len(valores[i])-1]}', end="\n")
    print('')
    return None


"""A próxima função calcula quantos nós existem no circuito. Tal cálculo é realizado por meio de simples iteração para
buscar o maior 'nó para'/'nó de destino'/'nó posterior'. Tal contagem será importante para criar o subvetor 
VetorB_Correntes."""


def qtd_nos(matriz_circuito):  # Entra a matriz-circuito
    qtdnos = 0
    for linhas in range(len(matriz_circuito)):
        if matriz_circuito[linhas][1] > qtdnos:
            qtdnos = matriz_circuito[linhas][1]
    # print(f'\nQuantidade de nós: {qtdnos}.')
    return qtdnos


"""A próxima função calcula quantas fontes de tensão existem no circuito. Para isso, basta iterar sobre as letras da
matriz-circuito e verificar se confere com a inicial V. Caso afirmativo, adiciona-se uma unidade. Tal leitura será
importante para criar o subvetor de diferença de potencial, ou como no código: vetorB_Fontes."""


def leitor_tensoes(matriz_circuito):  # Entra a matriz-circuito
    qtd_tensoes = 0
    for linhas in range(len(matriz_circuito)):
        if str(matriz_circuito[linhas][2])[0].lower() == 'v':
            qtd_tensoes += 1
    # print(f'\nQuantidade de fontes de tensão: {qtd_tensoes}.')
    return qtd_tensoes


"""Essa função cria o subvetor de mesmo nome e verifica a existência de fontes de tensão. Caso exista, adiciona a,
conforme ordem crescente dos nós, sua tensão no subvetor."""


def vetorB_Fontes(matriz_circuito):  # Entra a matriz-circuito
    vetorB_Fontes = list()
    for linhas in range(len(matriz_circuito)):
        if str(matriz_circuito[linhas][2])[0].lower() == 'v':
            vetorB_Fontes.append(matriz_circuito[linhas][3])
    # print(f'\nVetor de fontes de tensão: {vetorB_Fontes}.')
    return vetorB_Fontes


"""Análogo a função de cima. Porém verifica a existência de fontes de corrente que entram nos nós. Caso exista, 
adiciona sua amperagem. Caso contrário, adiciona 0."""


def vetorB_Correntes(matriz_circuito):  # Entra a matriz-circuito
    vetorB_Correntes = [float(0)]*qtd_nos(matriz_circuito)
    for linhas in range(len(matriz_circuito)):
        if str(matriz_circuito[linhas][2])[0].lower() == 'a':
            for nodes in range(2):
                if nodes == 0 and matriz_circuito[linhas][0] != 0:
                    vetorB_Correntes[matriz_circuito[linhas][0]-1] -= matriz_circuito[linhas][3]
                elif nodes == 1 and matriz_circuito[linhas][1] != 0:
                    vetorB_Correntes[matriz_circuito[linhas][1]-1] += matriz_circuito[linhas][3]
    # print(f'\nVetor de fontes de corrente: {vetorB_Correntes}.')
    return vetorB_Correntes


# ___________________________________________________________________________________________________________________


"""Essa próxima enche a matrizMNA com zeros!"""


def matriz_MNA(matriz, matriz_circuito):
    for i in range(qtd_nos(matriz_circuito) + leitor_tensoes(matriz_circuito)):
        linha = list()
        for j in range(qtd_nos(matriz_circuito) + leitor_tensoes(matriz_circuito)):
            elemento = float(0)
            linha.append(elemento)
        matriz.append(linha)
    return matriz


"""Essa próxima enche a matriz condutância com zeros!"""


def matriz_cond(matriz, matriz_circuito):
    for i in range(qtd_nos(matriz_circuito)):
        linha = list()
        for j in range(qtd_nos(matriz_circuito)):
            elemento = float(0)
            linha.append(elemento)
        matriz.append(linha)
    return matriz


"""Essa próxima enche a matriz C com zeros!"""


def matriz_C(matriz, matriz_circuito):
    for linhas in range(qtd_nos(matriz_circuito)):
        linha = list()
        for colunas in range(leitor_tensoes(matriz_circuito)):
            elemento = float(0)
            linha.append(elemento)
        matriz.append(linha)
    return matriz


"""Essa próxima enche a matriz C transposta com zeros!"""


def matriz_C_trans(matriz, matriz_trans):
    for linhas in range(len(matriz[0])):
        linha = list()
        for colunas in range(len(matriz)):
            elemento = float(0)
            linha.append(elemento)
        matriz_trans.append(linha)
    return matriz_trans


def matrizT(matriz, matriz_transp):
    for linhas in range(len(matriz)):
        for colunas in range(len(matriz[linhas])):
            matriz_transp[colunas][linhas] = matriz[linhas][colunas]
    return matriz_transp


def seletor(matrizG, matriz_circuito, L, C):
    # print(L, C)
    for linhas in range(len(matriz_circuito)):
        if ((matriz_circuito[linhas][0] - 1 == L and matriz_circuito[linhas][1] - 1 == C) or
            (matriz_circuito[linhas][0] - 1 == C and matriz_circuito[linhas][1] - 1 == L)) and \
                str(matriz_circuito[linhas][2])[0].lower() == 'r':
            # print(matriz_circuito[linhas][2], matriz_circuito[linhas][3])
            matrizG[L][C] -= 1/matriz_circuito[linhas][3]
            matrizG[C][L] -= 1/matriz_circuito[linhas][3]
    return None


"""A próxima acessa os elementos da matriz_MNA superior (e inferior, pois basta trocar os índices de linha e coluna).
Ao fazer isso, verifica se seu índice confere com algum elemento (que não seja fonte de tensão ou corrente) do circuito
(matriz_circuito). Caso afirmativo, o seletor alça tal elemento. Porém, a matrizMNA adiciona seu inverso aditivo e
multiplicativo."""


def triang_supinf(matrizG, matriz_circuito):
    for linhas in range(len(matrizG)-1):
        for colunas in range(linhas+1, len(matrizG[linhas])):
            # print(f'Linha, coluna e elemento das respectivas: {linhas, colunas, matriz[linhas][colunas]}')
            seletor(matrizG, matriz_circuito, linhas, colunas)
    return matrizG


def seletor_diagonal(matrizG, matriz_circuito, L):
    for linhas in range(len(matriz_circuito)):
        if (matriz_circuito[linhas][0] - 1 == L or matriz_circuito[linhas][1] - 1 == L) and str(matriz_circuito[linhas][2])[0].lower() == 'r':
            matrizG[L][L] += 1/matriz_circuito[linhas][3]
    return None


def diagonal(matrizG, matriz_circuito):
    for linhas in range(len(matrizG)):
        seletor_diagonal(matrizG, matriz_circuito, linhas)
    return matrizG


"""Essa busca as fontes de tensão no circuito para saber as correntes que passam por cada uma. Sendo assim, torna-se
possível criar a matrizC. Foi adotado que o maior nó fica definido como sendo o maior potencial no ramo. Ou seja, a
corrente passa do maior nó para menor nó, obedecendo a convenção."""


def seletor_tensoes(matrizC, matriz_circuito):
    contador = 0
    for linhas in range(len(matriz_circuito)):  # Itera sobre a matriz_circuito em busca de fontes de tensão.
        if str(matriz_circuito[linhas][2])[0].lower() == 'v':  # Ao achar uma, acrescenta ao contador, já que as fontes
            # devem ser diferenciadas.
            for colunas in range(2):
                if matriz_circuito[linhas][colunas] != 0 and colunas == 0:
                    # print(matriz_circuito[linhas])
                    matrizC[matriz_circuito[linhas][0]-1][contador] = - float(1)
                    # print(matriz_circuito[linhas][0])
                elif matriz_circuito[linhas][colunas] != 0 and colunas == 1:
                    # print(matriz_circuito[linhas])
                    matrizC[matriz_circuito[linhas][1]-1][contador] = float(1)
                    # print(matriz_circuito[linhas][1])
            contador += 1
    return matrizC


def G(matrizG, matriz_circuito):
    triang_supinf(matrizG, matriz_circuito)
    diagonal(matrizG, matriz_circuito)
    # imprime_matriz(matrizG, 'Condutância')
    return matrizG


def C(matrizC, matriz_circuito):
    seletor_tensoes(matrizC, matriz_circuito)
    # imprime_matriz(matrizC, 'Matriz C')
    return matrizC


def Ctrans(matrizC, matrizCtrans):
    matriz_C_trans(matrizC, matrizCtrans)
    matrizT(matrizC, matrizCtrans)
    # imprime_matriz(matrizCtrans, 'Matriz C transposta')
    return


"""Essa função apenas concatena as duas anteriores de forma a obtermos o vetor-linha B da expressão matricial: 
Ax = B."""


def B(vetorB_Correntes, vetorB_Fontes):
    imprime_vetor(vetorB_Correntes + vetorB_Fontes, 'vetor B')
    return vetorB_Correntes + vetorB_Fontes


nome_arquivo = input('Por favor, insira o nome do arquivo contendo as 4 informações acima e espaçadas por espaço '
                     'somente: ')  # Permite o usuário entrar com o nome do texto;


matriz_original, w = conversor(nome_arquivo)
imprime_matriz(matriz_original, 'Circuito original')
matriz_circuito = estacionario_senoidal([matriz_original, w])
imprime_matriz(matriz_circuito, 'Circuito estacionário senoidal')
qtd_nos(matriz_circuito)

matrizMNA = list()
matrizG = list()
matrizC = list()
matrizCtrans = list()


matriz_MNA(matrizMNA, matriz_circuito)
matriz_cond(matrizG, matriz_circuito)
matriz_C(matrizC, matriz_circuito)

vetorB = B(vetorB_Correntes(matriz_circuito), vetorB_Fontes(matriz_circuito))
G(matrizG, matriz_circuito)
C(matrizC, matriz_circuito)
Ctrans(matrizC, matrizCtrans)


'''
nome_arquivo = input('Por favor, insira o nome do arquivo contendo as 4 informações acima e espaçadas por espaço '
                     'somente: ')  # Permite o usuário entrar com o nome do texto;


matriz_original = conversor(nome_arquivo)
matriz_circuito = conversor(nome_arquivo)
imprime_matriz(matriz_original, 'Circuito original')


matriz_circuito = circuitodc(matriz_circuito)
imprime_matriz(matriz_circuito, 'Circuito DC')


matrizMNA = list()
matrizG = list()
matrizC = list()
matrizCtrans = list()


matriz_MNA(matrizMNA, matriz_circuito)
matriz_cond(matrizG, matriz_circuito)
matriz_C(matrizC, matriz_circuito)


vetorB = B(vetorB_Correntes(matriz_circuito), vetorB_Fontes(matriz_circuito))
G(matrizG, matriz_circuito)
C(matrizC, matriz_circuito)
Ctrans(matrizC, matrizCtrans)
'''

# _____________________________________________________________________________________________________________________


"""A próxima concatena todas as demais matrizes. Ou seja, forma a matriz MNA a partir da concatenação das matrizes:
   i) matriz G;
   ii) matriz C;
   iii) matriz C transposta.
"""


def concatena(matriz_circuito, matrizMNA, matrizG, matrizC, matrizCtrans):
    for linhas in range(len(matrizMNA)-leitor_tensoes(matriz_circuito)):
        for colunas in range(len(matrizMNA)-leitor_tensoes(matriz_circuito)):
            matrizMNA[linhas][colunas] = matrizG[linhas][colunas]

    for linhas in range(len(matrizC)):
        for colunas in range(len(matrizC[linhas])):
            matrizMNA[linhas][colunas + qtd_nos(matriz_circuito)] = matrizC[linhas][colunas]

    for linhas in range(len(matrizCtrans)):
        for colunas in range(len(matrizCtrans[linhas])):
            matrizMNA[linhas + qtd_nos(matriz_circuito)][colunas] = matrizCtrans[linhas][colunas]

    imprime_matriz(matrizMNA, 'Matriz MNA final')
    return matrizMNA


concatena(matriz_circuito, matrizMNA, matrizG, matrizC, matrizCtrans)


# ______________________________________________________________________________________________________________________

tamanho = len(matrizMNA)
matriz = matrizMNA
vetorC = [None]*tamanho
vetorS = [None]*tamanho

"Essa função auxiliar troca as colunas especificadas em maior_coluna. Aqui troca-se a primeira linha da k-ésima" \
"matriz pela linha que contém o maior elemento da k-ésima coluna."


def troca_linha(matriz, vetor_linha, linhadomaior, k):
    matriz[k], matriz[linhadomaior] = matriz[linhadomaior], matriz[k]
    vetor_linha[k], vetor_linha[linhadomaior] = vetor_linha[linhadomaior], vetor_linha[k]     # Repara que, ao
    # operar a substituição na matriz, deve-se executar no vetor de entrada (vetor_linha).
    return None


"Essa função encontra o maior elemento da coluna k."


def maior_coluna(matriz, vetor_linha, k):
    mc = matriz[k][k]          # mc significa o maior elemento da coluna. Nesse caso, no início da
    # k-ésima matriz ou k-ésima linha e coluna da matriz original.
    linhadomaior = k           # Supomos que mc é o primeiro da k-ésima matriz e, obviamente, está na k-ésima
    # linha da matriz de entrada.
    for linha in range(k, tamanho):          # Itera-se sobre as linhas da k-ésima matriz.
        if abs(matriz[linha][k]) > abs(mc):  # and matriz[linha][k] != 0:           Ocorre a troca do maior da coluna.
            mc = matriz[linha][k]
            linhadomaior = linha
    troca_linha(matriz, vetor_linha, linhadomaior, k)          # Chama a função para operar a troca única de linhas.
    return troca_linha(matriz, vetor_linha, linhadomaior, k)


"Essa função escalona a matriz da coluna k até a última da direita."


def escalonamento(matriz, k):
    pivo = matriz[k][k]          # Primeiro elemento da diagonal da matriz k-ésima.
    for linha in range(k+1, tamanho):          # Itera sobre as linhas que vem embaixo.
        primeirodalinha = matriz[linha][k]
        for coluna in range(k, tamanho):          # Ocorre a eliminação gaussiana
            if pivo != 0:
                matriz[linha][coluna] = matriz[linha][coluna] - (matriz[k][coluna]*primeirodalinha/pivo)   # Multiplica
                # a primeira linha da matriz k-ésima pelo fator especificado e depois soma com as demais linhas.
                matriz[linha][k] = primeirodalinha/pivo        # Esse elemento guarda as operações na matriz L.
    return matriz


"Essa função de fato faz a decomposição LU da matriz. Tudo por meio de sucessivas " \
"k (tamanho da matriz) repetições que são possibilitadas pelas funções maior_coluna e escalonamento."


def decomposicao_lu(matriz, vetor_linha):
    for k in range(tamanho-1):   # Aqui ocorre a iteração sobre as linhas da matriz. Repara que para k=0,
        # temos a matriz de entrada; para k=1, temos a matriz de entrada exceto a primeira linha e coluna; para k=2,
        # matriz de entrada exceto as duas primeiras linhas e colunas; .... Só não itera sobre o último elemento!
        maior_coluna(matriz, vetor_linha, k)
        escalonamento(matriz, k)
    return matriz


"Essa função "


def somatorio(matriz_l, vetor_c, i):
    soma = 0
    for a in range(i):
        soma += matriz_l[i][a]*vetor_c[a]
    return soma


"Essa função "


def cria_c(matriz, vetorB):
    vetorC[0] = vetorB[0]
    for i in range(1, tamanho):
        somatorio(matriz, vetorC, i)
        for j in range(i):
            vetorC[i] = vetorB[i] - somatorio(matriz, vetorC, i)
    return vetorC


"Essa função "


def somatorio2(matrizU, vetorS, i):
    soma = 0
    for a in range(i):
        soma += vetorS[tamanho-1-a]*matrizU[tamanho-1-i][tamanho-1-a]
    if matrizU[tamanho-1-i][tamanho-1-i] == 0:
        return 0
    else:
        return soma/matrizU[tamanho-1-i][tamanho-1-i]


"Essa função fornece a solução do sistema."


def solucao(matriz, vetorC):
    if matriz[tamanho-1][tamanho-1] != 0:
        vetorS[tamanho-1] = vetorC[tamanho-1]/matriz[tamanho-1][tamanho-1]
    else:
        vetorS[tamanho-1] = 0
    for i in range(1, tamanho):
        if matriz[tamanho-1-i][tamanho-1-i] != 0:
            somatorio2(matriz, vetorS, i)
            vetorS[tamanho-1-i] = (vetorC[tamanho-1-i]/matriz[tamanho-1-i][tamanho-1-i]) - (somatorio2(matriz, vetorS, i))
        else:
            somatorio2(matriz, vetorS, i)
            vetorS[tamanho-1-i] = 0 - (somatorio2(matriz, vetorS, i))
    return vetorS


"Essa função calcula numericamente o determinante da matriz de entrada."


def det_matriz(matriz):
    vetor_diagonal = list()  # Cria um vetor que vai receber os elementos da diagonal da matriz U (A diagonal da L é
    # composta por 1s somente.).
    determinante = 1  # Declara determinante como sendo a identidade multiplicativa.
    for k in range(len(matriz)):
        vetor_diagonal.append(matriz[k][k])  # Adiciona todos os elementos da diagonal no vetor.
    for k in range(len(vetor_diagonal)):
        determinante *= vetor_diagonal[k]  # Faz o produto entre todos os elementos da diagonal.
    if determinante != 0:
        print(f"\nSistema possui uma única solução \ne seu determinante é, aproximadamente:{determinante:.4f}!\n")
    else:
        print("\nSistema não possui uma única solução!\n")
        sys.exit()
    return determinante


def lureal():
    print("\n")
    decomposicao_lu(matriz, vetorB)
    print("Matriz L e U:")
    imprime_matriz(matriz, 'Solução LU')
    cria_c(matriz, vetorB)
    print("\nA solução do sistema (o vetor S) é,\n"
          "lembrando que primeiro vem as tensões e depois correntes nas fontes):")
    solucao(matriz, vetorC)
    imprime_vetor(vetorS, 'Solução do sistema')
    print("\n")
    imprime_vetorcomplexo(vetorpol(vetorS), 'Solução em coordenadas polares (graus)')
    det_matriz(matriz)
    return None


lureal()


# ______________________________________________________________________________________________________________________


"""A próxima função acha as condições iniciais dos capacitores por meio da matriz original (circuito antes das 
modificações) e do vetor solução. Primeiro, itera-se sobre a matriz original de forma a achar seus capacitores. Ao 
encontrá-los, guarda os nós de anteriores e posteriores. Agora, itera-se sobre o vetor solução ao mesmo tempo iterando
sobre a matriz original. Ao verificar que o índice (+1, pois Python conta do 0) é igual ao nó, faz subtração (nó ante-
rior) ou adição (nó posterior), seguindo a convenção adotada durante todo o código."""


def condcap(matriz_original, vetor_sol):
    vetor_cond = list()
    for linhas in range(len(matriz_original)):
        if str(matriz_original[linhas][2])[0].lower() == 'c':
            vetor_cond.append([matriz_original[linhas][0], matriz_original[linhas][1]])
    for linhas in range(len(vetor_cond)):  # Adição de mais uma coluna para entrar com as diferenças de potenciais.
        vetor_cond[linhas].append(0)
    for linhas in range(len(vetor_sol)):
        for nodes in range(len(vetor_cond)):
            if linhas + 1 == vetor_cond[nodes][0]:  # Verificação do índice (+1, pois começa do 0)
                # com o nó anterior do capacitor. Por convenção, faz a subtração do potencial.
                vetor_cond[nodes][2] -= round(vetor_sol[linhas], 4)
            elif linhas + 1 == vetor_cond[nodes][1]:  # Verificação do índice (+1, pois começa do 0)
                # com o nó posterior do capacitor. Por convenção, faz a adição do potencial.
                vetor_cond[nodes][2] += round(vetor_sol[linhas], 4)
    imprime_matriz(vetor_cond, 'Condição inicial do(s) capacitor(es). Os dois primeiros nós e o potencial')
    return vetor_cond


condcap(matriz_circuito, vetorS)
