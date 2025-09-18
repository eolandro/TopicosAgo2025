import os
import mmap
import struct
import time

# ==== CONFIGURACIÓN ====
# Ruta del archivo contenedor (donde buscarás los archivos)
RUTA_CONTENEDOR = r"C:/Users/olver/Documents/Noveno Semestre/Topicos de Ciberseguridad/Unidad 1/recursos de clase/resultado6"
# Carpeta donde se guardarán los archivos extraídos
CARPETA_SALIDA = r"C:/Users/olver/Documents/Noveno Semestre/Topicos de Ciberseguridad/Unidad 1/recursos de clase/archivos_finales"
# Tamaño mínimo para evitar extraer archivos muy pequeños y ruidosos (en bytes)
MIN_SIZE_BYTES = 5 * 1024 * 1024  # Reducido a MB para permitir archivos de audio más pequeños
# Límite máximo de archivos a extraer
MAX_EXTRACCIONES = 8

ARTISTA_BUSCADO = b"Alexander Ehlers"

# ==== Firmas y mapeo a extensión/descripción ====
MAGIC_NUMBERS = {
    b"\xFF\xD8\xFF": ("jpg", "JPEG"),
    b"\x89PNG\r\n\x1a\n": ("png", "PNG"),
    b"\x49\x44\x33": ("mp3", "Audio MP3 con cabecera ID3"),
    b"OggS": ("ogg", "OGG"),
    b"ftyp": ("mp4", "MP4"),
    b"\x1A\x45\xDF\xA3": ("mkv", "MKV"),
    b"RIFF": ("wav", "WAV"),
}

# ==== Parsers (final de archivos) ====
def parse_jpeg(mm, start, file_size):
    end_pos = mm.find(b"\xFF\xD9", start + 2)
    if end_pos != -1:
        return end_pos + 2, "JPEG (encontrado FF D9)"
    return None, "JPEG (no encontrado FF D9)"

def parse_png(mm, start, file_size):
    pos = start + 8
    try:
        while pos + 8 <= file_size:
            length = int.from_bytes(mm[pos:pos+4], 'big')
            ctype = mm[pos+4:pos+8]
            next_chunk = pos + 8 + length + 4
            if ctype == b'IEND':
                return next_chunk, "PNG (IEND encontrado)"
            pos = next_chunk
    except Exception as e:
        return None, f"PNG (error parseando chunks: {e})"
    return None, "PNG (no se encontró IEND)"

def parse_mp3(mm, start, file_size):
    if mm[start:start+3] == b'ID3' and start + 10 <= file_size:
        sz_bytes = mm[start+6:start+10]
        size = ((sz_bytes[0] & 0x7f) << 21) | ((sz_bytes[1] & 0x7f) << 14) | ((sz_bytes[2] & 0x7f) << 7) | (sz_bytes[3] & 0x7f)
        end = start + 10 + size
        if end <= file_size:
            return end, "MP3 (ID3v2 tag size)"
    return None, "MP3 (sin ID3, usando fallback)"

def parse_mp4(mm, pos, file_size):
    box_start = pos - 4
    if box_start < 0:
        return None, "MP4 (posición inválida para caja ftyp)"
    try:
        if box_start + 8 > file_size:
            return None, "MP4 (header incompleto)"
        size32 = int.from_bytes(mm[box_start:box_start+4], 'big')
        if size32 == 0:
            return None, "MP4 (size=0, hasta EOF, usar fallback)"
        if size32 == 1:
            if box_start+16 > file_size:
                return None, "MP4 (size64 header incompleto)"
            size64 = int.from_bytes(mm[box_start+8:box_start+16], 'big')
            end = box_start + size64
        else:
            end = box_start + size32
        if end <= file_size:
            return end, "MP4 (box size leído)"
        return None, "MP4 (box size apunta fuera)"
    except Exception as e:
        return None, f"MP4 (error parseando cajas: {e})"

def parse_mkv(mm, start, file_size):
    return None, "MKV (usando fallback, parsing no implementado)"

def parse_wav(mm, start, file_size):
    if start + 8 > file_size:
        return None, "WAV (header incompleto)"
    size_le = int.from_bytes(mm[start+4:start+8], 'little')
    end = start + 8 + size_le
    if end <= file_size:
        return end, "WAV (usado campo RIFF-size)"
    return None, "WAV (RIFF-size apunta fuera de archivo)"

def parse_ogg(mm, start, file_size):
    pos = start
    try:
        while pos + 27 <= file_size:
            if mm[pos:pos+4] != b'OggS':
                return None, "OGG (página no encontrada donde se esperaba)"
            header_type = mm[pos+5]
            seg_count = mm[pos+26]
            seg_table = mm[pos+27: pos+27+seg_count]
            if len(seg_table) != seg_count:
                return None, "OGG (tabla de segmentos incompleta)"
            payload_len = sum(seg_table)
            next_page = pos + 27 + seg_count + payload_len
            if header_type & 0x04:
                return next_page, "OGG (EOS encontrado)"
            pos = next_page
    except Exception as e:
        return None, f"OGG (error parseando páginas: {e})"
    return None, "OGG (no se encontró EOS antes de EOF)"

# Mapeo de extensiones a funciones
PARSERS = {
    "jpg": parse_jpeg,
    "png": parse_png,
    "wav": parse_wav,
    "ogg": parse_ogg,
    "mp3": parse_mp3,
    "mp4": parse_mp4,
    "mkv": parse_mkv,
}

# ==== Funciones principales ====
def encontrar_firmas(ruta):
    firmas = []
    file_size = os.path.getsize(ruta)
    with open(ruta, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        for magic, (ext, desc) in MAGIC_NUMBERS.items():
            start = 0
            while True:
                pos = mm.find(magic, start)
                if pos == -1:
                    break
                firmas.append((pos, ext, desc, magic))
                start = pos + 1
        mm.close()
    return sorted(firmas, key=lambda x: x[0])

def siguiente_firma_pos(actual_pos, firmas, file_size):
    for pos, *_ in firmas:
        if pos > actual_pos:
            return pos
    return file_size

def rangos_solapan(a_start, a_end, ranges):
    for s,e in ranges:
        if not (a_end <= s or a_start >= e):
            return True
    return False

def extraer_con_parsers(ruta_contenedor, carpeta_salida, min_size_bytes, max_archivos):
    size = os.path.getsize(ruta_contenedor)
    firmas = encontrar_firmas(ruta_contenedor)
    
    if not firmas:
        print("No se encontraron firmas.")
        return

    print(f"🔎 Encontradas {len(firmas)} firmas candidatas.")
    os.makedirs(carpeta_salida, exist_ok=True)

    extraidos = 0
    ranges_extraidos = []

    with open(ruta_contenedor, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        for idx, (pos, ext, desc, magic) in enumerate(firmas, start=1):
            if extraidos >= max_archivos:
                print("Límite de archivos alcanzado.")
                break

            if rangos_solapan(pos, pos + 1, ranges_extraidos):
                print(f"{idx}. [{ext}] pos {pos} -> SALTADO (ya dentro de un rango extraído).")
                continue

            if ext == "mp3":
                search_end = min(pos + 1024 * 1024, size)
                data_chunk = mm[pos:search_end]
                if ARTISTA_BUSCADO not in data_chunk:
                    print(f"{idx}. [{ext}] pos {pos} -> Descartado (artista no encontrado).")
                    continue
                else:
                    print(f"{idx}. [{ext}] pos {pos} -> Artista '{ARTISTA_BUSCADO.decode()}' encontrado, procesando...")

            end = None
            metodo = "sin determinar"
            parser = PARSERS.get(ext)
            
            if ext == "mp3":
                end = siguiente_firma_pos(pos, firmas, size)
                metodo = f"FALLBACK MP3 -> hasta la siguiente firma o EOF (pos {end})"
            elif parser:
                try:
                    end, metodo = parser(mm, pos, size)
                except Exception as e:
                    end, metodo = None, f"parser error: {e}"

            if not end or end <= pos:
                end = siguiente_firma_pos(pos, firmas, size)
                metodo = f"FALLBACK -> hasta la siguiente firma o EOF (pos {end})"

            tam_bytes = end - pos
            if tam_bytes < min_size_bytes:
                print(f"{idx}. [{ext}] pos {pos} -> descartado (tamaño {tam_bytes // (1024 * 1024)} MB < mínimo).")
                continue

            if rangos_solapan(pos, end, ranges_extraidos):
                print(f"{idx}. [{ext}] pos {pos} -> descartado por solapamiento.")
                continue

            f.seek(pos)
            datos = f.read(tam_bytes)
            nombre = f"carved_{extraidos+1}_{pos}.{ext}"
            ruta_out = os.path.join(carpeta_salida, nombre)
            
            with open(ruta_out, "wb") as out:
                out.write(datos)

            ranges_extraidos.append((pos, end))
            extraidos += 1
            print(f" Extraído: {nombre} | Tamaño={tam_bytes // (1024 * 1024)} MB | Método: {metodo}")

        mm.close()

    print(f"\nProceso terminado. Archivos extraídos: {extraidos}")

# ==== EJECUTAR EL PROCESO (con tiempo) ====
if __name__ == "__main__":
    inicio = time.time()
    extraer_con_parsers(RUTA_CONTENEDOR, CARPETA_SALIDA, MIN_SIZE_BYTES, MAX_EXTRACCIONES)
    fin = time.time()
    duracion = fin - inicio
    mins, secs = divmod(duracion, 60)
    print(f"\n⏱ Tiempo total de ejecución: {int(mins)} min {secs:.2f} seg")
