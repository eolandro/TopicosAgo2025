#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int FUN_00401000(void);

int main() {
    clock_t start, end;
    double cpu_time_used;

    // Iniciar contador de tiempo
    start = clock();

    int result = FUN_00401000();

    // Terminar contador de tiempo
    end = clock();

    // Calcular segundos que tardó en correr
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;

    // Calcular consumo de carbono
    double valor = 0.0000001233 * cpu_time_used;

    printf("\nTiempo de ejecución: %.2f segundos\n", cpu_time_used);
    printf("Consumo de carbono: %e\n", valor);
    fflush(stdout);

    return 0;
}

int FUN_00401000(void) {
    int iVar1;
    time_t tVar2;
    FILE *file;
    unsigned char byte;

    // Obtener tiempo actual y usarlo como semilla
    tVar2 = time(NULL);
    srand((unsigned int)tVar2);

    // Abrir archivo en modo binario para escritura
    file = fopen("s_sample4.ppm", "wb");

    // Escribir cabecera PPM (formato P6)
    fwrite("P6\n640 480\n255\n", 1, 15, file);  // 0xF bytes

    // Doble bucle anidado para generar imagen 640x480
    for (int y = 0; y < 480; y++) {            // 0x1e0
        for (int x = 0; x < 640; x++) {        // 0x280
            // Generar R
            iVar1 = rand();
            byte = (unsigned char)(iVar1 % 256);
            fwrite(&byte, 1, 1, file);

            // Generar G
            iVar1 = rand();
            byte = (unsigned char)(iVar1 % 256);
            fwrite(&byte, 1, 1, file);

            // Generar B
            iVar1 = rand();
            byte = (unsigned char)(iVar1 % 256);
            fwrite(&byte, 1, 1, file);
        }
    }

    // Cerrar archivo
    fclose(file);
    return 0;
}
