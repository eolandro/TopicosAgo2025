import argparse
from pathlib import Path
import time  # para medir tiempo

# Registrar tiempo de inicio
start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("Archivo", help="Archivo a parchar", type=Path)

Data_patch = [b'\x39', b'\xC0', b'\x90', b'\x90', b'\x90', b'\x90']

args = parser.parse_args()

if args.Archivo.exists():
    archivo_parchado = Path(str(args.Archivo.resolve()) + '_patch.exe')
    print("Archivo encontrado")
    with args.Archivo.open("rb") as entrada:
        with archivo_parchado.open("wb") as salida:
            NByt = 0
            D = entrada.read(1)
            while D:
                NByt += 1
                salida.write(D)

                if NByt == 0x25F:
                    for a in Data_patch:
                        salida.write(a)
                    entrada.read(6)

                D = entrada.read(1)

# Registrar tiempo de fin
end_time = time.time()
elapsed_time = end_time - start_time

# Mostrar tiempo en consola
print(f"Tiempo de ejecución: {elapsed_time:.6f} segundos")
