import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("archivo", help="Archivo combinado", type=Path)
parser.add_argument("offsets", nargs="+", type=str, help="Desplazamientos y tipos de archivo en formato offset:extension")
args = parser.parse_args()

# Procesar los argumentos
archivos_info = []
for arg in args.offsets:
    if ':' in arg:
        offset_str, extension = arg.split(':', 1)
        archivos_info.append((int(offset_str), extension))
    else:
        # Si no hay extensión, usar .bin por defecto
        archivos_info.append((int(arg), "bin"))

# Abrimos archivo fuente
with args.archivo.open("rb") as f:
    # Tamaño total del archivo
    f.seek(0, 2)
    tam_total = f.tell()

    # Recorremos offsets en orden dado
    for i, (offset, extension) in enumerate(archivos_info):
        # Determinar el final de este segmento
        if i + 1 < len(archivos_info):
            fin = archivos_info[i + 1][0]  # Siguiente offset
        else:
            fin = tam_total

        # Leer bloque
        f.seek(offset)
        data = f.read(fin - offset)

        # Guardar en archivo de salida con extensión correcta
        nombre = f"parte{i}.{extension}"
        with open(nombre, "wb") as out:
            out.write(data)

        print(f"Guardado {nombre} (offset {offset} -> {fin})")