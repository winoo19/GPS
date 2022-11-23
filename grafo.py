from typing import List, Tuple, Dict
import networkx as nx
import sys
import matplotlib.pyplot as plt
import random

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
        self.aristas: dict[object, dict[object, dict]] = {}

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
                self.adj[t][s] = {"data": data, "weight": weight}
                self.aristas[(t, s)] = {"data": data, "weight": weight}

    def eliminar_vertice(self, v: object) -> None:
        """Si el objeto v es un vértice del grafo lo elimiina.
        Si no, no hace nada.

        Args: v vértice que se quiere eliminar
        Returns: None
        """
        self.adj.pop(v, -1)
        for k, _ in self.aristas.items():
            if v in k:
                self.aristas.pop(k)
        for _, value in self.adj.items():
            value.pop(v, -1)

    def eliminar_arista(self, s: object, t: object) -> None:
        """Si los objetos s y t son vértices del grafo y existe
        una arista de u a v la elimina.
        Si no, no hace nada.

        Args:
            s: vértice de origen de la arista
            t: vértice de destino de la arista
        Returns: None
        """
        self.adj[s].pop(t, -1)
        self.aristas.pop((s, t), -1)
        if self.es_dirigido():
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
        """Si el objeto u es un vértice del grafo, devuelve
        su grado saliente.
        Si no, devuelve None.

        Args: u vértice del grafo
        Returns: El grado saliente (int) si el vértice existe y
        None en caso contrario.
        """
        return len(self.adj[v].keys()) if v in self.adj else None

    def grado_entrante(self, v: object) -> int or None:
        """Si el objeto u es un vértice del grafo, devuelve
        su grado entrante.
        Si no, devuelve None.

        Args: u vértice del grafo
        Returns: El grado entrante (int) si el vértice existe y
        None en caso contrario.
        """
        return sum(1 for _, a in self.adj if v in a) if v in self.adj else None

    def grado(self, v: object) -> int or None:
        """Si el objeto u es un vértice del grafo, devuelve
        su grado si el grafo no es dirigido y su grado saliente si
        es dirigido.
        Si no pertenece al grafo, devuelve None.

        Args: u vértice del grafo
        Returns: El grado (int) o grado saliente (int) según corresponda
        si el vértice existe y None en caso contrario.
        """
        grado = self.grado_saliente(v) + self.grado_entrante(v)
        return grado // (2 if not self.es_dirigido() else 1) if v in self.adj else None

    def es_connexo(self) -> bool:
        """Devuelve True si el grafo es conexo y False en caso contrario.

        Args: None
        Returns: True si el grafo es conexo y False en caso contrario.
        """
        return self.convertir_a_NetworkX().is_connected()

    #### Algoritmos ####
    def dijkstra(self, origen: object, destino: object) -> Dict[object, object]:
        """Calcula un Árbol Abarcador Mínimo para el grafo partiendo
        del vértice "origen" usando el algoritmo de Dijkstra. Calcula únicamente
        el árbol de la componente conexa que contiene a "origen".

        Args: origen vértice del grafo de origen
        Returns: Devuelve un diccionario que indica, para cada vértice alcanzable
        desde "origen", qué vértice es su padre en el árbol abarcador mínimo.
        """
        if origen not in self.adj or destino not in self.adj:
            return None
        min_distances = {v: float("inf") for v in self.adj}
        min_distances[origen] = 0
        pq = heapdict()
        pq[origen] = 0
        parents = {origen: None}
        while pq:
            v, _ = pq.popitem()
            if v == destino:
                return parents
            for w in self.adj[v]:
                new_distance = min_distances[v] + self.adj[v][w]["weight"]
                if new_distance < min_distances[w]:
                    min_distances[w] = new_distance
                    parents[w] = v
                    pq[w] = new_distance
        return parents

    def camino_minimo(self, origen: object, destino: object) -> List[object]:
        parents = self.dijkstra(origen, destino)
        if parents is None:
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
        pass

    def kruskal(self) -> List[Tuple[object, object]]:
        """Calcula un Árbol Abarcador Mínimo para el grafo
        usando el algoritmo de Kruskal.

        Args: None
        Returns: Devuelve una lista [(s1,t1),(s2,t2),...,(sn,tn)]
        de los pares de vértices del grafo
        que forman las aristas del arbol abarcador mínimo.
        """
        n_vertices = len(self.adj)
        forest = set(map(lambda x: frozenset((x,)), self.adj.keys()))
        path = []
        aristas = sorted(
            self.aristas, key=lambda x: self.aristas[x]["weight"], reverse=True
        )

        while len(path) < n_vertices - 1:
            u, v = aristas.pop()
            set_u = set_v = None

            for tree in forest:
                if u in tree:
                    set_u = tree
                if v in tree:
                    set_v = tree
                if set_u and set_v:
                    break

            if set_u != set_v:
                path.append((u, v))
                forest.remove(set_u)
                forest.remove(set_v)
                forest.add(set_u | set_v)

        return path

    #### NetworkX ####
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

    def NetworkX_a_grafo(self, G: nx.Graph or nx.DiGraph) -> None:
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
            self.agregar_arista(s, t, data=G[s][t])

    def kruskal_to_graph(self, aristas: List[Tuple[object, object]]) -> nx.Graph:
        """Construye un grafo a partir de una lista de aristas.

        Args: aristas lista de aristas [(s1,t1),(s2,t2),...,(sn,tn)]
        Returns: Devuelve un objeto Graph con los vértices y aristas
        de la lista dada.
        """
        G = nx.Graph()
        for s, t in aristas:
            data, weight = self.obtener_arista(s, t)
            G.add_node(s)
            G.add_node(t)
            G.add_edge(s, t, data=data, weight=weight)
        return G

    def draw(self, draw_weights=False, node_size=5, width=0.5, arrows=False, pos=None, nb=False):
        """Dibuja el grafo usando networkx.
        Args: None
        Returns: None
        """
        if not nb:
            plt.plot()
        G = self.convertir_a_NetworkX()
        if not pos:
            pos = nx.spring_layout(G)
        nx.draw(G, pos=pos, with_labels=True, node_size=node_size, width=width, arrows=arrows)
        if draw_weights:
            labels = nx.get_edge_attributes(G, "weight")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        if not nb:
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
    for i in range(10):
        graph.agregar_vertice(i)

    for _ in range(15):
        graph.agregar_arista(
            random.randint(0, 9),
            random.randint(0, 9),
            None,
            round(random.random() * 10) + 1,
        )

    parents = graph.dijkstra(1, 5)
    path = []
    v = 5
    while v is not None:
        path.append(v)
        v = parents[v]
    print(path[::-1])
    graph.draw(True)

    # print("Minimum span tree", graph.kruskal())
    # G = graph.convertir_a_NetworkX()
    # pos = nx.spring_layout(G)
    # K = graph.kruskal_to_graph(graph.kruskal())
    # plot = plt.plot()
    # nx.draw(G, pos)
    # nx.draw(K, pos, edge_color="r")
    # labels = nx.get_edge_attributes(G, "weight")
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    # plt.show()
