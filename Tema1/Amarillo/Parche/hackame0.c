#include <stdio.h>

int valido = 0;
int main(int argc, char **argv){
    if (valido == 127){
        printf("Acceso Concedido");
    }else{
        printf("Acceso no concedido");
    }
    return 0;
}