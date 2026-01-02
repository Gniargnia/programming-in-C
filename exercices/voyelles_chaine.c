#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Exercice : Compter les voyelles dans une chaîne
// Objectif : Lire une chaîne et compter le nombre de voyelles (a, e, i, o, u, minuscules ou majuscules)
// Notions : chaînes, boucles, conditions
// Indice : Utilisez une boucle pour parcourir chaque caractère, vérifiez avec tolower et une condition

int main(void)
{
    // Demandez une chaîne avec get_string
    string s = get_string("Entrez une phrase: ");
    // Initialisez un compteur int count = 0;
    int count = 0;
    // Stocke la longueur de la chaîne
    int length = strlen(s);
    // Boucle for (int i = 0; i &lt; strlen(string); i++)
    for (int i = 0; i < length; i++)
    {
        // Si tolower(string[i]) est 'a', 'e', 'i', 'o', 'u', incrémentez count
        char c = tolower(s[i]);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u')
        {
            count += 1;
        }
    }
    printf("Nombre de voyelles: %i\n", count);
    
    // Affichez le nombre de voyelles avec printf

    return 0;
}