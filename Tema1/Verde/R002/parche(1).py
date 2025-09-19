import argparse
from pathlib import Path
import time

parser = argparse.ArgumentParser()
parser.add_argument("Archivo",help="Archivo a parchar",type=Path)

inicio = time.time()

data_patch1 = [b'\x39']
data_patch2 = [b'\xc0',b'\x90',b'\x90',b'\x90',b'\x90',b'\x0f']

args = parser.parse_args()
if args.Archivo.exists():
    archivo_parchado = Path(str(args.Archivo.resolve()) + '_patch.exe')
    print("Archivo encontrado")
    with args.Archivo.open("rb") as entrada:
        with archivo_parchado.open("wb") as salida:
            n_byte = 0
            D = entrada.read(1)
            while D:
                n_byte += 1
                salida.write(D)
                if n_byte == 0x25F:
                    print(D,"valor")
                    print(data_patch1[0])
                    salida.write(data_patch1[0])
                    #entrada.read(1)
                    n_byte += 1
                    #entrada.read(6)
                
                if n_byte == 0x260:
                    print(D,"valor")
                    for elemento in data_patch2:
                        print(elemento)
                        salida.write(elemento)
                    entrada.read(len(data_patch2)+1)
                D = entrada.read(1)

# Fin cronómetro
end = time.time()
elapsed = end - inicio 

# Calcular consumo de carbono
valor = 0.0000001233 * elapsed

print(f"\nTiempo de ejecución: {elapsed:.2f} segundos")
print(f"Consumo de carbono: {valor:e}")
