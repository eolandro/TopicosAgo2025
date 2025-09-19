
import struct
import sys
from collections import defaultdict

# Firma mágica que identifica archivos OGG
MAGIA_OGG = b"OggS"

# ---------------------------------------------------------
# Función para leer el tamaño EBML (se usa en videos WEBM)
# ---------------------------------------------------------
def leer_tamanio_ebml(datos, pos):
    if pos >= len(datos):
        return None, None
    primer_byte = datos[pos]
    mascara = 0x80
    tamanio = 1
    while (primer_byte & mascara) == 0:
        tamanio += 1
        mascara >>= 1
        if mascara == 0:
            break
    if tamanio > 8 or pos + tamanio > len(datos):
        return None, None
    bytes_tamanio = datos[pos:pos+tamanio]
    valor = bytes_tamanio[0] & (0xFF >> (tamanio + 1))
    for i in range(1, len(bytes_tamanio)):
        valor = (valor << 8) | bytes_tamanio[i]
    return tamanio, valor

# ---------------------------------------------------------
# Encontrar fin de un archivo WEBM
# ---------------------------------------------------------
def encontrar_fin_webm(datos, inicio):
    pos = inicio
    try:
        pos += 4
        long_bytes, valor = leer_tamanio_ebml(datos, pos)
        if long_bytes is None:
            return None
        pos += long_bytes + valor
        id_segmento = b"\x18\x53\x80\x67"
        inicio_segmento = datos.find(id_segmento, pos)
        if inicio_segmento == -1:
            return None
        long_seg, val_seg = leer_tamanio_ebml(datos, inicio_segmento + 4)
        if long_seg is None:
            return None
        fin = inicio_segmento + 4 + long_seg + val_seg
        return fin if fin <= len(datos) else len(datos)
    except:
        return None

# ---------------------------------------------------------
# Encontrar fin de un JPG
# ---------------------------------------------------------
def encontrar_fin_jpg(datos, inicio):
    fin = datos.find(b"\xFF\xD9", inicio)  # marca de fin JPG
    return fin + 2 if fin != -1 else len(datos)

# ---------------------------------------------------------
# Funciones auxiliares para OGG/OGV
# ---------------------------------------------------------
def leer_pagina_ogg(datos, pos, total):
    if pos + 27 > total or datos[pos:pos+4] != MAGIA_OGG:
        return None
    version = datos[pos+4]
    if version != 0:
        return None
    tipo_encabezado = datos[pos+5]
    num_segmentos = datos[pos+26]
    tam_encabezado = 27 + num_segmentos
    if pos + tam_encabezado > total:
        return None
    tabla = datos[pos+27:pos+27+num_segmentos]
    tam_cuerpo = sum(tabla)
    tam_total = tam_encabezado + tam_cuerpo
    if pos + tam_total > total:
        return None
    return tam_total, tipo_encabezado

def encontrar_fin_ogv(datos, inicio):
    pos = inicio
    total = len(datos)
    valido = False
    while pos < total:
        leido = leer_pagina_ogg(datos, pos, total)
        if not leido:
            break
        tam_pag, tipo = leido
        fin_pag = pos + tam_pag
        if tipo & 0x04:  # fin de stream
            valido = True
            return fin_pag
        pos = fin_pag
        if pos >= total or datos[pos:pos+4] != MAGIA_OGG:
            break
    return None if not valido else pos

# ---------------------------------------------------------
# Buscar fin de MP3 (lee frames uno por uno)
# ---------------------------------------------------------
def leer_header_mp3(cabecera):
    if len(cabecera) < 4:
        return None
    b1, b2, b3, b4 = cabecera
    if b1 != 0xFF or (b2 & 0xE0) != 0xE0:
        return None
    version = (b2 >> 3) & 0x03
    capa = (b2 >> 1) & 0x03
    bitrate_idx = (b3 >> 4) & 0x0F
    sample_idx = (b3 >> 2) & 0x03
    padding = (b3 >> 1) & 0x01
    bitrates = [None,32,40,48,56,64,80,96,112,128,160,192,224,256,320,None]
    sample_rates = [44100, 48000, 32000, None]
    if version != 3 or capa != 1:
        return None
    if bitrate_idx >= len(bitrates) or sample_idx >= len(sample_rates):
        return None
    bitrate = bitrates[bitrate_idx] * 1000
    samplerate = sample_rates[sample_idx]
    if not bitrate or not samplerate:
        return None
    return int((144 * bitrate) // samplerate + padding)

def encontrar_fin_mp3(datos, inicio):
    pos = inicio
    total = len(datos)
    if datos[pos:pos+3] == b"ID3" and pos + 10 <= total:
        bytes_tam = datos[pos+6:pos+10]
        tam_tag = ((bytes_tam[0] & 0x7F) << 21) | ((bytes_tam[1] & 0x7F) << 14) | ((bytes_tam[2] & 0x7F) << 7) | (bytes_tam[3] & 0x7F)
        pos += 10 + tam_tag
    while pos + 4 <= total:
        frame = leer_header_mp3(datos[pos:pos+4])
        if frame is None:
            break
        pos += frame
    return pos

# ---------------------------------------------------------
# Encontrar fin de ZIP
# ---------------------------------------------------------
def encontrar_fin_zip(datos, inicio):
    firma = b"\x50\x4B\x05\x06"
    pos = datos.find(firma, inicio)
    if pos == -1 or pos + 22 > len(datos):
        return len(datos)
    tam_coment = int.from_bytes(datos[pos+20:pos+22], "little")
    return pos + 22 + tam_coment

# ---------------------------------------------------------
# Función principal que analiza el archivo y extrae todo
# ---------------------------------------------------------
def extraer_todo(ruta):
    with open(ruta, "rb") as f:
        datos = f.read()
    longitud = len(datos)
    print(f"🔎 Analizando: {ruta}  (tamaño: {longitud} bytes)")
    print("-" * 60)

    # Firmas de archivos conocidos
    formatos = {
        b"\xFF\xD8\xFF": {"ext": "jpg", "nombre": "JPEG", "fin": encontrar_fin_jpg},
        b"\x1A\x45\xDF\xA3": {"ext": "webm", "nombre": "WEBM", "fin": encontrar_fin_webm},
        MAGIA_OGG: {"ext": "ogg", "nombre": "OGG", "fin": encontrar_fin_ogv},
        b"ID3": {"ext": "mp3", "nombre": "MP3", "fin": encontrar_fin_mp3},
        b"\xFF\xFB": {"ext": "mp3", "nombre": "MP3", "fin": encontrar_fin_mp3},
        b"\x50\x4B\x03\x04": {"ext": "zip", "nombre": "ZIP", "fin": encontrar_fin_zip},
    }

    i = 0
    total = 0
    contador = 1

    while i < longitud:
        encontrado = False
        for firma, info in formatos.items():
            lf = len(firma)
            if i + lf <= longitud and datos[i:i+lf] == firma:
                inicio = i
                fin = info['fin'](datos, inicio)
                if fin is None or fin <= inicio:
                    break  # archivo inválido
                extraido = datos[inicio:fin]
                tam = len(extraido)
                ext = info['ext']

                # Filtro: si es OGG demasiado chico, lo saltamos
                if info['nombre'] == "OGG" and tam < 1024:
                    print(f"⚠️ OGG muy pequeño ignorado en 0x{inicio:X}-{fin:X} ({tam} bytes)\n")
                    i = fin
                    encontrado = True
                    break

                nombre_archivo = f"{contador}.{ext}"
                with open(nombre_archivo, "wb") as out:
                    out.write(extraido)

                print(f"✅ Extraído: {nombre_archivo}")
                print(f"   Tipo: {info['nombre']}")
                print(f"   Inicio: 0x{inicio:X}")
                print(f"   Fin:    0x{fin:X}")
                print(f"   Tamaño: {tam} bytes\n")

                total += 1
                contador += 1
                i = fin
                encontrado = True
                break
        if not encontrado:
            i += 1

    print("-" * 60)
    print(f"🎉 Extracción completada: {total} archivo(s).")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    extraer_todo(sys.argv[1])
