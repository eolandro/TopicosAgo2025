#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void)
{
    FILE *file;
    int i, j;
    int random_value;
    unsigned char pixel_component;
    
    // Cabecera PPM (P6 indica formato binario, 640x480, máximo valor 255)
    const char *ppm_header = "P6\n640 480\n255\n";
    
    // Inicializar generador de números aleatorios
    srand((unsigned int)time(NULL));
    
    // Abrir archivo para escritura binaria
    file = fopen("sample_reconstructed.ppm", "wb");
    if (file == NULL) {
        printf("Error: No se pudo crear el archivo\n");
        return 1;
    }
    
    // Escribir cabecera PPM (15 bytes)
    fwrite(ppm_header, 1, 15, file);
    
    // Generar imagen de 480x640 píxeles (alto x ancho)
    for (i = 0; i < 480; i++) {          // 0x1e0 = 480 decimal
        for (j = 0; j < 640; j++) {      // 0x280 = 640 decimal
            // Componente Rojo (0-255)
            random_value = rand();
            pixel_component = (unsigned char)(random_value % 256);
            fwrite(&pixel_component, 1, 1, file);
            
            // Componente Verde (0-255)
            random_value = rand();
            pixel_component = (unsigned char)(random_value % 256);
            fwrite(&pixel_component, 1, 1, file);
            
            // Componente Azul (0-255)
            random_value = rand();
            pixel_component = (unsigned char)(random_value % 256);
            fwrite(&pixel_component, 1, 1, file);
        }
    }
    
    fclose(file);
    printf("Archivo sample_reconstructed.ppm generado exitosamente\n");
    printf("Dimensiones: 640x480 pixels (formato PPM P6)\n");
    
    return 0;
}
