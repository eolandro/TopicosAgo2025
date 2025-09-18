#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int FUN_00401000(void) {
    int iVar1;
    time_t tVar2;
    FILE *fp;
    unsigned char pixel;
    int row, col;

    // Dimensiones
    int width = 640;   // 0x280
    int height = 480;  // 0x1E0
    int maxval = 255;

    // Inicializar semilla aleatoria
    tVar2 = time(NULL);
    srand((unsigned int)tVar2);

    // Abrir archivo
    fp = fopen("color.ppm", "wb");
    if (!fp) {
        perror("Error al abrir el archivo");
        return 1;
    }

    // Escribir cabecera PPM P6
    // P6 = formato para color rgb
    // width height maxval
    fprintf(fp, "P6\n%d %d\n%d\n", width, height, maxval);

    // Generar pixeles aleatorios
    for (row = 0; row < height; row++) {
        for (col = 0; col < width; col++) {
            // 3 valores aleatorios por píxel para replicar ensamblador
            iVar1 = rand();
            pixel = (unsigned char)(iVar1 % 256);
            fwrite(&pixel, 1, 1, fp);

            iVar1 = rand();
            pixel = (unsigned char)(iVar1 % 256);
            fwrite(&pixel, 1, 1, fp);

            iVar1 = rand();
            pixel = (unsigned char)(iVar1 % 256);
            fwrite(&pixel, 1, 1, fp);
        }
    }

    fclose(fp);
    return 0;
}

int main() {
    return FUN_00401000();
}
