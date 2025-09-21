#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    FILE *f;
    int w = 1280, h = 720;
    unsigned char pixel[3];
    int i, j;

    // Nombre fijo del archivo
    const char *filename = "imagen.ppm";

    // Abrir archivo para escritura (sobrescribe si existe)
    f = fopen(filename, "wb");
    if (!f) {
        printf("Error al crear el archivo\n");
        return 1;
    }

    // Escribir cabecera del PPM
    fprintf(f, "P6\n%d %d\n255\n", w, h);

    // Inicializar semilla aleatoria
    srand((unsigned int)time(NULL));

    // Generar imagen con colores aleatorios
    for (i = 0; i < h; i++) {
        for (j = 0; j < w; j++) {
            pixel[0] = rand() % 256; // Rojo
            pixel[1] = rand() % 256; // Verde
            pixel[2] = rand() % 256; // Azul
            fwrite(pixel, 1, 3, f);
        }
    }

    fclose(f);
    printf("Imagen creada: %s (sobrescribe la anterior)\n", filename);
    return 0;
}
