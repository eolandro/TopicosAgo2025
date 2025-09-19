import argparse
from pathlib import Path

PARCHES = [
    # (posición, bytes nuevos)
    (0x20F, [b'\x00']),           # Cambiar 1 byte en posición 527
    (0x23D, [b'\xb8', b'\x00', b'\x00'])  # Cambiar 3 bytes en posición 573
]

parser = argparse.ArgumentParser()
parser.add_argument("Archivo", help="Archivo a parchar", type=Path)
args = parser.parse_args()
    
if args.Archivo.exists():
    print("Archivo encontrado")
    archivo_salida = Path(f"{args.Archivo.stem}_parchado_con_python{args.Archivo.suffix}")
        
    print("\nIniciando proceso de parcheo...")
    print("=" * 60)
    # Leer todo el archivo de una vez
    with open(args.Archivo, 'rb') as f:
        datos = bytearray(f.read())
        
    # Aplicar cada parche
    for posicion, bytes_nuevos in PARCHES:
        print(f"Parcheando posición 0x{posicion:X}: {len(bytes_nuevos)} bytes")
            
        # Reemplazar los bytes en la posición indicada
        for i, byte_nuevo in enumerate(bytes_nuevos):
            datos[posicion + i] = ord(byte_nuevo)  # Convertir byte a número
        
    # Guardar el archivo parchado
    with open(archivo_salida, 'wb') as f:
        f.write(datos)
        
    print("=" * 60)
    print(f"\n¡Listo! Archivo guardado como: {archivo_salida.name}")
    
