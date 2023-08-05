def obtener_indices_de_matriz_en_lista(matriz, indices_lista):
    matriz_plana = matriz.flatten()
    resultados = matriz_plana[indices_lista]
    return resultados