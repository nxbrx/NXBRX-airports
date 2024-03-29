import pandas as pd
from geopy.distance import geodesic as gdist

class Grafo:

    def __init__(self, vertices):
        self.V = vertices  # qtd de vértices
        self.grafo = []  # Grafo

    def adicionaAresta(self, tupla1, tupla2):

        # calculando a distância entre os pontos usando latitude e longitude de cada aeroporto
        peso = gdist((tupla1[1], tupla1[2]), (tupla2[1], tupla2[2])).kilometers  # peso da aresta = distancia em Km arredondados
        self.grafo.append([tupla1[0], tupla2[0], round(peso)])

    # Encontrar o conjunto ao qual o vértice pertence
    def encontra(self, pai, i):

        if pai[i] != i:
            pai[i] = self.encontra(pai, pai[i])
        return pai[i]

    # Faz a união dos dois conjuntos por classificação
    def uniao(self, pai, nivel, x, y):

        if nivel[x] < nivel[y]:
            pai[x] = y
        elif nivel[x] > nivel[y]:
            pai[y] = x
        else:
            pai[y] = x
            nivel[x] += 1

    def KruskalMST(self):

        MST_resultado = []
        # Iterador para iterar a MST_resultado
        e = 0

        # Ordena as arestas usando a chave como o peso de cada aresta
        self.grafo = sorted(self.grafo, key=lambda item: item[2])

        pai = []
        nivel = []

        for no in range(self.V):
            pai.append(no)
            nivel.append(0)

        # Iterador para as arestas ordenadas
        i = 0
        while i < (self.V - 1):
            # armazena os valores da aresta de menor peso
            u, v, peso = self.grafo[i]
            i = i + 1

            x = self.encontra(pai, u)
            y = self.encontra(pai, v)

            # Verifica se a aresta gera um ciclo
            if x != y:
                e = e + 1
                MST_resultado.append([u, v, peso])
                self.uniao(pai, nivel, x, y)

        return MST_resultado

# Leitura da base de dados
db = pd.read_csv('airport.csv')

# Instância do grafo
g = Grafo(len(db))

# Captação dos dados da base de dados e adição das arestas
for idx, linha in db.iterrows():

    aeroporto_1 = (idx, linha['LATITUDE'], linha['LONGITUDE'])
    indice_aeroporto = linha['Numero_Aleatorio']  # Índice destino da Aresta
    linha_destino = db.iloc[indice_aeroporto]  # armazena o array da linha do Dataframe pelo índice
    aeroporto_2 = (indice_aeroporto, linha_destino[5], linha_destino[6])

    g.adicionaAresta(aeroporto_1, aeroporto_2)

# Cria a MST com o algoritmo de Kruskal
MST = g.KruskalMST()

# Imprime a Árvore de Spanning Mínimo (MST) com nomes de aeroportos
for edge in MST:
    airport1_idx, airport2_idx, distance = edge
    airport1 = db.loc[airport1_idx, 'AIRPORT']
    airport2 = db.loc[airport2_idx, 'AIRPORT']
    print(f"{airport1} <--> {airport2}, Distance: {distance} km")
