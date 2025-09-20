import time

# Constantes rand() 
RAND_MAX = 0x7fff  # 32767
a = 214013
c = 2531011
mod = 2**32

class CRand:
    def __init__(self, semilla):
        self.semilla = semilla

    def rand(self):
        self.semilla = (a * self.semilla + c) % mod
        return (self.semilla >> 16) & 0x7fff  # MSVC

# Inicialización de semilla 
semilla = int(time.time())
rand_gen = CRand(semilla)

nombreArchivo = "ejemplo.ppm"

# Cabecera del archivo original (0xF bytes)
header = b"P6\n640 480\n255\n"

with open(nombreArchivo, "wb") as f:
    f.write(header)
    for y in range(480):
        for x in range(640):
            r = rand_gen.rand() % 256
            g = rand_gen.rand() % 256
            b = rand_gen.rand() % 256
            f.write(bytes([r, g, b]))
print(f"""
      --------------------------------------------
      Archivo '{nombreArchivo}' generado correctamente.
      --------------------------------------------
      """)