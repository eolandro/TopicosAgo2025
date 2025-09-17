import argparse
from pathlib import Path

# archivo generado por el prof
parser = argparse.ArgumentParser()
parser.add_argument("ArchivoProfe", help="Primer archivo", type=Path)

# Archivo = "resultado8"

Patrones = {
    "ogv": [b"\x4f\x67\x67\x53\x00\x02\x00\x00\x00"],
    "webm": [b"\x1a\x45\xdf\xa3"],
    "jpg": [b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01"],
    "mp3": [
        b"\x49\x44\x33\x02\x00\x00\x00\x00",
        b"\xff\xfb\x90\x64\x00\x00\x00\x00",
        b"\xff\xfa\x92\xc4\x00\x00\x00\x00",
        b"\xff\xf3\x40\xc4\x00\x00\x00\x00",
        b"\xff\xf2\x48\x80\x00\x00\x00\x00",
    ],
    "zip": [b"\x50\x4b\x03\x04\x14\x03\x00\x00"],
}

# pa mas facil buscar desde el mas pesao
orden_patrones = ["webm", "ogv", "mp3", "zip", "jpg"]

def buscarPatrones(Patrones_Recibidos):
    args = parser.parse_args()
    if args.ArchivoProfe.exists():
        print("Archivo existe")

        # Verificacion de a calis
        # with open(Archivo, "rb") as archProf:
        with args.ArchivoProfe.open("rb") as archProf:
            fr = archProf.read()

            for clave in orden_patrones:
                for patron in Patrones_Recibidos[clave]:
                    pos = fr.find(patron)  # Buscamos el primer patron pa
                    while pos != -1:
                        print(f"Se encontró {clave} con patrón {patron} en {pos}")

                        # Buscar siguiente inicio de otro patrón
                        siguiente = len(fr)
                        for p_ext, p_list in Patrones_Recibidos.items():
                            if p_ext == clave:  # ignorar mismo tipo
                                continue
                                # p de patron p_list pos donde estan los patrones
                            for p in p_list:
                                n = fr.find(
                                    p, pos + len(patron)
                                )  # Busca el siguiente patron "pos + len(patron) = a posicion actual pa"
                                if (
                                    n != -1 and n < siguiente
                                ):  # Comparacion  de si encuentra o nada  no >D
                                    siguiente = n

                        extraer(clave, fr, pos, siguiente)

                        # Buscar siguientes ocurrencias de este patrón sin empexar desde el inicio del archivo >:D
                        pos = fr.find(patron, siguiente)


def extraer(extension, fr, pos_ini, pos_fin):
    contador = 0
    salida = Path(f"extraido_{contador}.{extension}")
    while salida.exists():
        contador += 1
        salida = Path(f"extraido_{contador}.{extension}")

    with salida.open("wb") as f:
        f.write(fr[pos_ini:pos_fin])

    print(f"Archivo extraído: {salida} (desde {pos_ini} hasta {pos_fin})\n")


def main():
    buscarPatrones(Patrones)


main()
