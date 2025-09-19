import sys
import os

def encontrar_todas_diferencias(archivo1, archivo2):
    """
    Encuentra todas las diferencias entre dos archivos binarios (ej: .exe)
    y muestra los desplazamientos en bytes
    """
    try:
        # Leer ambos archivos en modo binario
        with open(archivo1, 'rb') as f1:
            datos1 = f1.read()
        
        with open(archivo2, 'rb') as f2:
            datos2 = f2.read()
        
        print(f"\nBUSCANDO TODAS LAS DIFERENCIAS")
        print(f"Archivo 1: {archivo1} ({len(datos1)} bytes)")
        print(f"Archivo 2: {archivo2} ({len(datos2)} bytes)")
        print("=" * 60)
        
        # Comparar tamaños primero
        if len(datos1) != len(datos2):
            print(f"Los archivos tienen tamaños diferentes:")
            print(f"   {archivo1}: {len(datos1)} bytes")
            print(f"   {archivo2}: {len(datos2)} bytes")
            print()
        
        # Buscar todas las diferencias
        min_len = min(len(datos1), len(datos2))
        diferencias = []
        
        for i in range(min_len):
            if datos1[i] != datos2[i]:
                diferencias.append(i)
        
        # Buscar diferencias en bytes adicionales si los hay
        if len(datos1) > len(datos2):
            for i in range(min_len, len(datos1)):
                diferencias.append(i)
        elif len(datos2) > len(datos1):
            for i in range(min_len, len(datos2)):
                diferencias.append(i)
        
        if diferencias:
            print(f"SE ENCONTRARON {len(diferencias)} DIFERENCIAS:")
            print()
            
            # Mostrar todas las diferencias (máximo 50 para no saturar)
            max_diferencias_mostrar = min(50, len(diferencias))
            
            for i, pos in enumerate(diferencias[:max_diferencias_mostrar]):
                if pos < min_len:  # Diferencia dentro del rango común
                    print(f"   Diferencia {i+1}:")
                    print(f"     Desplazamiento: byte {pos} (0x{pos:X})")
                    print(f"     {archivo1}: {datos1[pos]:02X}")
                    print(f"     {archivo2}: {datos2[pos]:02X}")
                    
                    # Mostrar contexto alrededor de la diferencia
                    inicio = max(0, pos - 2)
                    fin = min(min_len, pos + 3)
                    
                    # Contexto para archivo 1
                    contexto1 = ' '.join(f'{datos1[j]:02X}' if j != pos else f'[{datos1[j]:02X}]' for j in range(inicio, fin))
                    # Contexto para archivo 2
                    contexto2 = ' '.join(f'{datos2[j]:02X}' if j != pos else f'[{datos2[j]:02X}]' for j in range(inicio, fin))
                    
                    print(f"     Contexto: {contexto1}")
                    print(f"               {contexto2}")
                    print(f"               {' '.join('   ^ ' if j == pos else '     ' for j in range(inicio, fin))}")
                    print()
                else:  # Diferencia por tamaño diferente
                    if len(datos1) > len(datos2):
                        print(f"   Diferencia {i+1}:")
                        print(f"     Desplazamiento: byte {pos} (0x{pos:X})")
                        print(f"     {archivo1}: {datos1[pos]:02X if pos < len(datos1) else 'N/A'}")
                        print(f"     {archivo2}: [BYTE FALTANTE]")
                        print()
                    else:
                        print(f"   Diferencia {i+1}:")
                        print(f"     Desplazamiento: byte {pos} (0x{pos:X})")
                        print(f"     {archivo1}: [BYTE FALTANTE]")
                        print(f"     {archivo2}: {datos2[pos]:02X if pos < len(datos2) else 'N/A'}")
                        print()
            
            if len(diferencias) > max_diferencias_mostrar:
                print(f"   ... y {len(diferencias) - max_diferencias_mostrar} diferencias más")
                print(f"   Use herramientas profesionales para análisis completos")
            
                                
        else:
            print("Los archivos son COMPLETAMENTE IDÉNTICOS")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def main():
    if len(sys.argv) != 3:
        print("Uso: python diferenciar_binarios.py archivo1.exe archivo2.exe")
        print("Ejemplo: python diferenciar_binarios.py programa1.exe programa2.exe")
        sys.exit(1)
    
    archivo1 = sys.argv[1]
    archivo2 = sys.argv[2]
    
    # Verificar que los archivos existen
    if not os.path.exists(archivo1):
        print(f"Error: No se encuentra el archivo '{archivo1}'")
        sys.exit(1)
    
    if not os.path.exists(archivo2):
        print(f"Error: No se encuentra el archivo '{archivo2}'")
        sys.exit(1)
    
    # Encontrar todas las diferencias
    encontrar_todas_diferencias(archivo1, archivo2)

if __name__ == "__main__":
    main()