import argparse
import sys
from pathlib import Path

def apply_patches(data: bytearray, patches: list[tuple[int, bytes]]):
    """
    Aplica los parches predefinidos al archivo.
    """
    for offset, patch_bytes in patches:
        end = offset + len(patch_bytes)
        if end > len(data):
            data.extend(b'\x00' * (end - len(data)))  # Rellena si es necesario
        data[offset:end] = patch_bytes

def main():
    parser = argparse.ArgumentParser(
        description="Aplica parches predefinidos a un archivo binario."
    )
    parser.add_argument("archivo", type=Path, help="Archivo original a parchear")
    parser.add_argument(
        "-o", "--output", type=Path,
        help="Archivo de salida (por defecto: <original>_patched<.ext>)"
    )
    args = parser.parse_args()

    if not args.archivo.is_file():
        sys.exit(f"ERROR: No existe el archivo: {args.archivo}")

    data = bytearray(args.archivo.read_bytes())
    out_path = args.output or args.archivo.with_name(f"{args.archivo.stem}_patched{args.archivo.suffix}")

    # 🔹 Parche específico basado en los cambios detectados
    patches = [
        (0x324, b'\x43'),  # d8 -> 43
        (0x325, b'\xff')   # fe -> ff
    ]

    print(f"Aplicando {len(patches)} parche(s)…")
    apply_patches(data, patches)
    out_path.write_bytes(data)
    print(f"\nArchivo parcheado generado en:\n  {out_path}")

if __name__ == "__main__":
    main()
