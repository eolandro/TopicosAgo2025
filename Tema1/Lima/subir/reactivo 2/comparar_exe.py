import hashlib
import sys

def comparar_archivos_hex(archivo1, archivo2):
    """
    Compara dos archivos byte por byte y muestra las diferencias
    """
    try:
        with open(archivo1, 'rb') as f1, open(archivo2, 'rb') as f2:
            contenido1 = f1.read()
            contenido2 = f2.read()
            
            # Comparar tamaño
            if len(contenido1) != len(contenido2):
                print(f"Los archivos tienen tamaños diferentes:")
                print(f"   {archivo1}: {len(contenido1)} bytes")
                print(f"   {archivo2}: {len(contenido2)} bytes")
                return False
            
            # Comparar byte por byte
            diferencias = []
            for i, (byte1, byte2) in enumerate(zip(contenido1, contenido2)):
                if byte1 != byte2:
                    diferencias.append((i, byte1, byte2))
            
            if diferencias:
                print(f"Se encontraron {len(diferencias)} diferencias:")
                for i, (pos, byte1, byte2) in enumerate(diferencias[:10]):  # Mostrar solo las primeras 10
                    print(f"   Posición 0x{pos:08X}: {byte1:02X} ≠ {byte2:02X}")
                if len(diferencias) > 10:
                    print(f"   ... y {len(diferencias) - 10} diferencias más")
                return False
            else:
                print("Los archivos son idénticos")
                return True
                
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def calcular_hash(archivo):
    """Calcula los hashes MD5, SHA1 y SHA256 de un archivo"""
    try:
        with open(archivo, 'rb') as f:
            contenido = f.read()
            md5 = hashlib.md5(contenido).hexdigest()
            sha1 = hashlib.sha1(contenido).hexdigest()
            sha256 = hashlib.sha256(contenido).hexdigest()
            
            print(f"\nHashes de {archivo}:")
            print(f"  MD5:    {md5}")
            print(f"  SHA1:   {sha1}")
            print(f"  SHA256: {sha256}")
            
    except FileNotFoundError:
        print(f"Archivo no encontrado: {archivo}")

def main():
    if len(sys.argv) != 3:
        print("Uso: python comparador_hex.py archivo1.exe archivo2.exe")
        return
    
    archivo1 = sys.argv[1]
    archivo2 = sys.argv[2]
    
    print(f"\nComparando {archivo1} vs {archivo2}")
    print("=" * 50)
    
    # Calcular hashes
    calcular_hash(archivo1)
    calcular_hash(archivo2)
    
    print("\n" + "=" * 50)
    
    # Comparar archivos
    resultado = comparar_archivos_hex(archivo1, archivo2)
    
    if resultado:
        print("\nLos archivos son completamente idénticos")
    else:
        print("\nLos archivos son diferentes")

if __name__ == "__main__":
    main()