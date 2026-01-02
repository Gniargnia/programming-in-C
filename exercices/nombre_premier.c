#include <cs50.h>
#include <math.h>
#include <stdio.h>

// Exercice 4 : Nombre premier
// Objectif : Écrire une fonction qui vérifie si un nombre est premier
// Notions : fonctions, boucles, conditions
// Indice : Un nombre premier >1 n'est divisible que par 1 et lui-même. Testez les diviseurs de 2 à sqrt(n).

bool est_premier(long long n);
void print_bool(bool b);

int main(void)
{
    // TODO : Lisez un entier positif avec get_int
    long long i = get_long_long("What number? ");
    // TODO : Appelez la fonction est_premier et affichez le résultat
    printf("Est premier : ");
    print_bool(est_premier(i));
    printf("\n");
    return 0;
}

// TODO : Implémentez la fonction bool est_premier(int n)
bool est_premier(long long n)
{
// Retourne true si premier, false sinon
// Pour n <= 1, false
    if (n <= 1)
    {
        return false;
    }
    if (n == 2)
    {
        return true;
    }
    if (n % 2 == 0)
        return false;
    // Boucle de 2 à n-1, si divisible, false
    // Sinon true
    for (long long i = 3; i * i <= n; i++)
    {
        if (n % i == 0)
        {
            return false;
        }
    }
    return true;
}

void print_bool(bool b)
{
    printf("%s", b ? "oui" : "non");
}