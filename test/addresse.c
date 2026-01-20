#include <stdio.h>

int main(void)
{
    int n = 50;
    int *p = &n;
    
    printf("Adresse de n        : %p\n", (void*)&n);
    printf("Valeur de p         : %p\n", (void*)p);
    printf("Adresse de p        : %p\n", (void*)&p);
    printf("Valeur pointée (*p) : %d\n", *p); 
}