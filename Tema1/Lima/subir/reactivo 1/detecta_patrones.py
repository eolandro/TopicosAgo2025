import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("archivo", help="Archivo fuente a analizar", type=Path)
args = parser.parse_args()

# Patrones
PATRON_MP3 = [b"\x49", b"\x44", b"\x33"]
PATRON_WEBM = [b"\x1A", b"\x45", b"\xDF", b"\xA3"]
PATRRON_ZIP = [b"\x50", b"\x4B", b"\x03", b"\x04"]
PATRONES_JPG = [
    [b"\xFF", b"\xD8", b"\xFF", b"\xE0"],
    [b"\xFF", b"\xD8", b"\xFF", b"\xDB"]
]

# Patrón y secuencia para OGV (OggS)
PATRON_OGV = [b"\x4F", b"\x67", b"\x67", b"\x53"]
SECUENCIA_OGV = [b"\x00", b"\x02", b"\x00", b"\x00", b"\x00", b"\x00", b"\x00", b"\x00", b"\x00", b"\x00"]

MAX_ARCHIVOS = {"jpg": 2, "ogv": 2, "webm": 1, "zip": 1, "mp3": 1}
contadores = {"jpg": 0, "ogv": 0, "webm": 0, "zip": 0, "mp3": 0}

Cola = []
nbyte = 0
ogv_offsets = []  # Para trackear offsets OGV encontrados


def total_encontrados():
    return sum(contadores.values())


def verificar_mp3(offset):
    try:
        with args.archivo.open("rb") as f:
            f.seek(offset) 
            header = f.read(6)
            if len(header) < 6:
                return False
            version_mayor = header[3]
            return version_mayor in [2, 3, 4]
    except:
        return False


def verificar_jpg():
    """Verifica si los últimos bytes coinciden con algún patrón JPG"""
    for patron in PATRONES_JPG:
        patron_len = len(patron)
        if len(Cola) >= patron_len:
            coincide = True
            for i in range(patron_len):
                if Cola[-(patron_len - i)] != patron[i]:
                    coincide = False
                    break
            if coincide:
                return patron_len
    return 0


def verificar_ogv(offset):
    """Verifica la secuencia OGV después del patrón OggS"""
    try:
        with args.archivo.open("rb") as f:
            f.seek(offset + 4)  # después de "OggS"
            secuencia = f.read(10)
            if len(secuencia) < 10:
                return False
            for i in range(10):
                if secuencia[i] != SECUENCIA_OGV[i][0]:
                    return False
            return True
    except:
        return False


def es_offset_ogv_valido(offset):
    """Verifica que el offset OGV no esté demasiado cerca de otros"""
    for existing_offset in ogv_offsets:
        if abs(offset - existing_offset) < 10000:
            return False
    return True


if args.archivo.exists():
    with args.archivo.open("rb") as f:
        Cola = []
        nbyte = 0
        Terminado = False

        while not Terminado:
            bt = f.read(1)
            if not bt:
                break

            nbyte += 1
            Cola.append(bt)

            if len(Cola) > 4:
                Cola.pop(0)

            # --- Verificar JPG ---
            if contadores["jpg"] < MAX_ARCHIVOS["jpg"] and len(Cola) >= 3:
                patron_len = verificar_jpg()
                if patron_len > 0:
                    offset = nbyte - patron_len
                    print(f"{offset}:jpg")
                    contadores["jpg"] += 1
                    if total_encontrados() == sum(MAX_ARCHIVOS.values()):
                        Terminado = True
                    continue

            # --- Verificar WEBM ---
            if contadores["webm"] < MAX_ARCHIVOS["webm"] and len(Cola) == 4:
                if Cola == PATRON_WEBM:
                    offset = nbyte - 4
                    print(f"{offset}:webm")
                    contadores["webm"] += 1
                    if total_encontrados() == sum(MAX_ARCHIVOS.values()):
                        Terminado = True
                    continue

            # --- Verificar ZIP ---
            if contadores["zip"] < MAX_ARCHIVOS["zip"] and len(Cola) == 4:
                if Cola == PATRRON_ZIP:
                    offset = nbyte - 4
                    print(f"{offset}:zip")
                    contadores["zip"] += 1
                    if total_encontrados() == sum(MAX_ARCHIVOS.values()):
                        Terminado = True
                    continue

            # --- Verificar MP3  ---
            if contadores["mp3"] < MAX_ARCHIVOS["mp3"] and len(Cola) >= 3:
                ultimos_3 = Cola[-3:] if len(Cola) > 3 else Cola
                if ultimos_3 == PATRON_MP3:
                    offset = nbyte - 3
                    if verificar_mp3(offset):
                        print(f"{offset}:mp3")
                        contadores["mp3"] += 1
                        if total_encontrados() == sum(MAX_ARCHIVOS.values()):
                            Terminado = True
                        continue

            # --- Verificar OGV  ---
            if contadores["ogv"] < MAX_ARCHIVOS["ogv"] and len(Cola) == 4:
                if Cola == PATRON_OGV:
                    offset = nbyte - 4
                    if es_offset_ogv_valido(offset) and verificar_ogv(offset):
                        print(f"{offset}:ogv")
                        ogv_offsets.append(offset)
                        contadores["ogv"] += 1
                        if total_encontrados() == sum(MAX_ARCHIVOS.values()):
                            Terminado = True
                        continue

else:
    print("El archivo no existe")
