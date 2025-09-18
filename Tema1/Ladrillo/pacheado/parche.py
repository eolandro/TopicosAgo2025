import argparse
from pathlib import Path

# Lista de parches: cada parche es un grupo independiente
PATCHES = [
    [0x210, b'\x7F\x4D\x90\x90\x90\x90'],
    [0x21C, b'\x90\x90\x90\x90'],
    [0x220, b'\x90'],
    [0x229, b'\xEB\x34\x90\x90\x90'],
    [0x25F, b'\x39\xC0\x90\x90\x90\x90']
]

parser = argparse.ArgumentParser()
parser.add_argument("Archivo", help="Archivo a parchar", type=Path)
args = parser.parse_args()

if args.Archivo.exists():
    salida_path = Path("parcheando_patch.exe")
    print(f"Archivo encontrado: {args.Archivo}")

    with args.Archivo.open("rb") as entrada, salida_path.open("wb") as salida:
        data = bytearray(entrada.read())  # mutable

        # Aplicar todos los parches
        for offset, patch_bytes in PATCHES:
            if offset + len(patch_bytes) <= len(data):
                data[offset:offset+len(patch_bytes)] = patch_bytes

        salida.write(data)

    print(f"✅ Archivo parchado guardado como {salida_path}")
