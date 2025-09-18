

parches = {
    528: 0x7F, 529: 0x4D,
    530: 0x90, 531: 0x90,
    532: 0x90, 533: 0x90,
    540: 0x90, 541: 0x90,
    542: 0x90, 543: 0x90,
    544: 0x90, 553: 0xEB,
    554: 0x34, 555: 0x90,
    556: 0x90, 557: 0x90,
    607: 0x39, 608: 0xC0,
    609: 0x90, 610: 0x90,
    611: 0x90, 612: 0x90,
}

INPUT = "hackame.exe"
OUTPUT = "hackame_parchado.exe"

# Verificar si el archivo existe
try:
    with open(INPUT, "rb") as f:
        buf = f.read()
except FileNotFoundError:
    print(f"Error: no se encontró '{INPUT}'.")
    exit()

# Aplicar parches
cbt = -1
with open(OUTPUT, "wb") as salida:
    for bt in buf:
        cbt += 1
        if cbt in parches:
            bt = parches[cbt]
        salida.write(bt.to_bytes(1, 'little'))

print(f"{INPUT} ha sido parchado con éxito -> {OUTPUT}")
