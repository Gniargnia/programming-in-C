#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Exercice : Maximum dans un tableau
// Objectif : Lire un tableau d'entiers et trouver la valeur maximale
// Notions : tableaux, boucles, variables
// Indice : Initialisez max avec le premier élément, puis comparez dans une boucle

int main(void)
{
    // Demandez le nombre d'éléments N (get_int)
    int N = get_int("Nombre d'éléments: ");

    // Déclarez un tableau int numbers[N];
    int numbers[N];

    // Remplir le tableau de nombres
    for (int i = 0; i < N; i++)
    {
        numbers[i] = get_int("Entrez un nombre: ");
    }
    // Initialisez max = numbers[0]
    int max = numbers[0];

    // Utilisez une boucle pour lire N entiers dans le tableau
    for (int i = 1; i < N; i++)
    {
        // Boucle pour comparer chaque élément avec max
        if (numbers[i] > max)
        {
            max = numbers[i];
        }
    }
    // TODO : Affichez le maximum avec printf
    printf("Max: %i\n", max);

    return 0;
}