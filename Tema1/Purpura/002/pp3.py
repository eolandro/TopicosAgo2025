import argparse
import sys
from pathlib import Path

# (offset, nuevo_byte)
parche = [
    (0x324, b'\x43'),  
    (0x325, b'\xFF'),  
]

# recibir archivo de entrada y salida
parser = argparse.ArgumentParser() # parcha y mide el tiempo
parser.add_argument("Archivo", type=Path)
parser.add_argument("-o", "--output", dest="salida", type=Path, default=None) # Ruta de salida: archivo_patched
args = parser.parse_args()

# Verificar que el archivo de entrada exista
if not args.Archivo.is_file():
    sys.exit(f"ERROR: no existe el archivo {args.Archivo}")

print(f"Archivo encontrado: {args.Archivo.name}")

# Cargar todo el ejecutable en memoria como bytearray
buf = bytearray(args.Archivo.read_bytes())

# Ruta de salida: usa --output o añade sufijo "_patched"
destino = args.salida or args.Archivo.with_name(
    f"{args.Archivo.stem}_patched{args.Archivo.suffix}"
)

print(f"Aplicando {len(parche)} parche(s)…")

# Recorrer y aplicar cada parche
for offset, new_byte in parche:
    old = buf[offset]
    buf[offset:offset+1] = new_byte
    print(f"  Offset {hex(offset)}: {old:02X} → {new_byte.hex().upper()}")

# Archivo parchado
destino.write_bytes(buf)
print(f"Parche completado: {destino.name}")


