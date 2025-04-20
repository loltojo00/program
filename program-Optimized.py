import os
import string
import sys
from tqdm import tqdm
from typing import Literal, Dict, Final

# --- Constantes ---
# Usar un diccionario para mapear tipos a conjuntos de caracteres mejora la legibilidad
# y facilita la extensión si se necesitaran más tipos.
# Convertimos a bytes inmediatamente para evitar hacerlo repetidamente.
CHARSETS: Final[Dict[str, bytes]] = {
    'numeros': string.digits.encode('ascii'),
    'letras': string.ascii_letters.encode('ascii'),
    'ambos': (string.ascii_letters + string.digits).encode('ascii'),
}

# Tamaño del búfer optimizado para operaciones de I/O y uso de memoria.
# Usar potencias de 2 suele ser bueno, 8MB es un buen punto de partida.
BUFFER_SIZE: Final[int] = 8 * 1024 * 1024 # 8 MiB

# --- Función Optimizada ---

def generar_caracteres_optimizado(
    tipo: Literal['numeros', 'letras', 'ambos'],
    cantidad: int,
    archivo_salida: str
) -> None:
    """
    Genera un archivo con una cantidad específica de caracteres aleatorios
    del tipo especificado, usando optimizaciones significativas.

    Args:
        tipo: El tipo de caracteres a generar ('numeros', 'letras', 'ambos').
        cantidad: El número total de caracteres a generar.
        archivo_salida: La ruta del archivo donde se guardarán los caracteres.

    Raises:
        ValueError: Si el tipo de caracteres no es válido.
        IOError: Si ocurre un error al escribir en el archivo.
    """
    if tipo not in CHARSETS:
        raise ValueError(f"Tipo inválido: '{tipo}'. Use 'numeros', 'letras' o 'ambos'.")
    if cantidad < 0:
        raise ValueError("La cantidad de caracteres no puede ser negativa.")
    if not archivo_salida:
        raise ValueError("El nombre del archivo de salida no puede estar vacío.")

    caracteres: bytes = CHARSETS[tipo]
    charset_len: int = len(caracteres)

    # --- Optimización Clave: Tabla de Traducción ---
    # Precalculamos una tabla de traducción de 256 bytes.
    # Cada byte posible (0-255) se mapea a un carácter válido de nuestro set,
    # usando el módulo (%). Esto evita el bucle Python y el cálculo del módulo
    # para *cada* byte generado por os.urandom dentro del bucle principal.
    # La operación bytes.translate() es extremadamente rápida (implementada en C).
    translation_table: bytes = bytes(caracteres[i % charset_len] for i in range(256))

    try:
        with open(archivo_salida, 'wb') as f:
            # Usamos tqdm para la barra de progreso, configurada para bytes.
            # El total es la cantidad de bytes a escribir.
            with tqdm(total=cantidad, desc='Generando', unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                bytes_escritos = 0
                while bytes_escritos < cantidad:
                    # Determinamos cuántos bytes generar en esta iteración
                    bytes_a_generar = min(BUFFER_SIZE, cantidad - bytes_escritos)

                    # 1. Generar bytes aleatorios (rápido, desde el OS)
                    random_bytes: bytes = os.urandom(bytes_a_generar)

                    # 2. Traducir los bytes aleatorios a nuestro conjunto de caracteres usando la tabla
                    #    Esta es la operación más optimizada.
                    bloque_traducido: bytes = random_bytes.translate(translation_table)

                    # 3. Escribir el bloque traducido al archivo (operación de I/O en bloque)
                    f.write(bloque_traducido)

                    # Actualizar contador y barra de progreso
                    bytes_escritos += len(bloque_traducido) # Usar len real por si acaso
                    pbar.update(len(bloque_traducido))

    except IOError as e:
        print(f"\nError al escribir en el archivo '{archivo_salida}': {e}", file=sys.stderr)
        # Opcional: eliminar archivo parcialmente escrito si falla
        # if os.path.exists(archivo_salida):
        #     os.remove(archivo_salida)
        raise # Re-lanzar la excepción para que el вызывающий sepa que falló

# --- Función Principal Mejorada ---

def main() -> None:
    """Función principal para interactuar con el usuario y llamar al generador."""
    print('=== Generador de Caracteres ULTRA Optimizado v2 ===')

    # Validación de entrada más robusta
    while True:
        tipo = input('¿Qué quieres generar? (numeros/letras/ambos): ').strip().lower()
        if tipo in CHARSETS:
            break
        print("Entrada inválida. Por favor, elige 'numeros', 'letras' o 'ambos'.")

    while True:
        try:
            cantidad_str = input('¿Cuántos caracteres quieres generar? (ej: 1000, 5M, 1G): ').strip().upper()
            multiplier = 1
            if cantidad_str.endswith('K'):
                multiplier = 1024
                cantidad_str = cantidad_str[:-1]
            elif cantidad_str.endswith('M'):
                multiplier = 1024 * 1024
                cantidad_str = cantidad_str[:-1]
            elif cantidad_str.endswith('G'):
                multiplier = 1024 * 1024 * 1024
                cantidad_str = cantidad_str[:-1]

            cantidad = int(float(cantidad_str) * multiplier) # Permitir decimales como 0.5G
            if cantidad >= 0:
                break
            else:
                print("La cantidad no puede ser negativa.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número (puedes usar K, M, G).")

    while True:
        archivo_salida = input('Nombre del archivo de salida (ej: resultado.txt): ').strip()
        if archivo_salida:
            break
        print("El nombre del archivo no puede estar vacío.")

    try:
        print(f"Generando {cantidad} caracteres de tipo '{tipo}' en '{archivo_salida}'...")
        generar_caracteres_optimizado(tipo, cantidad, archivo_salida)
        print(f'\n¡Archivo "{archivo_salida}" ({cantidad} bytes) creado exitosamente!')
    except (ValueError, IOError) as e:
        print(f"\nError durante la generación: {e}", file=sys.stderr)
        sys.exit(1) # Salir con código de error

if __name__ == '__main__':
    main()