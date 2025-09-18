parches = {
    528: 0x7F, 
    529: 0x4D,
    530: 0x90, 
    531: 0x90,
    532: 0x90, 
    533: 0x90,
    540: 0X90, 
    541: 0X90,
    542: 0X90,
    543: 0X90,
    544: 0X90,
    553: 0XEB,
    554: 0X34,
    555: 0X90,
    556: 0X90,
    557: 0X90,
    607: 0X39,
    608: 0XC0,
    609: 0X90,
    610: 0X90,
    611: 0X90,
    612: 0X90, 
}

cbt = -1
buf = None

with open("hackame.exe", "rb") as exe:
    buf = exe.read()
    with open("hackame_parcheadito.exe", "wb") as salida:
        for bt in buf:
            cbt += 1
            if cbt in parches:
                bt = parches[cbt] 
            salida.write(bt.to_bytes(1, 'little'))
        print("hackame.exe ha sido parcheado con éxito.")