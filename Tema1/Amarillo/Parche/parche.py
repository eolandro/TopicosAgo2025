parches = {
    528: 0x7F, 529: 0x4D, 530: 0x90, 531: 0x90, 532: 0x90, 
    533: 0x90, 540: 0x90, 541: 0x90, 542: 0x90, 543: 0x90, 
    544: 0x90, 553: 0xEB, 554: 0x34, 555: 0x90, 556: 0x90, 
    557: 0x90, 607: 0x39, 608: 0xC0, 609: 0x90, 610: 0x90, 
    611: 0x90, 612: 0x90
}

with open("hackame.exe", "rb") as archivo:
    datos = bytearray(archivo.read())

for posicion, valor in parches.items():
    if posicion < len(datos):
        datos[posicion] = valor

with open("hackame_parcheAp.exe", "wb") as archivo:
    archivo.write(datos)

print("Parchado correctamente")