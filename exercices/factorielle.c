#include <cs50.h>
#include <stdio.h>

// Exercice : Calcul de factorielle
// Objectif : Calculer la factorielle d'un nombre entier positif N (N! = 1 * 2 * ... * N)
// Notions : boucles, variables
// Indice : Utilisez une boucle pour multiplier de 1 à N, initialisez result = 1

int main(void)
{
    // TODO : Demandez un entier positif N avec get_int (vérifiez N &gt;= 0)
    int N;
    do
    {
        N = get_int("What number? ");
    } 
    while (N < 0);   
    // TODO : Initialisez long long result = 1; (pour éviter overflow)
    long long result = 1;
    // TODO : Boucle for (int i = 1; i &lt;= N; i++) result *= i;
    for (int i = 1; i <= N; i++)
    {
        result *= i;
    }
    // TODO : Affichez la factorielle avec printf
    printf("Factorielle: %lld\n", result);

    return 0;
}