#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    int random_value;
    time_t current_time;
    FILE *file;
    unsigned char color_component;

    // Inicializar generador de números aleatorios
    current_time = time(NULL);
    srand((unsigned int)current_time);

    // Crear archivo PPM en modo escritura binaria
    file = fopen("reconstruido.ppm", "wb");
    if (file == NULL) {
        printf("Error: No se pudo crear el archivo\n");
        return 1;
    }

    // Escribir header PPM CORRECTO (14 bytes con saltos de línea)
    fputs("P6\n640 480\n255\n", file);

    // Generar píxeles aleatorios (640x480)
    for (int y = 0; y < 480; y++) {
        for (int x = 0; x < 640; x++) {
            // Componente ROJO
            random_value = rand();
            color_component = (unsigned char)(random_value % 256);
            fwrite(&color_component, 1, 1, file);

            // Componente VERDE
            random_value = rand();
            color_component = (unsigned char)(random_value % 256);
            fwrite(&color_component, 1, 1, file);

            // Componente AZUL
            random_value = rand();
            color_component = (unsigned char)(random_value % 256);
            fwrite(&color_component, 1, 1, file);
        }
    }

    // Cerrar archivo
    fclose(file);
    printf("Imagen reconstruido.ppm generada con éxito!\n");
    
    return 0;
}

