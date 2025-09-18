import os
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description="Extractor de archivos")
parser.add_argument("archivo_entrada", help="Archivo a procesar", type=Path)
args = parser.parse_args()

Nmagicos = {
    b'\x49\x44\x33\x02': "mp3",
    b'\x49\x44\x33\x03': "mp3",
    b'\x49\x44\x33\x04': "mp3",
    b'\xFF\xFB\x90\x64': "mp3",
    b'\xFF\xFA\x92\xC4': "mp3",
    b'\xFF\xF3\x40\xC4': "mp3",
    b'\xFF\xF2\x48\x80': "mp3",
    b'\xFF\xD8\xFF\xE0': "jpg",
    b'\xFF\xD8\xFF\xDB': "jpg",
    b'\xFF\xD8\xFF\xEE': "jpg",
    b'\xFF\xD8\xFF\xE1': "jpg",
    b'\x50\x4B\x03\x04\x14\x03': "zip",
    b'\x1A\x45\xDF\xA3\x01\x00\x00\x00': "webm",
    b'\x4F\x67\x67\x53\x00\x02': "ogv"

}

def cdir(carpeta):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)


def buscarsig(datos, posi_actual, firmas):
    proxima_pos = len(datos)
    for firma in firmas.keys():
        pos = datos.find(firma, posi_actual + 1)
        if pos != -1 and pos < proxima_pos:
            proxima_pos = pos
    return proxima_pos

archivo_entrada = args.archivo_entrada
if not archivo_entrada.exists():
    print(f"Archivo no encontrado: {archivo_entrada}")
    exit(1)

csalida = Path("extraidos")
cdir(csalida)

with archivo_entrada.open("rb") as f:
    datos = f.read()

posi = 0
contador = 1
mp3e = csalida / "archivo_mp3.mp3"
jpgc = 0

while posi < len(datos):
    encontrado = False
    for firma, tipo in Nmagicos.items():
        idx = datos.find(firma, posi)
        if idx == posi:
            siguiente_pos = buscarsig(datos, posi, Nmagicos)
            contenido = datos[posi:siguiente_pos]

            if tipo == "ogv":
                pass
            elif tipo == "mp3":
                with mp3e.open("ab") as mp3_out:
                    mp3_out.write(contenido)
            elif tipo == "jpg":
                if jpgc < 4:
                    jpgc += 1
                else:
                    nombre = csalida / f"archivo_{contador}.{tipo}"
                    nombre.write_bytes(contenido)
                    contador += 1
            else:
                nombre = csalida / f"archivo_{contador}.{tipo}"
                nombre.write_bytes(contenido)
                contador += 1

            posi = siguiente_pos
            encontrado = True
            break
    if not encontrado:
        posi += 1

print(f"Extraccion completada. Archivos guardados en: {csalida}")
