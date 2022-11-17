from typing import List, Tuple, Dict
import networkx as nx
import sys

import heapq

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
        self.adj[v] = {}

    def agregar_arista(self, s: object, t: object, data: object, weight: float = 1) -> None:
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
        if s in self.adj and t in self.adj:
            self.adj[s][t] = {
                "data": data,
                "weight": weight
            }
            if not self.es_dirigido():
                self.adj[t][s] = {
                "data": data,
                "weight": weight
                }


    def eliminar_vertice(self, v: object) -> None:
        """Si el objeto v es un vértice del grafo lo elimiina.
        Si no, no hace nada.

        Args: v vértice que se quiere eliminar
        Returns: None
        """
        self.adj.pop(v, -1)
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
        if self.es_dirigido():
            self.adj[t].pop(s, -1)

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
        grado = self.grado_saliente(v)+self.grado_entrante(v)
        return grado//(2 if not self.es_dirigido() else 1) if v in self.adj else None

    #### Algoritmos ####
    def dijkstra(self, origen: object) -> Dict[object, object]:
        """Calcula un Árbol Abarcador Mínimo para el grafo partiendo
        del vértice "origen" usando el algoritmo de Dijkstra. Calcula únicamente
        el árbol de la componente conexa que contiene a "origen".

        Args: origen vértice del grafo de origen
        Returns: Devuelve un diccionario que indica, para cada vértice alcanzable
        desde "origen", qué vértice es su padre en el árbol abarcador mínimo.
        """
        pass

    def camino_minimo(self, origen: object, destino: object) -> List[object]:
        pass

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
        pass

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
        for s, t in self.aristas():
            G.add_edge(s, t)
