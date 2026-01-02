#include <cs50.h>
#include <stdio.h>

int main (int argc, string argv[])
{
    printf("Hello, ");
    for (int i = 1; i < argc; i++)
    {
        printf("%s", argv[i]);
        printf(" ");
    }
    printf("\n");
}