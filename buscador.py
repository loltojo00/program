import os
from tqdm import tqdm

# --- Funciones auxiliares ---
def cargar_diccionario(ruta_diccionario):
    palabras = set()
    with open(ruta_diccionario, 'r', encoding='utf-8') as f:
        for linea in f:
            palabra = linea.strip().lower()
            if palabra:
                palabras.add(palabra)
    return palabras

# --- Busqueda simple ---
def buscar_palabra_simple(ruta_archivo, palabra_buscar):
    palabra_bytes = palabra_buscar.lower().encode('utf-8')
    tam_palabra = len(palabra_bytes)

    print(f"\nBuscando la palabra '{palabra_buscar}' en el archivo '{ruta_archivo}'...\n")
    posiciones = []

    with open(ruta_archivo, 'rb') as f:
        contenido = f.read()

    idx = 0
    while True:
        idx = contenido.lower().find(palabra_bytes, idx)
        if idx == -1:
            break
        posiciones.append(idx)
        idx += tam_palabra

    if posiciones:
        print(f"\nEncontrado {len(posiciones)} veces:")
        for i, pos in enumerate(posiciones, 1):
            print(f"{i}. Posición byte: {pos}")
    else:
        print("\nNo se encontró la palabra.")

# --- Busqueda multiple ---
def buscar_palabras_diccionario(ruta_archivo, ruta_diccionario):
    palabras = cargar_diccionario(ruta_diccionario)
    if not palabras:
        print("\nEl diccionario está vacío.")
        return

    print(f"\nBuscando {len(palabras)} palabras en el archivo '{ruta_archivo}'...\n")

    resultados = {palabra: [] for palabra in palabras}

    with open(ruta_archivo, 'rb') as f:
        contenido = f.read()

    contenido_lower = contenido.lower()

    for palabra in tqdm(palabras, desc="Buscando", unit="palabra"):
        palabra_bytes = palabra.encode('utf-8')
        tam_palabra = len(palabra_bytes)

        idx = 0
        while True:
            idx = contenido_lower.find(palabra_bytes, idx)
            if idx == -1:
                break
            resultados[palabra].append(idx)
            idx += tam_palabra

    # Mostrar resultados
    for palabra, posiciones in resultados.items():
        if posiciones:
            print(f"\nPalabra '{palabra}' encontrada {len(posiciones)} veces:")
            for i, pos in enumerate(posiciones, 1):
                print(f"{i}. Posición byte: {pos}")

# --- Programa principal ---
def main():
    print('=== Buscador de Palabras ULTRA Optimizado v2 ===\n')

    while True:
        print("\u00bfModo de búsqueda?")
        print("1. Buscar una palabra")
        print("2. Buscar varias palabras desde un archivo (diccionario)")
        modo = input("Elige (1/2): ").strip()

        if modo in {'1', '2'}:
            break
        print("Entrada inválida. Debes elegir 1 o 2.")

    ruta_archivo = input("Ruta del archivo donde buscar: ").strip()

    if not os.path.isfile(ruta_archivo):
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        return

    if modo == '1':
        palabra = input("Palabra a buscar (ignora mayúsculas/minúsculas): ").strip()
        if palabra:
            buscar_palabra_simple(ruta_archivo, palabra)
        else:
            print("No ingresaste una palabra válida.")

    elif modo == '2':
        ruta_diccionario = input("Ruta del archivo de diccionario (.txt): ").strip()
        if not os.path.isfile(ruta_diccionario):
            print(f"Error: No se encontró el diccionario '{ruta_diccionario}'")
            return
        buscar_palabras_diccionario(ruta_archivo, ruta_diccionario)

if __name__ == '__main__':
    main()
