import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("Archivo", help="Primer archivo", type=Path)

Patron = {
    "jpg": {"head": b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01", "footer": b"\xff\xd9"},
    "zip": {"head": b"\x50\x4b\x03\x04", "footer": b"\x50\x4b\x05\x06"},
    "mp3": {"head": b"\x49\x44\x33", "footer": None},  #ID3v2
    "ogv": {"head": b"\x4f\x67\x67\x53\x00\x02\x00\x00\x00", "footer": None},
    "webm": {"head": b"\x1a\x45\xdf\xa3", "footer": None}
}

Cola = ["webm","ogv","mp3","zip","jpg"]
nbyt = 1024  # 1 KB mínimo para guardar archivo encontrado

def extraer(extension, datos, inicio, fin, contador):
    if fin - inicio < nbyt: # Se verifica nbyt 
        return
    salida = Path(f"extraido_{contador}.{extension}")
    while salida.exists():
        contador += 1
        salida = Path(f"extraido_{contador}.{extension}")
    with salida.open("wb") as f:
        f.write(datos[inicio:fin])
    print(f"{salida} ({fin - inicio} bytes)")

def buscar(archivo: Path):
    with archivo.open("rb") as f: 
        datos = f.read()
    contador = 0
    archivosEncontrados = 0

    for tipo in Cola:
        patron = Patron[tipo]["head"]
        pos = datos.find(patron) # Para cada tipo de archivo se busca su head
        while pos != -1:
            footer = Patron[tipo]["footer"]
            if footer:
                fin = datos.find(footer, pos + len(patron))
                if fin != -1:
                    fin += len(footer)  # Incluir el footer
                else:
                    fin = len(datos)
            else:
                # Se pasa hasta la siguiente cabecera de otro tipo de archivo
                fin = len(datos)
                for otro, info in Patron.items():
                    if otro == tipo:
                        continue
                    n = datos.find(info["head"], pos + len(patron))
                    if n != -1 and n < fin:
                        fin = n
            extraer(tipo, datos, pos, fin, contador) # Patron valido llama a extraer para guardar
            contador += 1
            archivosEncontrados += 1
            pos = datos.find(patron, fin)
    print("-------------------------------------\n")
    if archivosEncontrados == 0:
        print("NO se encontraron archivos")

def detectar(archivo):
    CarpetaActual = Path('.').resolve()
    print(f"La ruta actual es: {CarpetaActual}\n")
    if archivo.exists():
        print(f"El archivo fue encontrado: {archivo}\n")
        return True
    else:
        print("NO se encontró el archivo")
        return False

def main():
    args = parser.parse_args()
    if detectar(args.Archivo):
        buscar(args.Archivo)

main()