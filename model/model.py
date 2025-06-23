import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allProducts = []
        self._idMapProducts = {}
        self._grafo = nx.Graph()
        self._bestPath = []
        self._maxLen = 0

    def getAllColors(self):
        colors = DAO.getAllColors()
        colors.sort()
        return colors

    def getAllProductsFromDB(self, color):
        self._allProducts = DAO.getAllNodes(color)
        for prod in self._allProducts:
            self._idMapProducts[prod.Product_number] = prod

    def buildGraph(self, year, color):
        self._grafo.clear()
        self.getAllProductsFromDB(color)
        self._grafo.add_nodes_from(self._allProducts)
        edges = DAO.getAllEdges(year, color) # lista di tuple (n_prod1, n_prod2, peso)
        for edge in edges:
            self._grafo.add_edge(self._idMapProducts[edge[0]], self._idMapProducts[edge[1]], weight= edge[2])
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getInfoGrafo(self):
        archi = list(self._grafo.edges(data=True))
        archi.sort(key = lambda x: x[2]["weight"], reverse = True)
        archi_selezionati = archi[0:3] # [(nodo1, nodo2, {"weight": ...}), (), ()]
        prodotti = []
        for arco in archi_selezionati:
            prodotti.append(arco[0].Product_number)
            prodotti.append(arco[1].Product_number)
        # ora in prodotti ho un elenco di numero di prodotto (eventualmente duplicati)
        nodi_ripetuti = []
        for i in range(0, len(prodotti)-1):
            if prodotti[i] in prodotti[i+1:]:
                nodi_ripetuti.append(prodotti[i])
        return archi_selezionati, nodi_ripetuti

    def getAllProductsInGraph(self):
        return list(self._grafo.nodes())


    def getBestScore(self, source):
        self._bestPath = []
        self._maxLen = 0
        parziale = [source]
        vicini = self._grafo.neighbors(source)
        for vicino in vicini:
            parziale.append(vicino)
            self._ricorsione(parziale)
            parziale.pop()

        return self._maxLen-1

    def _ricorsione(self, parziale):
        if len(parziale) > self._maxLen:
            self._maxLen = len(parziale)
            self._bestPath = copy.deepcopy(parziale)
        vicini = self._grafo.neighbors(parziale[-1])
        for vicino in vicini:
            if self._grafo[vicino][parziale[-1]]["weight"] > self._grafo[parziale[-2]][parziale[-1]]["weight"] :
                parziale.append(vicino)
                self._ricorsione(parziale)
                parziale.pop()

    def getBestScore(self, source):
        self._bestPath = []
        self._maxLen = 0
        parziale = [source]
        vicini = self._grafo.neighbors(source)
        for vicino in vicini:
            parziale.append(vicino)
            self._ricorsione(parziale)
            parziale.pop()

        return self._maxLen - 1

    def _ricorsione(self, parziale):
        if len(parziale) > self._maxLen:
            self._maxLen = len(parziale)
            self._bestPath = copy.deepcopy(parziale)
        vicini = self._grafo.neighbors(parziale[-1])
        for vicino in vicini:
            if self._grafo[vicino][parziale[-1]]["weight"] > self._grafo[parziale[-2]][parziale[-1]]["weight"]:
                parziale.append(vicino)
                self._ricorsione(parziale)
                parziale.pop()