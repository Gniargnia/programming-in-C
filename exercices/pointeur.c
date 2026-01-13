#include <stdio.h>

int main(void)
{
    int x = 42;
    int *p = &x;
    *p = 100;

    printf("x vaut: %d\n", x);
    printf("p pointe vers: %p\n", (void*)p);
    printf("la valeur pointée par p: %d\n", *p);
}