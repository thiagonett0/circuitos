"""
Seja um circuito elétrico sem ligações em delta, então ele pode ser solucionado numericamente por meio deste código. Pa-
ra tal, faz-se necessário que o documento txt seja escrito com os seguintes argumentos, espaçados:

    i) nó anterior (assumido, ao longo do código, possuir potencial menor que o posterior);
    ii) nó posterior;
    iii) inicial do componente elétrico (r: resistência; v: fonte de tensão; a: fonte de corrente; c: capacitor; l: in-
    dutor; d: diodo);
    iv) valor conforme o SI.
    Ao final, uma linha em branco.

O resolvente numérico resolve o circuito no regime DC como AC. Primeiramente, evocamos a função conversor para inserir-
mos o nome do documento, que gerará outro em forma matricial, utilizado para cálculos. Esse último, nomeado de
"matrizcircuito" deve ser guardado para ser acessado pela função:

    i) circuitodc, que modificará o circuito para resolução em DC;
    ii) circuitac, que modificará o circuito para resolução em AC.

O processo para a solução em DC segue os seguintes passos, conforme abaixo:
    i) circuitodc, para ajustar a matriz >>>>
"""



def conversor(nome):

    """
    A função conversor converte o arquivo txt (nome_arquivo) em uma matriz contendo as informações do circuito
    (matriz) como segue:
    i) nó 'de';
    ii) nó 'para';
    iii) inicial do componente;
    iv) valor conforme o SI.
    Ao final, deixe uma linha em branco.
    """

    conteudo = open(nome, 'r', encoding='utf-8')  # Abre o arquivo;
    matriz = list()  # Declara a matriz que receberá as informações;
    for linha in conteudo:
        matriz.append([int(linha.split()[0]), int(linha.split()[1]),
                       str(linha.split()[2]), float(linha.split()[3])])  # Transforma cada linha do texto (conteudo) em
        # um vetor. Seus elementos são as 4 informações. Assim, por meio da iteração acima, realizada no vetor, adiciona
        # esses elementos na matriz (matriz).
    conteudo.close()  # Fecha o arquivo
    # print(f'Circuito original: {matriz}')
    imprime_matriz(matriz, 'Original')
    return matriz  # Retorna a matriz pronta para a realização de cálculos


def circuitodc(matriz):

    """A função circuitodc varre a matriz-circuito verificando a existência de capacitores e indutores. Por meio da teoria
    de circuitos, ao considerar o ramo do capacitor como aberto e o ramo do indutor como curto-circuito, obtemos um circuito
    DC. A próxima função realiza tal tarefa."""

    for linha in range(len(matriz)):  # Itera sobre a matriz em busca de capacitores (C), indutores (L) e diodos (D);
        if str(matriz[linha][2])[0].lower() == 'c':
            matriz[linha][2], matriz[linha][3] = 'r', 1e12  # Numericamente equivalente a um ramo aberto;
        elif str(matriz[linha][2])[0].lower() == 'l':
            matriz[linha][2], matriz[linha][3] = 'r', 1e-12  # Numericamente equivalente a um curto-circuito;
        elif str(matriz[linha][2])[0].lower() == 'd':
            matriz[linha][2] = 'v'  # Modelo bateria do diodo;
    # print(f'Circuito DC: {matriz}')
    imprime_matriz(matriz, 'Circuito DC')
    return matriz  # Após as alterações, a função retorna o circuito DC.


# ______________________________________________________________________________________________________________________

'''CORRENTE DA FONTE DE TENSÃO: (ENTRADA, SAÍDA)'''


def imprime_vetor(vetor, nome):

    """Essa função imprime vetores linha."""

    print(f'\nEsse é o vetor {nome}:\n')
    for i in range(len(vetor)):
        print(f'{vetor[i]:.12f}')
    print('\n')
    return None


def imprime_matriz(valores, nome):

    "Essa função imprime matrizes."

    print(f'\nEssa é a matriz {nome}:\n')
    for i in range(len(valores)):
        for j in range(len(valores[i])-1):
            if valores[i][j] is float:
                print(f'{valores[i][j]:.4f}', end=" ")
            print(f'{valores[i][j]}', end=" ")
        if valores[i][len(valores[i])-1] is float:
            print(f'{valores[i][len(valores[i])-1]:.4f}', end="\n")
        print(f'{valores[i][len(valores[i])-1]}', end="\n")
    print('\n')
    return None


def transposta(A):

    """
    Descrição: Seja A uma matriz quadrada de ordem n e seus elementos denotados por a[i,j]. Então, a transposição leva
    a[i,j] de A em a[j,i] de A^t. Para tal, cria-se a matriz A^t, inicialmente com zeros. Por meio de iterações, acessa
    cada elemento de A e aloca conforme a operação de transposição em A^t;

    Entrada(s): A (matriz que se quer operar a transposição);

    Saída(s): At (a transposta de A)
    """

    At = [[0]*len(A) for _ in range(len(A[0]))]
    for linhas in range(len(A)):
        for colunas in range(len(A[linhas])):
            At[colunas][linhas] = A[linhas][colunas]
    return At


# ______________________________________________________________________________________________________________________


def qtd_nos(original):  # Entra a matriz-circuito

    """
    A próxima função calcula quantos nós existem no circuito. Tal cálculo é realizado por meio de simples iteração para
    buscar o maior 'nó para'/'nó de destino'/'nó posterior'. Tal contagem será importante para criar o subvetor
    VetorB_Correntes.
    """

    qtdnos = 0
    for linhas in range(len(original)):
        if original[linhas][1] > qtdnos:
            qtdnos = original[linhas][1]
    # print(f'\nQuantidade de nós: {qtdnos}.')
    return qtdnos


def leitor_tensoes(original):  # Entra a matriz-circuito

    """A próxima função calcula quantas fontes de tensão existem no circuito. Para isso, basta iterar sobre as letras da
    matriz-circuito e verificar se confere com a inicial V. Caso afirmativo, adiciona-se uma unidade. Tal leitura será
    importante para criar o subvetor de diferença de potencial, ou como no código: vetorB_Fontes."""

    qtd_tensoes = 0
    for linhas in range(len(original)):
        if str(original[linhas][2])[0].lower() == 'v':
            qtd_tensoes += 1
    # print(f'\nQuantidade de fontes de tensão: {qtd_tensoes}.')
    return qtd_tensoes


def matrizG(modificada):
    """
    Descrição:

    Entrada(s):

    Saída(s):
    """
    G = [([0]*(len(vetorb(modificada)[1])+len(vetorb(modificada)[2])))
         for _ in range(len(vetorb(modificada)[1])+len(vetorb(modificada)[2]))]

    """Acessa os elementos da matriz_MNA superior (e inferior, pois basta trocar os índices de linha e coluna).
    Ao fazer isso, verifica se seu índice confere com algum elemento (que não seja fonte de tensão ou corrente) do circuito
    (matriz_circuito). Caso afirmativo, o seletor alça tal elemento. Porém, a matrizMNA adiciona seu inverso aditivo e
    multiplicativo."""

    for linhas in range(len(G)-1):
        for colunas in range(linhas+1, len(G[linhas])):
            # print(f'Linha, coluna e elemento das respectivas: {linhas, colunas, matriz[linhas][colunas]}')
            for linhas2 in range(len(modificada)):
                if ((modificada[linhas2][0] - 1 == linhas and modificada[linhas2][1] - 1 == colunas) or
                    (modificada[linhas2][0] - 1 == colunas and modificada[linhas2][1] - 1 == linhas)) and \
                        str(modificada[linhas2][2])[0].lower() == 'r':
                    # print(matriz_circuito[linhas][2], matriz_circuito[linhas][3])
                    G[linhas][colunas] -= 1/modificada[linhas2][3]
                    G[colunas][linhas] -= 1/modificada[linhas2][3]
    for L in range(len(G)):
        for linhas in range(len(modificada)):
            if (modificada[linhas][0] - 1 == L or modificada[linhas][1] - 1 == L) and \
                    str(modificada[linhas][2])[0].lower() == 'r':
                G[L][L] += 1/modificada[linhas][3]
    return G


def matrizC(modificada):
    """
    Descrição: Essa busca as fontes de tensão no circuito para saber as correntes que passam por cada uma. Sendo assim,
    torna-se possível criar a matriz C. Foi adotado que o nó posterior possui o maior potencial no ramo. Ou seja, a cor-
    rente passa do nó posterior para o anterior, obedecendo a convenção;

    Entrada(s): matriz_circuito (matriz original do circuito);

    Saída(s): C (matriz que indica onde há fontes de corrente nos nós), transposta(C) (matriz transposta de C).
    """
    C = [[0]*len(vetorb(modificada)[2]) for _ in range(len(vetorb(modificada)[1]))]
    contador = 0
    for linhas in range(len(modificada)):  # Itera sobre a matriz_circuito em busca de fontes de tensão.
        if str(modificada[linhas][2])[0].lower() == 'v':  # Ao achar uma, acrescenta ao contador, já que as fontes
            # devem ser diferenciadas.
            for colunas in range(2):
                if modificada[linhas][colunas] != 0 and colunas == 0:
                    # print(matriz_circuito[linhas])
                    C[modificada[linhas][0]-1][contador] = - 1
                    # print(matriz_circuito[linhas][0])
                elif modificada[linhas][colunas] != 0 and colunas == 1:
                    # print(matriz_circuito[linhas])
                    C[modificada[linhas][1]-1][contador] = 1
                    # print(matriz_circuito[linhas][1])
            contador += 1
    return C, transposta(C)


def vetorb(modificada):

    """Análogo a função de cima. Porém verifica a existência de fontes de corrente que entram nos nós. Caso exista,
    adiciona sua amperagem. Caso contrário, adiciona 0."""

    bcorrentes = [0]*qtd_nos(modificada)
    for linhas in range(len(modificada)):
        if str(modificada[linhas][2])[0].lower() == 'a':
            for nodes in range(2):
                if nodes == 0 and modificada[linhas][0] != 0:
                    bcorrentes[modificada[linhas][0]-1] -= modificada[linhas][3]
                elif nodes == 1 and modificada[linhas][1] != 0:
                    bcorrentes[modificada[linhas][1]-1] += modificada[linhas][3]
    # print(f'\nVetor de fontes de corrente: {vetorB_Correntes}.')

    """Essa função cria o subvetor de mesmo nome e verifica a existência de fontes de tensão. Caso exista, adiciona a,
    conforme ordem crescente dos nós, sua tensão no subvetor."""

    bfontes = list()
    for linhas in range(len(modificada)):
        if str(modificada[linhas][2])[0].lower() == 'v':
            bfontes.append(modificada[linhas][3])
    # print(f'\nVetor de fontes de tensão: {vetorB_Fontes}.')
    return bcorrentes + bfontes, bcorrentes, bfontes


def matrizA(modificada):

    A = [([0]*(qtd_nos(modificada)+leitor_tensoes(modificada)))
         for _ in range(qtd_nos(modificada)+leitor_tensoes(modificada))]
    G = matrizG(modificada)
    C = matrizC(modificada)[0]
    Ct = matrizC(modificada)[1]

    for linhas in range(len(A)-leitor_tensoes(modificada)):
        for colunas in range(len(A)-leitor_tensoes(modificada)):
            A[linhas][colunas] = G[linhas][colunas]
    for linhas in range(len(C)):
        for colunas in range(len(C[linhas])):
            A[linhas][colunas + qtd_nos(modificada)] = C[linhas][colunas]
    for linhas in range(len(Ct)):
        for colunas in range(len(Ct[linhas])):
            A[linhas + qtd_nos(modificada)][colunas] = Ct[linhas][colunas]
    return A


# ______________________________________________________________________________________________________________________


"""
Agora entra a parte da resolução do circuito por meio da decomposição LU.

Seja a equação matricial Ax = b, tais que:

    i) A é a matriz de ordem a ser definida na função A;
    ii) x é o vetor solução. Aquele que se deseja determinar;
    iii) b é o vetor independente a ser definido na função b.

Então, o sistema é equivalente ao seguinte:
    i) Ly = b, resolvida por substituição posterior;
    ii) Ux = y, resolvida por substituição anterior.

tais que:
    i) L é a matriz triangular inferior com diagonal unitária;
    ii) U é a matriz triangular superior;
    iii) e satisfazem A = LU.
"""


def troca_linha(A, b, linhadomaior, k):

    """
    Descrição: opera a troca de linhas da matriz A e do vetor b conforme necessário durante a decomposição LU. A troca
    de linhas ocorre entre uma linha qualquer k e o do pivô. Mais acuradamente, troca-se a primeira linha da k-ésima
    matriz particionada inferior direita pela linha que contém o elemento de maior módulo da k-ésima coluna, obtido pela
    função maior_coluna. Sendo assim, tanto a matriz A como o vetor b são modificados;

    Entrada(s): A, b, linhadomaior (linha do pivô), k (k-ésima iteração);

    Saída(s): .
    """

    A[k], A[linhadomaior] = A[linhadomaior], A[k]
    b[k], b[linhadomaior] = b[linhadomaior], b[k]     # Repara que, ao operar a substituição na matriz, deve-se
    # executar no vetor de entrada (vetor_linha).
    return None


def maior_coluna(A, b, k):

    """
    Descrição: faz a procura do elemento de maior módulo da coluna da k-ésima matriz particionada inferior direita. Pri-
    meiramente, supõe que tal elemento é o primeiro da coluna durante a k-ésima iteração, ou seja, o k-ésimo da diagonal
    . Consequentemente, supõe-se que sua linha é a k-ésima da matriz A. Para selecionar o maior, itera-se sobre os
    elementos da coluna e verifica se a desigualdade abaixo é satisfeita. Caso afirmativo, então troca-se o elemento e a
    linha. Ao final, chama a função auxiliar troca_linha para efetuar a troca de linhas necessária;

    Entrada(s): A, b, k (k-ésima iteração)

    Saída(s): troca_linha(A, b, linhadomaior, k) (ou seja a matriz A e o vetor b alterados)
    """

    mc = A[k][k]          # mc significa o maior elemento da coluna. Nesse caso, no início da
    # k-ésima matriz ou k-ésima linha e coluna da matriz original.
    linhadomaior = k           # Supomos que mc é o primeiro da k-ésima matriz e, obviamente, está na k-ésima
    # linha da matriz de entrada.
    for linha in range(k, len(A)):          # Itera-se sobre as linhas da k-ésima matriz.
        if abs(A[linha][k]) > abs(mc):          # Ocorre a troca do maior da coluna.
            mc = A[linha][k]
            linhadomaior = linha
    troca_linha(A, b, linhadomaior, k)          # Chama a função para operar a troca única de linhas.
    return troca_linha(A, b, linhadomaior, k)


def escalonamento(A, k):

    """
    Descrição: executa o escalonamento das k-ésimas sub-matrizes de A. Primeiramente, estabelece o pivô da k-ésima
    iteração, itera-se sobre sua coluna. Caso o pivô é nulo, então sua coluna é constituída somente de zeros e portanto
    passa para a próxima iteração (e o LU "falhará"). Caso contrário, executa eliminação Gaussiana conforme abaixo.
    Perceba que ocorre o escalonamento e também o guardar das operações. Esses valores guardados constituem os elemen-
    tos da matriz L, como consta abaixo;

    Entrada(s): A, k (k-ésima iteração);

    Saída(s): A (escalonada, na forma LU).
    """

    pivo = A[k][k]          # Primeiro elemento da diagonal da matriz k-ésima.
    for linha in range(k+1, len(A)):          # Itera sobre as linhas que vem embaixo.
        primeirodalinha = A[linha][k]
        for coluna in range(k, len(A)):          # Ocorre a eliminação gaussiana
            if pivo != 0:
                A[linha][coluna] = A[linha][coluna] - (A[k][coluna]*primeirodalinha/pivo)   # Multiplica
                # a primeira linha da matriz k-ésima pelo fator especificado e depois soma com as demais linhas.
                A[linha][k] = primeirodalinha/pivo        # Esse elemento guarda as operações na matriz L.
    return A


def decomposicao_lu(A, b):

    """
    Descrição: executa a decomposição LU do sistema Ax = b. Essa função apenas faz o compilado das auxiliares e realiza
    as k-ésimas iterações;

    Entrada(s): A, b;

    Saída(s): A (escalonada, na forma LU).
    """

    for k in range(len(A)-1):   # Aqui ocorre a iteração sobre as linhas da matriz. Repara que para k=0,
        # temos a matriz de entrada; para k=1, temos a matriz de entrada exceto a primeira linha e coluna; para k=2,
        # matriz de entrada exceto as duas primeiras linhas e colunas; .... Só não itera sobre o último elemento!
        maior_coluna(A, b, k)
        escalonamento(A, k)
    return A


def somatorioy(A, y, limitesomatorio):

    """
    Descrição: Somatório que determina os elementos do vetor y. Repara que os elementos acessados de A são os elementos
    de L, ou seja, a parte triangular inferior de A;

    Entrada(s): A (escalonada, na forma LU), y (vetor auxiliar da decomposição), limitesomatorio (para ser o limite do
    somatório de fato, precisa subtrair 1);

    Saída(s): soma (somatório que determina os elementos do vetor y)
    """

    soma = 0
    for varmuda in range(limitesomatorio):
        soma += A[limitesomatorio][varmuda]*y[varmuda]
    return soma


def vetory(A, b):

    """
    Descrição: Determinação do vetor y. Sua expressão satisfaz:

    y[linhas] = b[linhas] - somatório_{varmuda=0}^{linhas-1} L[linhas][varmuda] * y[varmuda]

    Primeiramente, verifica-se do algoritmo matemático que y[0] = b[0]. Os demais elementos são determinados de forma
    recursiva conforme a expressão abaixo, em que j é uma variável muda do somatório.

    Entrada(s): A (escalonada, na forma LU), b

    Saída(s): y
    """

    y = [0]*len(A)
    for linhas in range(len(A)):  # Itera do y[1] até o último y.
        # for elementos in range(linhas):  # Itera de forma recursiva sobre os y anteriores
        y[linhas] = b[linhas] - somatorioy(A, y, linhas)
    return y


def somatoriox(A, x, limitesomatorio):

    """
    Descrição:

    Entrada(s): A (escalonada, na forma LU), x (vetor solução da decomposição), limitesomatorio (para ser o limite do
    somatório de fato, precisa subtrair 1);

    Saída(s):
    """

    soma = 0
    for varmuda in range(limitesomatorio):
        soma += x[len(A)-1-varmuda]*A[len(A)-1-limitesomatorio][len(A)-1-varmuda]  # Repara que vem de baixo p cima
    return soma


def vetorx(A, y):
    """
    Descrição:  Determinação do vetor x. Sua expressão satisfaz:

    x[linhas] = (y[linhas] - somatório_{varmuda=0}^{linhas-1} L[linhas][varmuda] * y[varmuda])/U[linhas][linhas]

    Entrada(s):

    Saída(s):
    """
    x = [0]*len(A)
    """if A[len(A)-1][len(A)-1] != 0:
        x[len(A)-1] = y[len(A)-1]/A[len(A)-1][len(A)-1]
    else:
        x[len(A)-1] = 0  # Esse é o caso da variável ser independente. Ou seja, o sistema possui infinitas soluções!"""
    for linhas in range(len(A)):
        if A[len(A)-1-linhas][len(A)-1-linhas] != 0:
            x[len(A)-1-linhas] = (y[len(A)-1-linhas] - somatoriox(A, x, linhas))/A[len(A)-1-linhas][len(A)-1-linhas]
        else:
            somatoriox(A, x, linhas)
            x[len(A)-1-linhas] = 0 - (somatoriox(A, x, linhas))
    return x


def det_matriz(A):

    """
    Descrição: calcula o determinante da matriz A, já escalonada. Basta calcular o produto dos elementos da sua diago-
    nal. Primeiramente, define-se o determinante como sendo 1 e um vetor (vetor_diagonal) que guardará os elementos da
    diagonal de A;

    Entrada(s): A (escalonada);

    Saída(s): detA (determinante de A).
    """

    vetor_diagonal = list()  # Cria um vetor que vai receber os elementos da diagonal da matriz U (A diagonal da L é
    # composta por 1s somente.).
    detA = 1  # Declara determinante como sendo a identidade multiplicativa.
    for linhas in range(len(A)):
        vetor_diagonal.append(A[linhas][linhas])  # Adiciona todos os elementos da diagonal no vetor.
    for elementos in range(len(vetor_diagonal)):
        detA *= vetor_diagonal[elementos]  # Faz o produto entre todos os elementos da diagonal.
    if detA != 0:
        print(f"\nSistema linearmente independente, possui uma única \nsolução e seu determinante é, "
              f"aproximadamente:{detA:.4f}!\n")
    elif detA == 0:
        print(f'\nSistema linearmente dependente, possui um conjunto infinito \nou nulo de soluções e seu '
              f'determinante é nulo.\n')
    return detA


def lureal(modificada):

    """
    Descrição: agrega todas as funções e resolve o sistema Ax = b;

    Entrada(s): ;

    Saída(s): .
    """

    A = matrizA(modificada)
    b = vetorb(modificada)[0]
    imprime_matriz(A, 'A')
    imprime_vetor(b, 'b')
    decomposicao_lu(A, b)
    imprime_matriz(A, "A na forma LU")
    det_matriz(A)
    y = vetory(A, b)
    x = vetorx(A, y)
    imprime_vetor(x, "solução do sistema (o vetor x)")
    return x


# ______________________________________________________________________________________________________________________


def condcap(inalterada, vetor_sol):

    """A próxima função acha as condições iniciais dos capacitores por meio da matriz original (circuito antes das
    modificações) e do vetor solução. Primeiro, itera-se sobre a matriz original de forma a achar seus capacitores. Ao
    encontrá-los, guarda os nós anteriores e posteriores. Depois, itera-se sobre o vetor solução ao mesmo tempo iterando
    sobre a matriz original. Ao verificar que o índice (+1, pois Python conta do 0) é igual ao nó, faz subtração (nó an-
    terior) ou adição (nó posterior), seguindo a convenção adotada durante todo o código."""

    vetor_cond = list()
    for linhas in range(len(inalterada)):
        if str(inalterada[linhas][2])[0].lower() == 'c':
            vetor_cond.append([inalterada[linhas][0], inalterada[linhas][1], inalterada[linhas][2]])
    if vetor_cond == []:
        print('\nO circuito não apresenta capacitor(es)!\n')
        return None
    for linhas in range(len(vetor_cond)):  # Adição de mais uma coluna para entrar com as diferenças de potenciais.
        vetor_cond[linhas].append(0)
    for linhas in range(len(vetor_sol)):
        for nodes in range(len(vetor_cond)):
            if linhas + 1 == vetor_cond[nodes][0]:  # Verificação do índice (+1, pois começa do 0)
                # com o nó anterior do capacitor. Por convenção, faz a subtração do potencial.
                vetor_cond[nodes][3] -= vetor_sol[linhas]
            elif linhas + 1 == vetor_cond[nodes][1]:  # Verificação do índice (+1, pois começa do 0)
                # com o nó posterior do capacitor. Por convenção, faz a adição do potencial.
                vetor_cond[nodes][3] += vetor_sol[linhas]
    for linhas in range(len(vetor_cond)):
        del vetor_cond[linhas][0]
        del vetor_cond[linhas][0]
    imprime_matriz(vetor_cond, 'condição inicial do(s) capacitor(es). Ela apresenta os dois primeiros nós e o '
                               'potencial.\nO potencial é dado por: (nó dc posterior) - (nó dc anterior)')
    return vetor_cond


def condind(inalterada, vetor_sol):
    vetor_cond = list()
    for linhas in range(len(inalterada)):
        if str(inalterada[linhas][2])[0].lower() == 'l':
            vetor_cond.append([inalterada[linhas][0], inalterada[linhas][1], inalterada[linhas][2]])
    if vetor_cond == []:
        print('\nO circuito não apresenta indutor(es)!\n')
        return None
    for linhas in range(len(vetor_cond)):  # Adição de mais uma coluna para entrar com as correntes nos indutores.
        vetor_cond[linhas].append(0)
    for linhas in range(len(vetor_sol)):
        for nodes in range(len(vetor_cond)):
            if linhas + 1 == vetor_cond[nodes][0]:  # Verificação do índice (+1, pois começa do 0)
                # com o nó anterior do capacitor. Por convenção, faz a subtração do potencial.
                vetor_cond[nodes][3] -= vetor_sol[linhas]
            elif linhas + 1 == vetor_cond[nodes][1]:  # Verificação do índice (+1, pois começa do 0)
                # com o nó posterior do capacitor. Por convenção, faz a adição do potencial.
                vetor_cond[nodes][3] += vetor_sol[linhas]
    for linhas in range(len(vetor_cond)):
        vetor_cond[linhas][3] *= 1e12
    for linhas in range(len(vetor_cond)):
        del vetor_cond[linhas][0]
        del vetor_cond[linhas][0]
    imprime_matriz(vetor_cond, 'condição inicial do(s) indutor(es). Ela apresenta os dois primeiros nós e a corrente.'
                               '\nA corrente é dada por: [ (nó dc posterior) - (nó dc anterior) ] * 1e12')
    return vetor_cond


def resolventepermanente():

    """
    Descrição: Resolve o circuito dc, por meio de análise nodal modificada e decomposição LU. A descrição dos passos
    segue como abaixo:
        i) Passa o circuito dc, em formato de texto, para matricial e guarda ela até o final do algoritmo;
        ii) Passa o circuitp dc, em formato de texto, para matricial. Mas ao contrário de i), faz-se uso constante dessa
        para montar a matriz A e vetor b do sistema Ax=b;
        iii) Modifica a matriz original. Troca capacitores e indutores para resistências;
        iv) Monta as submatrizes de A e já retorna ela montada;
        v) Soluciona o sistema Ax=b e retorna a solução x;
        vi) Grosseiramente, a matrizdc, obtida em ii) foi constantemente alterada e usada a ponto de virar a matriz A.
        Sendo assim, para zerá-la e calcular as condições iniciais, redefinimos a variável;
        vii) Calcula as tensões dos capacitores no tempo 0- a partir da matriz redefinida em vi e retorna as condições
        iniciais em forma de matriz, que será preenchida com todas as tensões dos capacitores para graficar a solução;
        viii) Análogo a vii), porém para indutores.

    Entrada(s): ;

    Saída(s): Solução do sistema (sol_dc), condições iniciais e finais dos capacitores (tensoes) e condições iniciais e
    finais dos indutores (correntes).
    """

    inalterada = conversor('Electronics\Circuits\circuitodc')
    original = conversor('Electronics\Circuits\circuitodc')
    matrizdc = circuitodc(original)
    matrizA(matrizdc)
    sol_dc = lureal(matrizdc)
    original = inalterada
    tensoesDC = condcap(original, sol_dc)
    correntesDC = condind(original, sol_dc)
    print(f'DC: {tensoesDC, correntesDC}')
    print(f'\n-------------Resolvente AC permanente!-------------\n')
    inalterada = conversor('Electronics\Circuits\circuitoac')
    original = conversor('Electronics\Circuits\circuitoac')
    matrizacpermanente = circuitodc(original)
    matrizA(matrizacpermanente)
    sol_acpermanente = lureal(matrizacpermanente)
    original = inalterada
    tensoesAC = condcap(original, sol_acpermanente)
    correntesAC = condind(original, sol_acpermanente)
    tensoes = 0
    correntes = 0
    if type(tensoesDC) == list:
        tensoes = tensoesAC + tensoesDC
    if type(correntesDC) == list:
        correntes = correntesAC + correntesDC
    print(f'AC: {tensoesAC, correntesAC}')
    print(f'Final: {tensoes, correntes}')
    sol = [sol_acpermanente] + [sol_dc]
    print(f'Solução DC: {sol_dc}')
    print(f'Solução AC: {sol_acpermanente}')
    print(f'Solução Final: {sol}')
    return sol, tensoes, correntes


resolventepermanente()
sol = resolventepermanente()[0]
tensoes = resolventepermanente()[1]
correntes = resolventepermanente()[2]

print(f'\n-----------------------------------------------------------------\n')

# ______________________________________________________________________________________________________________________

"""Resolução AC"""


"""def resolventeacpermanente():
    print(f'\n-------------Resolvente AC permanente!-------------\n')
    inalterada = conversor('circuito ac')
    original = conversor('circuito ac')
    matrizacpermanente = circuitodc(original)
    matrizA(matrizacpermanente)
    sol_acpermanente = lureal(matrizacpermanente)
    original = inalterada
    tensoes = condcap(original, sol_acpermanente)
    correntes = condind(original, sol_acpermanente)
    print(f'AC: {tensoes, correntes}')
    return sol_acpermanente, tensoes, correntes"""


# resolventeacpermanente()


print(f'\n-----------------------------------------------------------------\n')

# ______________________________________________________________________________________________________________________


def circuitoac(original, passo, k, tensoes, correntes):

    """
    Altera a matriz original, assim como a função circuitodc. Porém, aqui são implementadas as versões discretizadas
    de capacitores e indutores, exemplificadas na Prática 3 de Métodos Computacionais.

    Entrada(s): matriz (matriz original), passo (passo de discretização), k (variável de iteração), tensoes
    (condições iniciais dos capacitores) e correntes (condições iniciais dos indutores)

    Saída(s): matriz (matriz original modificada, matriz-circuitoac)
    """

    for linhas in range(len(original)):  # Itera sobre a matriz em busca de capacitores (C) e indutores (L)
        if str(original[linhas][2])[0].lower() == 'c':
            for nodes in range(len(tensoes)):  # Ao alçar a linha do capacitor na matriz-circuito, guardamos ela e
                # iteramos sobre as linhas da matriz tensões. Se os nós são iguais, então fazemos a troca.
                if tensoes != [] and original[linhas][2] == tensoes[nodes][0]:
                    original.append([original[linhas][0], original[linhas][1], 'a', original[linhas][3]*tensoes[nodes][1+k]/passo])
            original[linhas][2], original[linhas][3] = 'r', passo/original[linhas][3]
        elif str(original[linhas][2])[0].lower() == 'l':
            for nodes in range(len(correntes)):  # Ao alçar a linha do indutor na matriz-circuito, guardamos ela e
                # iteramos sobre as linhas da matriz corrente. Se os nós são iguais, então fazemos a troca.
                if correntes != [] and original[linhas][2] == correntes[nodes][0]:
                    print(f'AQUI ORIGINAL: {original}')
                    original.append([original[linhas][0], original[linhas][1], 'a', - correntes[nodes][1+k]])
            original[linhas][2], original[linhas][3] = 'r', original[linhas][3]/passo
        elif str(original[linhas][2])[0].lower() == 'd':
            original[linhas][2] = 'v'  # Modelo bateria do diodo;
    print(f'Matriz AC transitório: {original}')
    return original


def resolventeactransitorio(limite, passo, sol, tensoes, correntes):
    print(f'\n-------------Resolvente AC transitório!-------------\n')
    for iteracoes in range(limite):
        original = conversor('Electronics\Circuits\circuitoac')
        matriztransitoria = circuitoac(original, passo, iteracoes, tensoes, correntes)  # Modifica e retorna a matriz original, a
        # usada para construir Ax=b
        vetorb(matriztransitoria)
        matrizA(matriztransitoria)
        sol_transitoria = lureal(matriztransitoria)
        sol += [sol_transitoria]
        original = conversor('Electronics\Circuits\circuitoac')
        matriztransitoria = circuitoac(original, passo, iteracoes, tensoes, correntes)
    return sol, tensoes, correntes


print(f'SOLUÇÃO: {resolventeactransitorio(1, 0.1, sol, tensoes, correntes)[0]}')
