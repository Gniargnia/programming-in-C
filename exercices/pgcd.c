#include <cs50.h>
#include <stdio.h>

// Exercice : PGCD
// Objectif : Calculer le PGCD de deux nombres entiers positifs

int pgcd(int a, int b);

int main(void)
{
    int x = get_int("Entrez le premier nombre : ");
    int y = get_int("Entrez le deuxième nombre : ");
    printf("PGCD : %d\n", pgcd(x, y));
    return 0;
}

// TODO : Implémentez la fonction pgcd
int pgcd(int a, int b)
{
    // Votre code ici
}