# ==========================
# Funciones de extracción
# ==========================

def extraer_jpg():
    with open("resultado9", "rb") as f:
        data = f.read()

    contador = 1
    pos = 0
    while contador <= 2:
        # Buscar inicio de JPG
        inicio = data.find(b"\xFF\xD8\xFF", pos)
        if inicio == -1:
            print(f"No se encontró JPG #{contador}")
            break

        # Buscar final de JPG (FFD9) después de este inicio
        fin = inicio + 2
        while True:
            fin = data.find(b"\xFF\xD9", fin)
            if fin == -1:
                print(f"JPG #{contador} corrupto")
                break
            fin += 2  # incluir FFD9

            # Verificar que no haya otra cabecera JPG dentro de este rango
            siguiente_inicio = data.find(b"\xFF\xD8\xFF", inicio + 2)
            if siguiente_inicio == -1 or siguiente_inicio >= fin:
                break  # fin correcto
            else:
                # Hay otra cabecera dentro, buscar siguiente FFD9
                continue

        nombre = f"{contador}.jpg"
        with open(nombre, "wb") as out:
            out.write(data[inicio:fin])

        print(f"JPG #{contador} extraído como {nombre}")
        contador += 1
        pos = fin


def extraer_mp3():
    with open("resultado9", "rb") as f:
        data = f.read()

    posibles = [b"\x49\x44\x33", b"\xFF\xFB"]
    inicio = None
    for sig in posibles:
        pos = data.find(sig)
        if pos != -1:
            inicio = pos
            break

    if inicio is None:
        print("No se encontró MP3 en resultado9.")
        return

    MAGIC_NUMBERS = [b"\xFF\xD8\xFF", b"\x1A\x45\xDF\xA3", b"OggS", b"\x50\x4B\x03\x04"]
    fin = len(data)
    for sig in MAGIC_NUMBERS:
        pos = data.find(sig, inicio+3)
        if pos != -1 and pos < fin:
            fin = pos

    with open("6.mp3", "wb") as out:
        out.write(data[inicio:fin])

    print("MP3 extraído como 6.mp3")


def extraer_webm():
    with open("resultado9", "rb") as f:
        data = f.read()

    inicio = data.find(b"\x1A\x45\xDF\xA3")  # magic WebM
    if inicio == -1:
        print("No se encontró WebM en resultado9")
        return

    # Extraer desde inicio hasta el final del archivo
    with open("3.webm", "wb") as out:
        out.write(data[inicio:])

    print("WebM extraído como 3.webm")


def extraer_ogv():
    with open("resultado9", "rb") as f:
        data = f.read()

    inicio = 0
    contador = 1
    while contador <= 2:  # extraer 2 OGV
        inicio = data.find(b"OggS", inicio)
        if inicio == -1:
            print(f"No se encontró OGV #{contador}")
            break

        fin = inicio
        while fin < len(data):
            if data[fin:fin+4] != b"OggS":
                fin += 1
                continue

            if fin + 27 > len(data):
                break

            num_segments = data[fin + 26]
            page_header_size = 27 + num_segments
            segment_table = data[fin+27 : fin+27+num_segments]
            total_data = sum(segment_table)
            fin += page_header_size + total_data

            flag_eos = data[fin - total_data - page_header_size + 5] & 0x04
            if flag_eos:
                break

        nombre = f"{3 + contador}.ogv"  # 4.ogv y 5.ogv
        with open(nombre, "wb") as out:
            out.write(data[inicio:fin])

        print(f"OGV #{contador} extraído como {nombre}")
        inicio = fin
        contador += 1


def extraer_zip():
    with open("resultado9", "rb") as f:
        data = f.read()

    inicio = data.find(b"\x50\x4B\x03\x04")  # magic ZIP
    if inicio == -1:
        print("No se encontró ZIP en resultado9")
        return

    eocd = data.rfind(b"\x50\x4B\x05\x06")
    if eocd != -1:
        fin = eocd + 22
    else:
        fin = len(data)

    with open("7.zip", "wb") as out:
        out.write(data[inicio:fin])

    print("ZIP extraído como 7.zip")


# ==========================
# EJECUCIÓN
# ==========================
extraer_jpg()
extraer_mp3()
extraer_webm()
extraer_ogv()
extraer_zip()
