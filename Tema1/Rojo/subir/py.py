import argparse
import sys
from pathlib import Path

def generate_patches(orig: bytes, patched: bytes) -> list[tuple[int, bytes, bytes]]:
    """
    Recorre ambos buffers y registra cada offset donde difieren.
    Devuelve una lista con: (offset, byte_original, byte_nuevo).
    """
    patches = []
    min_len = min(len(orig), len(patched))

    # Parchea diferencias dentro del rango común
    for i in range(min_len):
        if orig[i] != patched[i]:
            patches.append((i, orig[i:i+1], patched[i:i+1]))

    # Si el parcheado es más largo, agrega bytes extra
    if len(patched) > len(orig):
        for i in range(min_len, len(patched)):
            patches.append((i, b"", patched[i:i+1]))

    return patches

def apply_patches(data: bytearray, patches: list[tuple[int, bytes, bytes]]):
    """
    Aplica cada parche al bytearray, extendiendo si es necesario.
    """
    for offset, _, patch_bytes in patches:
        end = offset + len(patch_bytes)
        if end > len(data):
            data.extend(b'\x00' * (end - len(data)))
        data[offset:end] = patch_bytes

def main():
    parser = argparse.ArgumentParser(
        description="Detecta diferencias entre dos binarios y aplica esos cambios al original."
    )
    parser.add_argument("original", type=Path, help="Ruta al ejecutable original (ej. hackame.exe)")
    parser.add_argument("demo",     type=Path, help="Ejecutable parcheado por debugger (ej. b.exe)")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Ruta de salida (por defecto: <original>_patched<.ext>)"
    )
    args = parser.parse_args()

    # Validaciones
    if not args.original.is_file():
        sys.exit(f"ERROR: No existe el archivo original: {args.original}")
    if not args.demo.is_file():
        sys.exit(f"ERROR: No existe el binario parcheado: {args.demo}")

    out_path = args.output or args.original.with_name(
        f"{args.original.stem}_patched{args.original.suffix}"
    )

    # Lectura de bytes
    orig_bytes = args.original.read_bytes()
    demo_bytes = args.demo.read_bytes()

    # Generar y aplicar
    patches = generate_patches(orig_bytes, demo_bytes)
    if not patches:
        print("No se detectaron diferencias. Nada que parchear.")
        return

    print(f"Detectados {len(patches)} cambio(s):\n")
    for offset, old, new in patches:
        old_hex = old.hex() if old else "--"
        new_hex = new.hex()
        print(f"  Offset 0x{offset:08X}: {old_hex} -> {new_hex}")

    print("\nAplicando parches…")
    data = bytearray(orig_bytes)
    apply_patches(data, patches)

    # Escribir resultado
    out_path.write_bytes(data)
    print(f"\nEjecutable parcheado generado en:\n  {out_path}")

if __name__ == "__main__":
    main()
