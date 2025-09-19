import argparse
from pathlib import Path

Parche = [
    [0x210, b'\xEB\x59\x90\x90\x90\x90']
]

parser = argparse.ArgumentParser()
parser.add_argument("Archivo", help="Archivo a parchar", type=Path)
args = parser.parse_args()

if args.Archivo.exists():
    salida_path = Path("parcheando_patch.exe")
    print(f"Archivo encontrado: {args.Archivo}")

    with args.Archivo.open("rb") as entrada, salida_path.open("wb") as salida:
        data = bytearray(entrada.read())

        for x, y in Parche:
            if x + len(y) <= len(data):
                data[x:x+len(y)] = y

        salida.write(data)

    print(f"Archivo parchado guardado como {salida_path}")
