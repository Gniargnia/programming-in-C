#include <cs50.h>
#include <stdio.h>

// Exercice 1 : Motif en boucle
// Objectif : Utiliser des boucles for imbriquées pour imprimer un triangle de '*'
// Notions : boucles, printf, constantes
// Indice : Pensez à une boucle externe pour les lignes, et une interne pour les colonnes.

int main(void)
{
    // TODO : Demandez à l'utilisateur la hauteur du triangle (entre 1 et 10)
    // Utilisez get_int pour lire un entier
    int height = get_int("Quelle hauteur de triangle? ");
    // TODO : Utilisez une boucle for pour chaque ligne (de 0 à hauteur-1)
    // Dans chaque ligne, utilisez une autre boucle for pour imprimer '*' (de 0 à i)
    for (int i = 0; i < height; i++)
    {
        // Comme la valeur de i augmente de 1 à chaque itération et que j est réinitialiser à 0 à chaque itération il y a un effet pyramidal
        for (int j = 0; j <= i; j++)
        {
            printf("*");
        }
        printf("\n");
    }
    // Exemple pour hauteur=3 :
    // *
    // **
    // ***

    return 0;
}