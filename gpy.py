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
    return direcciones.iloc[:5]


def clean_direccion(direccion):
    """convierte a minusculas y reemplaza acentos"""
    direccion = direccion.lower()
    direccion = direccion.replace("á", "a")
    direccion = direccion.replace("é", "e")
    direccion = direccion.replace("í", "i")
    direccion = direccion.replace("ó", "o")
    direccion = direccion.replace("ú", "u")
    return direccion


madrid = grafo.Grafo()
madrid.load_graph("grafos/plano_de_madrid_tsp2.txt")
direcciones = pd.read_csv("data/direcciones_clean.csv")
direcciones["direccion_clean"] = direcciones["Direccion completa"].apply(
    clean_direccion
)
matches = input_origin(direcciones)
print(matches)
