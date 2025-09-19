import os
import zipfile

FIRMAS_MAGICAS = {
    b'\xFF\xD8\xFF\xE0\x00\x10\x4A\x46': "jpg",  
    b'\xFF\xD8\xFF\xDB\x00\x43\x00\x04': "jpg",  
    b'\xFF\xD8\xFF\xEE\x00\x10\x4A\x46': "jpg",  
    b'\xFF\xD8\xFF\xE1\x00\x10\x4A\x46': "jpg",  
    b'\x50\x4B\x03\x04\x14\x03\x00\x00': "zip",  
    b'\x1A\x45\xDF\xA3\x01\x00\x00\x00': "webm",  
    b'\x00\x00\x00\x18\x66\x74\x79\x70': "mp4",  
    b'\x49\x44\x33\x02\x00\x00\x00\x00': "mp3",  
    b'\x49\x44\x33\x03\x00\x00\x00\x00': "mp3",  
    b'\x49\x44\x33\x04\x00\x00\x00\x00': "mp3",  
    b'\xFF\xFB\x90\x64\x00\x00\x00\x00': "mp3",  
    b'\xFF\xFA\x92\xC4\x00\x00\x00\x00': "mp3", 
    b'\xFF\xF3\x40\xC4\x00\x00\x00\x00': "mp3",  
    b'\xFF\xF2\x48\x80\x00\x00\x00\x00': "mp3",
     b'\x4F\x67\x67\x53\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\xF1\xFC': "ogv",
}

def crear_directorio_salida(ruta_directorio):
    if not os.path.exists(ruta_directorio):
        os.makedirs(ruta_directorio)

def extraer_archivo_zip(ruta_archivo_zip, ruta_directorio_salida):
    """Extrae el contenido de un archivo ZIP en el directorio especificado."""
    try:
        with zipfile.ZipFile(ruta_archivo_zip, 'r') as archivo_zip:
            archivo_zip.extractall(ruta_directorio_salida)
        print(f"Contenido del ZIP extraído: {ruta_archivo_zip}")
    except zipfile.BadZipFile:
        print(f"No se pudo extraer el archivo ZIP (posiblemente corrupto): {ruta_archivo_zip}")

def encontrar_siguiente_firma(contenido, posicion_actual, firmas_magicas):
    """Encuentra la posición de la siguiente firma mágica en el contenido."""
    siguiente_posicion = len(contenido)
    for firma in firmas_magicas.keys():
        posicion = contenido.find(firma, posicion_actual + 1)
        if posicion != -1 and posicion < siguiente_posicion:
            siguiente_posicion = posicion
    return siguiente_posicion

def extraer_archivos_desde_contenido(contenido, firmas_magicas, ruta_directorio_salida):
    posicion = 0
    while posicion < len(contenido):
        encontrado = False

        for firma, tipo_archivo in firmas_magicas.items():
            if contenido.startswith(firma, posicion):
                siguiente_posicion = encontrar_siguiente_firma(contenido, posicion, firmas_magicas)
                contenido_archivo = contenido[posicion:siguiente_posicion]
                nombre_archivo = f"{ruta_directorio_salida}/archivo_{posicion}.{tipo_archivo}"
                
                # Guardar el archivo extraído
                with open(nombre_archivo, "wb") as archivo_salida:
                    archivo_salida.write(contenido_archivo)
                
                print(f"Archivo extraído: {nombre_archivo}")
                
                # Si es un ZIP, extraer su contenido también
                if tipo_archivo == "zip":
                    extraer_archivo_zip(nombre_archivo, ruta_directorio_salida)
                
                posicion = siguiente_posicion
                encontrado = True
                break
        
        if not encontrado:
            posicion += 1

def main(archivo_entrada, directorio_salida):
    crear_directorio_salida(directorio_salida)
    
    # Leer el contenido del archivo de entrada
    with open(archivo_entrada, mode='rb') as archivo:
        contenido = archivo.read()
    
    # Extraer archivos basados en las firmas mágicas
    extraer_archivos_desde_contenido(contenido, FIRMAS_MAGICAS, directorio_salida)

if __name__ == "__main__":
    ARCHIVO_ENTRADA =  r"C:\Users\l1859\OneDrive\Escritorio\15 S\Topicos\Extraer Archivos\resultado5"
    CARPETA_SALIDA = r"C:\Users\l1859\OneDrive\Escritorio\15 S\Topicos\Extraer Archivos\archivos"
    main(ARCHIVO_ENTRADA, CARPETA_SALIDA)
