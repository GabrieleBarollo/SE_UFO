from copy import deepcopy

import networkx as nx
from geopy import distance

from database.dao import DAO


class Model:
    def __init__(self):
        self._mapState = {}

    def get_years(self):
        return DAO.read_years()
    def get_shapes(self):
        return DAO.read_shapes()

    def generate_graph(self, anno, shape):
        self.G = nx.Graph()
        lista_nodi = DAO.read_states()
        self.G.add_nodes_from(lista_nodi)

        for nodo in lista_nodi:
            self._mapState[nodo.id] = nodo

        info_edges = DAO.read_edges(anno, shape)
        for info in info_edges:
            if self.G.has_edge(self._mapState[info[0]], self._mapState[info[1]]):
                pass
            else:
                self.G.add_edge(self._mapState[info[0]], self._mapState[info[1]], peso=info[2])





        info_fin = []
        for nodo in self.G.nodes():
            somma_vicini = 0
            for vicino in self.G.neighbors(nodo):
                somma_vicini += self.G[nodo][vicino]['peso']
                if vicino == list(self.G.neighbors(nodo))[-1]:
                    info_fin.append((nodo, somma_vicini))

        return info_fin


    def ricercaPercorso(self):
        self.percorso_migliore = []
        self.distanza_max = float('-inf')


        for state in self.G.nodes():
            self.ricorsione(state, [state], 0, 0)

        return self.percorso_migliore


    def ricorsione(self, stato_iniziale, parziale, peso_arco_precedente, distanza_tot):

        if distanza_tot > self.distanza_max:
            self.distanza_max = distanza_tot
            self.percorso_migliore = deepcopy(parziale)

        for vicino in self.G.neighbors(stato_iniziale):
            peso_arco = self.G[stato_iniziale][vicino]['peso']
            d = distance.geodesic((stato_iniziale.lat, stato_iniziale.lng), (vicino.lat, vicino.lng)).km
            if peso_arco > peso_arco_precedente:
                distanza_tot += d
                parziale.append(vicino)
                self.ricorsione(vicino, parziale, peso_arco, distanza_tot)
                parziale.pop()














