// MSYS2 UCRT64
// cd "/c/Users/danie/OneDrive/Documentos/TecNM/Semestre 9/Topicos de Ciberseguridad/U1/R003"
// gcc color2.c -o color2.exe

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#define width 640  // 0x280
#define height 480 // 0x1e0

// El formato PPM / P6 guarda cada pixel como RGB en binario
// R = 1 byte, G = 1 byte, B = 1 byte
// total de 3 bytes por píxel
int main(void)
{
    // fopen(...)  <--- corresponde a: DAT_0040219c = fopen(s_sample.ppm_00402018,&DAT_00402023);
    // Abrimos/creamos el archivo "sample.ppm" en modo binario para escritura
    // En Ghidra el DAT_0040219c guarda el FILE* devuelto por fopen
    FILE *file = fopen("sample.ppm", "wb");
    if (!file)
    {
        perror("Error al abrir sample.ppm");
        return 1;
    }


    // En el exe hay 15 bytes en memoria (DAT_00402000) y conforman el encabezado del archivo PPM
    // Encabezado de 15 bytes: "P6 640 480 255\n o P6\n640 480\n255\n" 

    // La primera "línea" es un identificador PPM mágico Puede ser "P3" o "P6" (¡sin incluir las comillas dobles!). 
    // El siguiente La línea consta del ancho y la altura de la imagen como números ASCII. 
    // La última parte del encabezado proporciona el valor máximo del color componentes para los píxeles, 
    // esto permite que el formato describa más de valores de color de un solo byte (0,255).

    // fwrite(&DAT_00402000, 1, 0x0F, DAT_0040219c);
    const char header[] = "P6\n640 480\n255\n";
    if (fwrite(header, 1, sizeof(header) - 1, file) != sizeof(header) - 1)
    {
        perror("Error al escribir el encabezado");
        fclose(file);
        return 1;
    }

    // tVar2 = time((time_t *)0x0);
    // DAT_00402198 = (uint)tVar2;
    // srand(DAT_00402198);
    srand((unsigned)time(NULL));

    // el bucle de filas y columnas en el codigo del exe en Ghidra es
    // for (DAT_00402010 = 0; DAT_00402010 < 0x1e0; DAT_00402010++)
    // for (DAT_00402014 = 0; DAT_00402014 < 0x280; DAT_00402014++)
    // se sustituye en el for (y:0..479) y for (x:0..639)
    // en cada paso del for se generan 3 valores rand() % 256 y se escriben
    uint8_t pixel[3];
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            // En Ghidra:
            // iVar1 = rand();
            // DAT_0040200f = (undefined1)(iVar1 % 0x100);
            // fwrite(&DAT_0040200f,1,1,DAT_0040219c);

            pixel[0] = (uint8_t)(rand() % 256); // R  <- primer rand() % 0x100
            pixel[1] = (uint8_t)(rand() % 256); // G  <- segundo rand() % 0x100
            pixel[2] = (uint8_t)(rand() % 256); // B  <- tercer rand() % 0x100

            // en el codigo que nos da ghidra se hacen tres fwriteseguidos
            // esto se puede hacer en un solo paso
            if (fwrite(pixel, 1, 3, file) != 3)
            {
                perror("Error al escribir píxeles");
                fclose(file);
                return 1;
            }
        }
    }

    // fclose(DAT_0040219c);
    // cerrar el archivo
    fclose(file);
    return 0;
}

/*
unsigned char pixel;
for (int y = 0; y < height; y++)
{
    for (int x = 0; x < width; x++)
    {
        // Canal R
        pixel = (unsigned char)(rand() % 256);
        fwrite(&pixel, 1, 1, file);

        // Canal G
        pixel = (unsigned char)(rand() % 256);
        fwrite(&pixel, 1, 1, file);

        // Canal B
        pixel = (unsigned char)(rand() % 256);
        fwrite(&pixel, 1, 1, file);
    }
}
*/
