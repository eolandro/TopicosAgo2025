import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Extraer streams OGV de un archivo")
parser.add_argument("archivo", type=Path, help="Archivo con streams OGV")
args = parser.parse_args()

def extraer_ogv(archivo, output_dir="extraidos"):
    PATRON_OGG = b"OggS"
    data = archivo.read_bytes()
    Path(output_dir).mkdir(exist_ok=True)

    idx = 0
    stream_num = 0

    while stream_num<2:
        start = data.find(PATRON_OGG, idx)
        if start == -1:
            break

        end = data.find(PATRON_OGG, start + 4)
        while end != -1:
            header = data[end:end+27]
            if len(header) < 27:
                break
            header_type = header[5]
            if header_type & 0x04:
                end += len(header)
                break
            end = data.find(PATRON_OGG, end + 4)

        if end == -1:
            end = len(data)

        salida = Path(output_dir) / f"ogv_{stream_num}.ogv"
        salida.write_bytes(data[start:end])
        print(f"[+] Archivo extraído: {salida}")
        stream_num += 1
        idx = end

    print(f"Se extrajeron {stream_num} OGV")

extraer_ogv(args.archivo)
