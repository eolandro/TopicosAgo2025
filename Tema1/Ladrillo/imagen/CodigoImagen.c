#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void)
{
    time_t seed;
    FILE *arch;
    int x, y;
    unsigned char pixel;
    
    seed = time(NULL);
    srand((unsigned int)seed);
    
    arch = fopen("sample.ppm", "wb");
    if (!arch) {
        printf("Error al crear el archivo\n");
        return 1;
    }
    
    fprintf(arch, "P6\n640 480\n255\n");
    
    for (y = 0; y < 480; y++) {
        for (x = 0; x < 640; x++) {
            pixel = rand() % 256;
            fwrite(&pixel, 1, 1, arch);
            pixel = rand() % 256;
            fwrite(&pixel, 1, 1, arch);
            pixel = rand() % 256;
            fwrite(&pixel, 1, 1, arch);
        }
    }
    
    fclose(arch);
    printf("Imagen de ruido generada: sample.ppm\n");
    
    return 0;
}