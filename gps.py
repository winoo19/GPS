import grafo
import Levenshtein
import pandas as pd


def input_origin(direcciones):
    def str_dist(x):
        d = Levenshtein.distance(x, origin)
        common = set(x.split()).intersection(set(origin.split()))
        return d - len(common) - 2 * int(origin in x)

    origin = input("Introduce direccion de origen: ")
    direcciones["lev"] = direcciones["direccion_clean"].apply(lambda x: str_dist(x))
    direcciones = direcciones.sort_values("lev")
    return direcciones.iloc[0]


def clean_direccion(direccion):
    """convierte a minusculas y reemplaza acentos"""
    direccion = direccion.lower()
    direccion = direccion.replace("á", "a")
    direccion = direccion.replace("é", "e")
    direccion = direccion.replace("í", "i")
    direccion = direccion.replace("ó", "o")
    direccion = direccion.replace("ú", "u")
    return direccion


def find_closest_vertex(origin: pd.Series):
    """encuentra el vertice mas cercano a una direccion"""
    global cruces

    dist = lambda x: (origin["x"] - x["x"]) ** 2 + (origin["y"] - x["y"]) ** 2

    cruces["dist"] = cruces[
        (cruces["id_via"] == origin["id_via"])
        | (cruces["id_via_cruzada"] == origin["id_via"])
    ].apply(dist, axis=1)
    cruce = cruces.sort_values("dist").iloc[0]
    return (int(cruce["x"]), int(cruce["y"]))


madrid = grafo.Grafo()
madrid.load_graph("grafos/plano_de_madrid_tsp2.txt")
direcciones = pd.read_csv("data/direcciones_clean.csv")
cruces = pd.read_csv("data/cruces_clean.csv")
direcciones["direccion_clean"] = direcciones["Direccion completa"].apply(
    clean_direccion
)
origin = input_origin(direcciones)
print("Origen: ", origin)

destination = input_origin(direcciones)
print("Destino: ", destination)

origin_vertex = find_closest_vertex(origin)
destination_vertex = find_closest_vertex(destination)

# camino = madrid.camino_minimo(origin_vertex, destination_vertex)

madrid.draw_shortest_path(
    origin_vertex,
    destination_vertex,
    pos={k: k for k in madrid.adj.keys()},
    node_size=0.1,
    arrows=False,
    edge_width=0.1,
)

# print("El camino mas corto es: ", camino)


# print("Origen: ", origin_vertex)
# print("Destino: ", destination_vertex)
