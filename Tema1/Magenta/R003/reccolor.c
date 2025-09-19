// color_recon.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

/*
 Reconstrucción del comportamiento visto en el decompiler:
 - Cabecera P6 (15 bytes): "P6\n640 480\n255\n"
 - Seeding: srand(time(NULL))
 - Loop: height = 0x1e0 (480), width = 0x280 (640)
 - Por cada píxel escribe 3 bytes generados con rand()%0x100, usando fwrite(&byte,1,1,f)
*/

int main(void) {
    /* Constantes encontradas en el decompilado */
    const int WIDTH  = 0x280; // 640
    const int HEIGHT = 0x1e0; // 480

    /* Cabecera exacta (15 bytes) encontrada en DAT_00402000 */
    const unsigned char header[] = "P6\n640 480\n255\n"; /* longitud 15 */

    
    const char fname = "s_sample.ppm"; / reemplaza por la cadena exacta si es otra */

    FILE f = fopen(fname, "wb"); / en decompiler aparece fopen(..., &DAT_00402023) */
    if (!f) {
        perror("fopen");
        return 1;
    }

    
    if (fwrite(header, 1, sizeof(header)-1, f) != sizeof(header)-1) {
        perror("fwrite header");
        fclose(f);
        return 1;
    }

    time_t t = time(NULL);
    srand((unsigned int)t);

    unsigned char tmp;
    for (int y = 0; y < HEIGHT; ++y) {
        for (int x = 0; x < WIDTH; ++x) {
            /* R */
            tmp = (unsigned char)(rand() % 0x100);
            fwrite(&tmp, 1, 1, f);
            /* G */
            tmp = (unsigned char)(rand() % 0x100);
            fwrite(&tmp, 1, 1, f);
            /* B */
            tmp = (unsigned char)(rand() % 0x100);
            fwrite(&tmp, 1, 1, f);
        }
    }

    fclose(f);
    return 0;
}
