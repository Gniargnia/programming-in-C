#include <cs50.h>
#include <stdio.h>

// Exercice 2 : Somme des pairs
// Objectif : Lire un tableau d'entiers et calculer la somme des éléments pairs
// Notions : tableaux, boucles, conditions, fonctions
// Indice : Utilisez un tableau dynamique, une boucle pour lire les valeurs, et une condition pour vérifier si pair (x % 2 == 0)

int main(void)
{
    // TODO : Demandez le nombre d'éléments N (get_int)
    const int N = get_int("Combien de nombres? ");
    // TODO : Déclarez un tableau int scores[N];
    int scores[N];
    // TODO : Utilisez une boucle pour lire N entiers dans le tableau
    int sum = 0;
    for (int i = 0; i < N; i++)
    {
        scores[i] = i + 1;
        if (scores[i] % 2 == 0)
        {
            sum += scores[i];
        }
    }
    printf("Sommes: %d\n", sum);
    // TODO : Calculez la somme des éléments pairs
    // Initialisez sum = 0
    // Boucle sur le tableau, si scores[i] % 2 == 0, ajoutez à sum

    // TODO : Affichez la somme avec printf

    return 0;
}