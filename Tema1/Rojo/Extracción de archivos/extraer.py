import os
import zipfile

MAGIC_NUMBERS = {
    b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46': "jpg",
    b'\xFF\xD8\xFF\xDB\x00\x43\x00\x04': "jpg",
    b'\xFF\xD8\xFF\xEE\x00\x10\x4A\x46': "jpg",
    b'\xFF\xD8\xFF\xE1\x00\x10\x4A\x46': "jpg",
    b'\x50\x4B\x03\x04\x14\x03\x00\x00': "zip",
    b'\x1A\x45\xDF\xA3\x01\x00\x00\x00': "webm",
    b'\x4F\x67\x67\x53': "ogv",                   
    b'\x00\x00\x00\x18\x66\x74\x79\x70': "mp4",
    b'\x49\x44\x33\x02\x00\x00\x00\x00': "mp3",
    b'\x49\x44\x33\x03\x00\x00\x00\x00': "mp3",
    b'\x49\x44\x33\x04\x00\x00\x00\x00': "mp3",
    b'\xFF\xFB\x90\x64\x00\x00\x00\x00': "mp3",
    b'\xFF\xFA\x92\xC4\x00\x00\x00\x00': "mp3",
    b'\xFF\xF3\x40\xC4\x00\x00\x00\x00': "mp3",
    b'\xFF\xF2\x48\x80\x00\x00\x00\x00': "mp3",
    b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': "png",
}

def asegurar_directorio_salida(directorio_salida):
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)

def extraer_zip(ruta_zip, directorio_salida):
    try:
        with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
            zip_ref.extractall(directorio_salida)
    except zipfile.BadZipFile:
        print(f"ERROR: ZIP corrupto: {ruta_zip}")

def encontrar_siguiente_posicion_magica(contenido, posicion_actual, magic_numbers):
    siguiente = len(contenido)
    for firma in magic_numbers.keys():
        pos = contenido.find(firma, posicion_actual + 1)
        if pos != -1 and pos < siguiente:
            siguiente = pos
    return siguiente

def parsear_final_stream_ogg(contenido, inicio):
    pos = inicio
    largo = len(contenido)
    while pos + 27 <= largo:
        if contenido[pos:pos+4] != b'OggS':
            return pos
        try:
            header_type = contenido[pos + 5]
            page_segments = contenido[pos + 26]
        except IndexError:
            return largo

        tabla_segmentos_inicio = pos + 27
        tabla_segmentos_fin = tabla_segmentos_inicio + page_segments
        if tabla_segmentos_fin > largo:
            return largo

        segmentos = contenido[tabla_segmentos_inicio:tabla_segmentos_fin]
        tam_payload = sum(segmentos)
        fin_pagina = tabla_segmentos_fin + tam_payload
        if fin_pagina > largo:
            return largo

        if header_type & 0x04:  
            return fin_pagina

        pos = fin_pagina
    return largo

def extraer_archivos(contenido, magic_numbers, directorio_salida):
    posicion = 0
    contador_ogv = 0
    contador_archivos = 0
    max_archivos = 8 

    firmas_ordenadas = sorted(magic_numbers.items(), key=lambda kv: len(kv[0]), reverse=True)

    while posicion < len(contenido) and contador_archivos < max_archivos:
        encontrado = False
        for firma, tipo_archivo in firmas_ordenadas:
            if contenido.startswith(firma, posicion):
                if tipo_archivo == "ogv":
                    fin = parsear_final_stream_ogg(contenido, posicion)
                    if fin <= posicion:
                        fin = encontrar_siguiente_posicion_magica(contenido, posicion, magic_numbers)

                   
                    if contador_ogv < 2:
                        contador_ogv += 1
                        contador_archivos += 1
                        nombre_archivo = os.path.join(directorio_salida, f"{contador_archivos}.ogv")
                        with open(nombre_archivo, "wb") as out:
                            out.write(contenido[posicion:fin])
                        print(nombre_archivo)
                    
                    posicion = fin
                    encontrado = True
                    break

                
                siguiente = encontrar_siguiente_posicion_magica(contenido, posicion, magic_numbers)
                if siguiente <= posicion:
                    siguiente = len(contenido)
                contador_archivos += 1
                nombre_archivo = os.path.join(directorio_salida, f"{contador_archivos}.{tipo_archivo}")
                with open(nombre_archivo, "wb") as out:
                    out.write(contenido[posicion:siguiente])
                if tipo_archivo == "zip":
                    extraer_zip(nombre_archivo, directorio_salida)
                print(nombre_archivo)
                posicion = siguiente
                encontrado = True
                break

        if not encontrado:
            posicion += 1

def main(archivo_entrada, directorio_salida):
    asegurar_directorio_salida(directorio_salida)
    with open(archivo_entrada, "rb") as f:
        contenido = f.read()
    extraer_archivos(contenido, MAGIC_NUMBERS, directorio_salida)
    print("EXTRACCION COMPLETA.")

if __name__ == "__main__":
    INPUT_FILE = "resultado3"
    OUTPUT_DIR = "archivos"
    main(INPUT_FILE, OUTPUT_DIR)
