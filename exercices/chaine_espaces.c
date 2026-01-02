#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Exercice 3 : Compter les espaces
// Objectif : Lire une chaîne et compter le nombre d'espaces (' ')
// Notions : chaînes, boucles, strlen
// Indice : Parcourez la chaîne caractère par caractère, incrémentez un compteur quand vous trouvez ' '

int main(void)
{
    // TODO : Lisez une chaîne avec get_string("Entrez une phrase : ")
    string s = get_string("Entrez une phrase: ");
    // TODO : Initialisez un compteur int espaces = 0;
    int espaces = 0;
    // TODO : Utilisez une boucle for (int i = 0; i < strlen(s); i++)
    // Si s[i] == ' ', espaces++;
    int lenght = strlen(s); 
    for (int i = 0; i < lenght; i++)
    {
        if (s[i] == ' ')
        {
            espaces++;
        }
    }
        
    // TODO : Affichez le nombre d'espaces avec printf
    printf("%i\n", espaces);
    return 0;
}