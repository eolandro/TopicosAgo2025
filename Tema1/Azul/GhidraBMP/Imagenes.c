#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    FILE *file;
    int x, y;
    unsigned char r, g, b;

    srand((unsigned int)time(NULL));

    file = fopen("output.bmp", "wb");
    if (!file) return 1;

    unsigned char header[54] = {
        'B','M',
        0,0,0,0,
        0,0,0,0,
        54,0,0,0,
        40,0,0,0,
        0,0,0,0,
        0,0,0,0,
        1,0,
        24,0,
        0,0,0,0,
        0,0,0,0,
        0,0,0,0,
        0,0,0,0,
        0,0,0,0,
        0,0,0,0
    };

    int width = 640;
    int height = 480;
    int imageSize = 3 * width * height;
    int fileSize = imageSize + 54;

    *(int*)&header[2] = fileSize;
    *(int*)&header[18] = width;
    *(int*)&header[22] = height;
    *(int*)&header[34] = imageSize;

    fwrite(header, 1, 54, file);

    for (y = 0; y < height; y++) {
        for (x = 0; x < width; x++) {
            b = rand() % 256;
            g = rand() % 256;
            r = rand() % 256;
            fwrite(&b, 1, 1, file);
            fwrite(&g, 1, 1, file);
            fwrite(&r, 1, 1, file);
        }
    }

    fclose(file);
    return 0;
}