import argparse
from pathlib import Path

# Configuración de los cambios binarios
CAMBIO_1 = 0x20F
CAMBIO_2 = 0x23D
BYTES_CAMBIO_1 = [b'\x00']
BYTES_CAMBIO_2 = [b'\xb8', b'\x00', b'\x00']

parser = argparse.ArgumentParser(description="Modificador de ejecutables")
parser.add_argument("input_file", help="Archivo ejecutable de entrada", type=Path)
args = parser.parse_args()
    
if args.input_file.is_file():
    output_file = Path(f"Parche{args.input_file.name}")
    
    # Leer el contenido binario original
    with args.input_file.open('rb') as file_in:
        file_data = bytearray(file_in.read())
        
    # Aplicar primer cambio
    for index, new_byte in enumerate(BYTES_CAMBIO_1):
        file_data[CAMBIO_1 + index] = ord(new_byte)
        
    # Aplicar segundo cambio  

    for index, new_byte in enumerate(BYTES_CAMBIO_2):
        file_data[CAMBIO_2 + index] = ord(new_byte)
        
    # Guardar archivo modificado
    with output_file.open('wb') as file_out:
        file_out.write(file_data)
        
    print(f"✓ Archivo modificado: {output_file.name}")