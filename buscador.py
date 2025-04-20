import os

def buscar_palabra_en_archivo(archivo_path: str, palabra: str, buffer_size: int = 8*1024*1024):
    palabra = palabra.lower().encode('utf-8')  # buscamos en bytes, insensible a mayusculas
    palabra_len = len(palabra)

    posiciones = []  # donde encontraremos la palabra

    try:
        with open(archivo_path, 'rb') as f:
            offset = 0
 import os

def buscar_palabra_en_archivo(archivo_path: str, palabra: str, buffer_size: int = 8*1024*1024):
    palabra = palabra.lower().encode('utf-8')  # buscamos en bytes, insensible a mayusculas
    palabra_len = len(palabra)

    posiciones = []  # donde encontraremos la palabra

    try:
        with open(archivo_path, 'rb') as f:
            offset = 0
            buffer_anterior = b''

            while True:
                buffer_actual = f.read(buffer_size)
                if not buffer_actual:
                    break

                # Concatenar el final del buffer anterior para no perder palabras partidas
                buffer_completo = buffer_anterior + buffer_actual

                # Buscar todas las apariciones
                idx = buffer_completo.lower().find(palabra)
                while idx != -1:
                    posicion_real = offset - len(buffer_anterior) + idx
                    posiciones.append(posicion_real)

                    idx = buffer_completo.lower().find(palabra, idx + 1)

                # Guardar los ultimos bytes por si la palabra se parte entre bloques
                buffer_anterior = buffer_completo[-(palabra_len - 1):]

                offset += len(buffer_actual)

    except FileNotFoundError:
        print(f"Archivo no encontrado: {archivo_path}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

    return posiciones

def main():
    print('=== Buscador de Palabras ULTRA Optimizado ===')
    archivo = input('Ruta del archivo a buscar: ').strip()
    palabra = input('Palabra a buscar (ignora mayúsculas/minúsculas): ').strip()

    print(f"\nBuscando la palabra '{palabra}' en el archivo '{archivo}'...\n")
    posiciones = buscar_palabra_en_archivo(archivo, palabra)

    if posiciones:
        print(f"\nEncontrado {len(posiciones)} veces:")
        for idx, pos in enumerate(posiciones, start=1):
            print(f"{idx}. Posición byte: {pos}")
    else:
        print("\nNo se encontró la palabra en el archivo.")

if __name__ == '__main__':
    main()
