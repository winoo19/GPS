import sys
from typing import List, Tuple, Dict
import random as r

import networkx as nx
import matplotlib.pyplot as plt

from heapdict import heapdict

INFTY = sys.float_info.max


class Grafo:
    # Diseñar y construir la clase grafo

    def __init__(self, dirigido=False):
        """Crea un grafo dirigido o no dirigido.

        Args:
            dirigido: Flag que indica si el grafo es dirigido o no.
        Returns: Grafo o grafo dirigido (según lo indicado por el flag)
        inicializado sin vértices ni aristas.
        """
        self._dirigido = dirigido
        self.adj: dict[object, dict[object, dict]] = {}
        self.aristas: dict[object, dict] = {}

    def __str__(self):
        """Representación en string del grafo.

        Args: None
        Returns: Una representación en string del grafo.
        """
        return str(self.adj)

    def __getitem__(self, v: object) -> List[object]:
        """Devuelve la lista de adyacencia del vértice v.

        Args: v vértice del grafo
        Returns: La lista de adyacencia del vértice v.
        """
        return self.lista_adyacencia(v)

    def __iter__(self):
        """Iterador del grafo.

        Args: None
        Returns: Un iterador sobre los vértices del grafo.
        """
        return iter(self.adj)

    #### Operaciones básicas del TAD ####
    def es_dirigido(self) -> bool:
        """Indica si el grafo es dirigido o no

        Args: None
        Returns: True si el grafo es dirigido, False si no.
        """
        return self._dirigido

    def agregar_vertice(self, v: object) -> None:
        """Agrega el vértice v al grafo.

        Args: v vértice que se quiere agregar
        Returns: None
        """
        if v not in self.adj:
            self.adj[v] = {}

    def agregar_arista(
        self, s: object, t: object, data: object, weight: float = 1
    ) -> None:
        """Si los objetos s y t son vértices del grafo, agrega
        una arista al grafo que va desde el vértice s hasta el vértice t
        y le asocia los datos "data" y el peso weight.
        En caso contrario, no hace nada.

        Args:
            s: vértice de origen (source)
            t: vértice de destino (target)
            data: datos de la arista
            weight: peso de la arista
        Returns: None
        """
        if s == t and not self.es_dirigido():
            return None
        if s in self.adj and t in self.adj:
            self.aristas[(s, t)] = {"data": data, "weight": weight}
            self.adj[s][t] = {"data": data, "weight": weight}
            if not self.es_dirigido():
                self.aristas[(t, s)] = {"data": data, "weight": weight}
                self.adj[t][s] = {"data": data, "weight": weight}

    def eliminar_vertice(self, v: object) -> None:
        """Si el objeto v es un vértice del grafo lo elimiina.
        Si no, no hace nada.

        Args: v vértice que se quiere eliminar
        Returns: None
        """
        if v in self.adj:
            self.adj.pop(v, -1)
            for u, value in self.adj.items():
                value.pop(v, -1)
                self.aristas.pop((u, v), -1)
                if not self.es_dirigido():
                    self.aristas.pop((v, u), -1)

    def eliminar_arista(self, s: object, t: object) -> None:
        """Si los objetos s y t son vértices del grafo y existe
        una arista de s a t la elimina.
        Si no, no hace nada.

        Args:
            s: vértice de origen de la arista
            t: vértice de destino de la arista
        Returns: None
        """
        if s in self.adj and t in self.adj:
            self.adj[s].pop(t, -1)
            self.aristas.pop((s, t), -1)
            if not self.es_dirigido():
                self.adj[t].pop(s, -1)
                self.aristas.pop((t, s), -1)

    def obtener_arista(self, s: object, t: object) -> Tuple[object, float] or None:
        """Si los objetos s y t son vértices del grafo y existe
        una arista de u a v, devuelve sus datos y su peso en una tupla.
        Si no, devuelve None

        Args:
            s: vértice de origen de la arista
            t: vértice de destino de la arista
        Returns: Una tupla (a,w) con los datos de la arista "a" y su peso
        "w" si la arista existe. None en caso contrario.
        """
        arista = self.adj[s][t]
        return arista["data"], arista["weight"]

    def lista_adyacencia(self, u: object) -> List[object] or None:
        """Si el objeto u es un vértice del grafo, devuelve su lista de adyacencia.
        Si no, devuelve None.

        Args: u vértice del grafo
        Returns: Una lista [v1,v2,...,vn] de los vértices del grafo
        adyacentes a u si u es un vértice del grafo y None en caso
        contrario
        """
        return list(self.adj[u].keys()) if u in self.adj else None

    #### Grados de vértices ####
    def grado_saliente(self, v: object) -> int or None:
        """Si el objeto v es un vértice del grafo, devuelve
        su grado saliente.
        Si no, devuelve None.

        Args: v vértice del grafo
        Returns: El grado saliente (int) si el vértice existe y
        None en caso contrario.
        """
        return len(self.adj[v]) if v in self.adj else None

    def grado_entrante(self, v: object) -> int or None:
        """Si el objeto u es un vértice del grafo, devuelve
        su grado entrante.
        Si no, devuelve None.

        Args: u vértice del grafo
        Returns: El grado entrante (int) si el vértice existe y
        None en caso contrario.
        """
        return sum(1 for u in self.adj if v in self.adj[u]) if v in self.adj else None

    def grado(self, v: object) -> int or None:
        """Si el objeto u es un vértice del grafo, devuelve
        su grado si el grafo no es dirigido y su grado saliente si
        es dirigido.
        Si no pertenece al grafo, devuelve None.

        Args: u vértice del grafo
        Returns: El grado (int) o grado saliente (int) según corresponda
        si el vértice existe y None en caso contrario.
        """
        if v not in self.adj:
            return None
        grado = self.grado_saliente(v) + self.grado_entrante(v)
        return grado // (2 if not self.es_dirigido() else 1)

    def es_conexo(self) -> bool:
        """Devuelve True si el grafo es conexo y False en caso contrario.

        Args: None
        Returns: True si el grafo es conexo y False en caso contrario.
        """
        return self.convertir_a_NetworkX().is_connected()

    #### Algoritmos ####
    def dijkstra(self, origen: object) -> Dict[object, object]:
        """Calcula un Árbol Abarcador Mínimo para el grafo partiendo
        del vértice "origen" usando el algoritmo de Dijkstra. Calcula únicamente
        el árbol de la componente conexa que contiene a "origen".

        Args: origen vértice del grafo de origen
        Returns: Devuelve un diccionario que indica, para cada vértice alcanzable
        desde "origen", qué vértice es su padre en el árbol abarcador mínimo.
        """
        if origen not in self.adj:
            return None
        min_distances = {v: float("inf") for v in self.adj}
        min_distances[origen] = 0
        pq = heapdict()
        pq[origen] = 0
        parents = {origen: None}
        visited = set()
        while pq:
            v, _ = pq.popitem()
            visited.add(v)
            for w in self.adj[v]:
                """Visited nodes take less lookups (1) than weights (3)"""
                """Lookups on visited are"""
                if w not in visited:
                    new_distance = min_distances[v] + self.adj[v][w]["weight"]
                    if new_distance < min_distances[w]:
                        min_distances[w] = new_distance
                        parents[w] = v
                        pq[w] = new_distance
        return parents

    def camino_minimo(self, origen: object, destino: object) -> List[object]:
        if origen not in self.adj and destino not in self.adj:
            print(self.adj)
            return None
        min_distances = {v: float("inf") for v in self.adj}
        min_distances[origen] = 0
        pq = heapdict()
        pq[origen] = 0
        parents = {origen: None}
        visited = set()
        v = None
        while pq and v != destino:
            v, _ = pq.popitem()
            visited.add(v)
            for w in self.adj[v]:
                """Visited nodes take less lookups (1) than weights (3)"""
                """Lookups on visited are"""
                if w not in visited:
                    new_distance = min_distances[v] + self.adj[v][w]["weight"]
                    if new_distance < min_distances[w]:
                        min_distances[w] = new_distance
                        parents[w] = v
                        pq[w] = new_distance
        if parents is None or destino not in parents:
            return None
        path = []
        v = destino
        while v is not None:
            path.append(v)
            v = parents[v]
        return path[::-1]

    def prim(self) -> Dict[object, object]:
        """Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Prim.

        Args: None
        Returns: Devuelve un diccionario que indica, para cada vértice del
        grafo, qué vértice es su padre en el árbol abarcador mínimo.
        """

        padres = {}
        visitados = set()

        coste_min = heapdict()
        coste_min[r.choice(list(self.adj))] = 0

        while coste_min:
            v, _ = coste_min.popitem()
            visitados.add(v)
            for w, value in self.adj[v].items():
                if w not in visitados:
                    if w in padres:
                        if value["weight"] < coste_min[w]:
                            padres[w] = v
                            coste_min[w] = value["weight"]
                    else:
                        padres[w] = v
                        coste_min[w] = value["weight"]
        return padres

    def kruskal_dani(self) -> List[Tuple[object, object]]:
        """Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Kruskal.

        Args: None
        Returns: Devuelve una lista [(s1,t1),(s2,t2),...,(sn,tn)]
        de los pares de vértices del grafo
        que forman las aristas del arbol abarcador mínimo.
        """
        n_vertices = len(self.adj)
        forest = {v: frozenset((v,)) for v in self.adj.keys()}
        path = []
        aristas = sorted(
            self.aristas, key=lambda x: self.aristas[x]["weight"], reverse=True
        )

        while aristas and len(path) < n_vertices - 1:
            u, v = aristas.pop()
            set_u = forest[u]
            set_v = forest[v]
            if set_u != set_v:
                path.append((u, v))
                union = set_u | set_v
                for vertice in union:
                    forest[vertice] = union

        return path

    def kruskal(self) -> List[Tuple[object, object]]:
        """Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Kruskal.

        Args: None
        Returns: Devuelve una lista [(s1,t1),(s2,t2),...,(sn,tn)]
        de los pares de vértices del grafo
        que forman las aristas del arbol abarcador mínimo.
        """

        pass

    def convertir_a_NetworkX(self) -> nx.Graph or nx.DiGraph:
        """Construye un grafo o digrafo de Networkx según corresponda
        a partir de los datos del grafo actual.

        Args: None
        Returns: Devuelve un objeto Graph de NetworkX si el grafo es
        no dirigido y un objeto DiGraph si es dirigido. En ambos casos,
        los vértices y las aristas son los contenidos en el grafo dado.
        """
        G = nx.Graph() if not self.es_dirigido() else nx.DiGraph()
        for v in self:
            G.add_node(v)
        for s, t in self.aristas:
            data, weight = self.obtener_arista(s, t)
            G.add_edge(s, t, data=data, weight=weight)
        return G

    def from_NetworkX(self, G: nx.Graph or nx.DiGraph) -> None:
        """Construye un grafo o digrafo a partir de un objeto Graph
        o DiGraph de NetworkX.

        Args: G objeto Graph o DiGraph de NetworkX
        Returns: None
        """
        self.adj = {}
        self.aristas = {}
        self.dirigido = isinstance(G, nx.DiGraph)
        for v in G:
            self.agregar_vertice(v)
        for s, t in G.edges:
            self.agregar_arista(s, t, data=G[s][t], weight=G[s][t]["weight"])

    def draw_kruskal(
        self,
        pos=None,
        with_labels=False,
        with_weights=False,
        node_size=100,
        edge_width=1,
        arrows=False,
    ):
        G = self.convertir_a_NetworkX()
        pos = nx.spring_layout(G) if pos is None else pos
        kruskal = self.kruskal()
        edge_colors = [
            "g" if e in kruskal or (e[1], e[0]) in kruskal else "b" for e in G.edges
        ]
        weights = nx.get_edge_attributes(G, "weight") if with_weights else None
        nx.draw(
            G,
            pos=pos,
            with_labels=with_labels,
            node_size=node_size,
            width=edge_width,
            arrows=arrows,
            edge_color=edge_colors,
        )
        if with_weights:
            nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=weights)
        plt.show()

    def draw_shortest_path(
        self,
        origen,
        destino,
        pos=None,
        with_labels=False,
        with_weights=False,
        node_size=100,
        edge_width=1,
        arrows=False,
    ):
        path = self.camino_minimo(origen, destino)
        G = self.convertir_a_NetworkX()
        pos = nx.spring_layout(G) if pos is None else pos
        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        weights = nx.get_edge_attributes(G, "weight") if with_weights else None
        nx.draw(
            G,
            pos=pos,
            with_labels=with_labels,
            node_size=node_size,
            width=edge_width,
            arrows=arrows,
        )
        nx.draw_networkx_edges(
            G, pos=pos, edgelist=edges, edge_color="r", width=edge_width * 10
        )
        if with_weights:
            nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=weights)
        nx.draw_networkx_nodes(
            G, pos=pos, nodelist=[origen, destino], node_color="purple", node_size=10
        )
        plt.show()

    def save_graph(self, path="grafo.txt"):
        grafo = {
            "adj": self.adj,
            "aristas": self.aristas,
            "dirigido": self.es_dirigido(),
        }
        with open(path, "w", encoding="latin-1") as f:
            f.write(str(grafo))

    def load_graph(self, path="grafo.json"):
        with open(path, "r", encoding="latin-1") as f:
            js = eval(f.read())
        self.adj = js["adj"]
        self.aristas = js["aristas"]
        self.dirigido = js["dirigido"]


if __name__ == "__main__":
    graph = Grafo()
    # graph.agregar_vertice("A")
    # graph.agregar_vertice("B")
    # graph.agregar_vertice("C")
    # graph.agregar_vertice("D")
    # graph.agregar_vertice("E")
    # graph.agregar_vertice("V")
    # graph.agregar_vertice("W")
    # graph.agregar_vertice("X")
    n_vertices = 10
    for v in range(1, n_vertices):
        graph.agregar_vertice(v)

    for v in range(1, n_vertices):
        for w in range(1, n_vertices):
            if v != w and r.random() < 0.5:
                graph.agregar_arista(v, w, data=None, weight=r.randint(1, 100))

    # inicio = time.time()
    # graph.prim()
    # print("time:", time.time() - inicio)
    # inicio = time.time()
    # graph.prim_dani()
    # print("time:", time.time() - inicio)
    # graph.agregar_arista("A", "B", weight=5, data="A-B")
    # graph.agregar_arista("A", "V", weight=3, data="A-V")
    # graph.agregar_arista("A", "D", weight=6, data="A-D")
    # graph.agregar_arista("A", "E", weight=8, data="A-E")
    # graph.agregar_arista("V", "B", weight=9, data="V-B")
    # graph.agregar_arista("V", "C", weight=7, data="V-B")
    # graph.agregar_arista("B", "D", weight=1, data="B-D")
    # graph.agregar_arista("B", "C", weight=2, data="B-D")
    # graph.agregar_arista("C", "E", weight=5, data="C-E")
    # graph.agregar_arista("D", "E", weight=1, data="D-E")
    # graph.agregar_arista("X", "W", weight=4, data="D-W")

    # graph.draw_kruskal(
    #     with_labels=True, node_size=500, edge_width=2, arrows=True, with_weights=True
    # )

    # graph.draw_shortest_path(
    #     "A",
    #     "E",
    #     with_labels=True,
    #     node_size=500,
    #     edge_width=2,
    #     with_weights=True,
    # )
