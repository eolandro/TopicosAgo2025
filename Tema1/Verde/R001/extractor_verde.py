import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Extractor optimizado de archivos múltiples")
    parser.add_argument("archivo", help="Archivo binario a procesar", type=Path)
    
    args = parser.parse_args()
    
    if not args.archivo.exists():
        print(f"Error: El archivo {args.archivo} no existe")
        return
    
    # Patrones de cabeceras de archivos
    patrones = {
        "zip": b"\x50\x4B\x03\x04",
        "ogv": b"\x4F\x67\x67\x53",  # OggS
        "jpg1": b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01",
        "webm": b"\x1A\x45\xDF\xA3",
        "mp3": b"\x49\x44\x33",
        "jpg2": b"\xFF\xD8\xFF\xDB",
    }
    
    # Meta: extraer archivos específicos
    objetivos = {"jpg1": 1, "jpg2": 1, "zip": 1, "webm": 1, "ogv": 1, "ogv2":1, "mp3": 1}
    encontrados = {key: 0 for key in objetivos.keys()}
    
    print(f"Procesando archivo: {args.archivo}")
    archivo_size = args.archivo.stat().st_size
    print(f"Tamaño del archivo: {archivo_size} bytes")
    
    # Buscar patrones eficientemente
    posiciones = buscar_todos_los_patrones(args.archivo, patrones)
    
    print(f"Encontradas {len(posiciones)} ocurrencias de patrones")
    for pos, tipo in posiciones[:10]:  # Mostrar las primeras 10
        print(f"  {tipo} en posición {pos}")
    
    # Extraer archivos
    extraer_archivos_optimizado(args.archivo, posiciones, objetivos, encontrados)

def buscar_todos_los_patrones(archivo_path, patrones):
    """Busca todos los patrones en el archivo de manera eficiente"""
    posiciones = []
    chunk_size = 10 * 1024 * 1024  # 10MB chunks
    
    with archivo_path.open("rb") as archivo:
        # Calcular el tamaño máximo de patrón para el overlap
        max_pattern_size = max(len(patron) for patron in patrones.values())
        
        posicion_archivo = 0
        buffer_previo = b""
        
        while True:
            chunk = archivo.read(chunk_size)
            if not chunk:
                break
            
            # Combinar con buffer previo para no perder patrones en los límites
            data_completa = buffer_previo + chunk
            
            # Buscar cada patrón en este chunk
            for tipo, patron in patrones.items():
                pos = 0
                while True:
                    pos = data_completa.find(patron, pos)
                    if pos == -1:
                        break
                    
                    # Posición absoluta en el archivo
                    pos_absoluta = posicion_archivo - len(buffer_previo) + pos
                    posiciones.append((pos_absoluta, tipo))
                    pos += 1
            
            # Actualizar posición y buffer
            posicion_archivo += len(chunk)
            
            # Mantener un buffer para el siguiente chunk
            if len(data_completa) >= max_pattern_size:
                buffer_previo = data_completa[-max_pattern_size:]
            else:
                buffer_previo = data_completa
            
            # Mostrar progreso
            if posicion_archivo % (100 * 1024 * 1024) == 0:  # Cada 100MB
                print(f"Procesado: {posicion_archivo / 1024 / 1024:.1f} MB")
    
    # Ordenar por posición
    posiciones.sort()
    return posiciones

def extraer_archivos_optimizado(archivo_path, posiciones, objetivos, encontrados):
    """Extrae archivos basándose en las posiciones encontradas"""
    archivos_extraidos = 0
    posicion_actual = 0
    
    # Variables para manejar la unificación de archivos OGV
    ogv_unificado_nombre = "ogv_unificado.ogv"
    ogv_unificado = None
    ogv_encontrados = 0
    tamaño_total_ogv = 0
    
    # Variables para manejar la unificación de archivos MP3
    mp3_unificado_nombre = "mp3_unificado.mp3"
    mp3_unificado = None
    mp3_encontrados = 0
    tamaño_total_mp3 = 0
    
    with archivo_path.open("rb") as archivo:
        archivo_size = archivo.seek(0, 2)  # Ir al final para obtener tamaño
        
        for i, (pos, tipo) in enumerate(posiciones):
            # Saltar si esta posición ya fue procesada
            if pos < posicion_actual:
                continue
            
            # Determinar el final del archivo
            fin_archivo = archivo_size
            
            # Para archivos WEBM, no limitamos por el siguiente patrón
            # ya que pueden ser archivos grandes que se cortan prematuramente
            if tipo != "webm":
                for j in range(i + 1, len(posiciones)):
                    next_pos, next_tipo = posiciones[j]
                    if next_pos > pos:
                        fin_archivo = next_pos
                        break
            
            # Calcular el tamaño del archivo
            tamaño = fin_archivo - pos
            
            # Manejo especial para archivos OGV - unificar en un solo archivo
            if tipo == "ogv" or tipo == "ogv2":
                # Abrir archivo unificado solo cuando encontramos el primer OGV
                if ogv_unificado is None:
                    ogv_unificado = open(ogv_unificado_nombre, "wb")
                    print(f"Creando archivo unificado: {ogv_unificado_nombre}")
                
                # Leer y escribir el segmento al archivo unificado
                archivo.seek(pos)
                bytes_restantes = tamaño
                chunk_size = 1024 * 1024  # 1MB
                
                tamaño_mb = tamaño / (1024 * 1024)
                print(f"Unificando OGV #{ogv_encontrados + 1} (bytes {pos}-{fin_archivo-1}, tamaño: {tamaño_mb:.2f} MB)")
                
                while bytes_restantes > 0:
                    chunk_size_actual = min(chunk_size, bytes_restantes)
                    data = archivo.read(chunk_size_actual)
                    if not data:
                        break
                    ogv_unificado.write(data)
                    bytes_restantes -= len(data)
                
                ogv_encontrados += 1
                tamaño_total_ogv += tamaño
                posicion_actual = fin_archivo
                
            # Manejo especial para archivos MP3 - unificar en un solo archivo
            elif tipo == "mp3":
                # Abrir archivo unificado solo cuando encontramos el primer MP3
                if mp3_unificado is None:
                    mp3_unificado = open(mp3_unificado_nombre, "wb")
                    print(f"Creando archivo unificado: {mp3_unificado_nombre}")
                
                # Leer y escribir el segmento al archivo unificado
                archivo.seek(pos)
                bytes_restantes = tamaño
                chunk_size = 1024 * 1024  # 1MB
                
                tamaño_mb = tamaño / (1024 * 1024)
                print(f"Unificando MP3 #{mp3_encontrados + 1} (bytes {pos}-{fin_archivo-1}, tamaño: {tamaño_mb:.2f} MB)")
                
                while bytes_restantes > 0:
                    chunk_size_actual = min(chunk_size, bytes_restantes)
                    data = archivo.read(chunk_size_actual)
                    if not data:
                        break
                    mp3_unificado.write(data)
                    bytes_restantes -= len(data)
                
                mp3_encontrados += 1
                tamaño_total_mp3 += tamaño
                posicion_actual = fin_archivo
                
            else:
                # Para otros tipos de archivo, mantener la lógica original
                if encontrados[tipo] >= objetivos[tipo]:
                    continue
                
                # Extraer archivo normalmente
                contador = encontrados[tipo] + 1
                extension = get_extension(tipo)
                nombre_archivo = f"{tipo}_extraido_{contador:03d}.{extension}"
                
                # Para archivos WEBM, usar todo el espacio disponible hasta el final
                if tipo == "webm":
                    print(f"Extrayendo WEBM completo desde posición {pos} hasta el final del archivo")
                    tamaño = archivo_size - pos  # Usar todo el espacio restante
                    fin_archivo = archivo_size
                
                # Leer y escribir el segmento
                archivo.seek(pos)
                
                with open(nombre_archivo, "wb") as archivo_extraido:
                    # Copiar en chunks para archivos grandes
                    bytes_restantes = tamaño
                    chunk_size = 1024 * 1024  # 1MB
                    
                    while bytes_restantes > 0:
                        chunk_size_actual = min(chunk_size, bytes_restantes)
                        data = archivo.read(chunk_size_actual)
                        if not data:
                            break
                        archivo_extraido.write(data)
                        bytes_restantes -= len(data)
                
                print(f"Extraído: {nombre_archivo} (bytes {pos}-{fin_archivo-1}, tamaño: {tamaño/1024/1024:.2f} MB)" if tipo == "webm" else f"Extraído: {nombre_archivo} (bytes {pos}-{fin_archivo-1}, tamaño: {tamaño} bytes)")
                
                encontrados[tipo] += 1
                archivos_extraidos += 1
                posicion_actual = fin_archivo
            
            # Verificar si hemos extraído todo lo que necesitamos (excepto OGV y MP3 que se unifican)
            objetivos_no_unificados = {k: v for k, v in objetivos.items() if k not in ["ogv", "ogv2", "mp3"]}
            if all(encontrados[tipo] >= objetivos[tipo] for tipo in objetivos_no_unificados):
                break
    
    # Cerrar archivo OGV unificado si se creó
    if ogv_unificado:
        ogv_unificado.close()
        tamaño_total_mb = tamaño_total_ogv / (1024 * 1024)
        print(f"Archivo OGV unificado completado: {ogv_unificado_nombre}")
        print(f"  - Total de segmentos OGV unificados: {ogv_encontrados}")
        print(f"  - Tamaño total del archivo unificado: {tamaño_total_mb:.2f} MB")
        archivos_extraidos += 1
    
    # Cerrar archivo MP3 unificado si se creó
    if mp3_unificado:
        mp3_unificado.close()
        tamaño_total_mb = tamaño_total_mp3 / (1024 * 1024)
        print(f"Archivo MP3 unificado completado: {mp3_unificado_nombre}")
        print(f"  - Total de segmentos MP3 unificados: {mp3_encontrados}")
        print(f"  - Tamaño total del archivo unificado: {tamaño_total_mb:.2f} MB")
        archivos_extraidos += 1
    
    print(f"\nExtracción completada. Total de archivos extraídos: {archivos_extraidos}")
    print("Resumen:")
    for tipo, cantidad in encontrados.items():
        if tipo not in ["ogv", "ogv2", "mp3"]:
            print(f"  {tipo}: {cantidad}/{objetivos[tipo]}")
    if ogv_encontrados > 0:
        print(f"  ogv (unificado): {ogv_encontrados} segmentos en 1 archivo")
    if mp3_encontrados > 0:
        print(f"  mp3 (unificado): {mp3_encontrados} segmentos en 1 archivo")

def get_extension(tipo_archivo):
    """Retorna la extensión apropiada para cada tipo"""
    extensiones = {
        "zip": "zip", "ogv": "ogv", "jpg1": "jpg", 
        "jpg2": "jpg", "webm": "webm", "mp3": "mp3"
    }
    return extensiones.get(tipo_archivo, "bin")

if __name__ == "__main__":
    main()
