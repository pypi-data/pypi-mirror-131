import numpy as np
import scipy.stats as st


def agrega_categoria_entropia(diccionario_entropia, categoria, datos):
    nuevos_datos = np.array(datos)
    if categoria not in diccionario_entropia:
        diccionario_entropia[categoria] = st.entropy(nuevos_datos)


def modificar_matriz_para_evitar_divergencia_infinita(datos):
    nuevos_datos = np.copy(datos)
    indices_con_valores_0 = np.argwhere(nuevos_datos == 0)

    for indices in indices_con_valores_0:
        nuevos_datos[indices[0], indices[1]] = 1

    return nuevos_datos



