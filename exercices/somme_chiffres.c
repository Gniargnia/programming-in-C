#include <cs50.h>
#include <stdio.h>

// Exercice : Somme des chiffres
// Objectif : Calculer la somme des chiffres d'un nombre entier positif

int somme_chiffres(long long n);

int main(void)
{
    long long num = get_long_long("Entrez un nombre : ");
    printf("Somme des chiffres : %d\n", somme_chiffres(num));
    return 0;
}

// TODO : Implémentez la fonction somme_chiffres
int somme_chiffres(long long n)
{
    // Votre code ici
}