import os
import zipfile

NumerosMagicos = {
    b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46': "jpg",
    b'\xFF\xD8\xFF\xDB\x00\x43\x00\x04': "jpg",
    b'\xFF\xD8\xFF\xEE\x00\x10\x4A\x46': "jpg",
    b'\xFF\xD8\xFF\xE1\x00\x10\x4A\x46': "jpg",
    b'\x50\x4B\x03\x04\x14\x03\x00\x00': "zip",
    b'\x1A\x45\xDF\xA3\x01\x00\x00\x00': "webm",
    b'\x4F\x67\x67\x53\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\xF1\xFC': "ogv",
    b'\x00\x00\x00\x18\x66\x74\x79\x70': "mp4",
    b'\x49\x44\x33\x02\x00\x00\x00\x00': "mp3",
    b'\x49\x44\x33\x03\x00\x00\x00\x00': "mp3",
    b'\x49\x44\x33\x04\x00\x00\x00\x00': "mp3",
    b'\xFF\xFB\x90\x64\x00\x00\x00\x00': "mp3",
    b'\xFF\xFA\x92\xC4\x00\x00\x00\x00': "mp3",
    b'\xFF\xF3\x40\xC4\x00\x00\x00\x00': "mp3",
    b'\xFF\xF2\x48\x80\x00\x00\x00\x00': "mp3",
}

def crear_directorio_salida(carpeta_destino):
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

def descomprimir_zip(ruta_archivo, carpeta_destino):
    try:
        with zipfile.ZipFile(ruta_archivo, 'r') as zip_archivo:
            zip_archivo.extractall(carpeta_destino)
        print(f"ZIP descomprimido: {ruta_archivo}")
    except zipfile.BadZipFile:
        print(f"Error al descomprimir ZIP (archivo dañado): {ruta_archivo}")

def buscar_siguiente_firma(datos, posicion_actual, firmas):
    proxima_posicion = len(datos)
    for firma in firmas.keys():
        pos = datos.find(firma, posicion_actual + 1)
        if pos != -1 and pos < proxima_posicion:
            proxima_posicion = pos
    return proxima_posicion

def procesar_archivos(datos, firmas, carpeta_salida):
    posicion = 0
    contador_jpg = 1
    contador_mp3 = 1
    contador_ogv = 1
    
    while posicion < len(datos):
        encontrado = False
        for firma, tipo_archivo in firmas.items():
            if datos.startswith(firma, posicion):
                siguiente_pos = buscar_siguiente_firma(datos, posicion, firmas)
                contenido_archivo = datos[posicion:siguiente_pos]
                
                if tipo_archivo == "jpg":
                    nombre_archivo = f"{carpeta_salida}/jpg{contador_jpg}.jpg"
                    contador_jpg += 1
                elif tipo_archivo == "mp3":
                    nombre_archivo = f"{carpeta_salida}/mp3{contador_mp3}.mp3"
                    contador_mp3 += 1
                elif tipo_archivo == "ogv":
                    if contador_ogv == 1:
                        nombre_archivo = f"{carpeta_salida}/2.ogv"
                    else:
                        nombre_archivo = f"{carpeta_salida}/ogv.ogv"
                    contador_ogv += 1
                elif tipo_archivo == "webm":
                    nombre_archivo = f"{carpeta_salida}/webm.webm"
                elif tipo_archivo == "zip":
                    nombre_archivo = f"{carpeta_salida}/zip.zip"
                else:
                    nombre_archivo = f"{carpeta_salida}/archivo_{posicion}.{tipo_archivo}"
                
                with open(nombre_archivo, "wb") as archivo_salida:
                    archivo_salida.write(contenido_archivo)
                print(f"Extraído: {nombre_archivo}")
                
                if tipo_archivo == "zip":
                    descomprimir_zip(nombre_archivo, carpeta_salida)
                
                posicion = siguiente_pos
                encontrado = True
                break
        
        if not encontrado:
            posicion += 1

def ejecutar_extraccion(archivo_entrada, directorio_salida):
    """Función principal para procesar el archivo de entrada."""
    crear_directorio_salida(directorio_salida)
    
    with open(archivo_entrada, mode='rb') as archivo:
        contenido = archivo.read()
    
    procesar_archivos(contenido, NumerosMagicos, directorio_salida)

if __name__ == "__main__":
    ArchivoBinario = "resultado0"
    CarpetaExtraidos = "archivos_extraidos"
    ejecutar_extraccion(ArchivoBinario, CarpetaExtraidos)