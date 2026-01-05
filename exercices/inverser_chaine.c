#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Exercice : Inverser une chaîne
// Objectif : Inverser l'ordre des caractères d'une chaîne

void inverser_chaine(char *str);

int main(void)
{
    char *s = get_string("Entrez une chaîne : ");
    inverser_chaine(s);
    printf("Chaîne inversée : %s\n", s);
    return 0;
}

// TODO : Implémentez la fonction inverser_chaine
void inverser_chaine(char *str)
{
    if (str == NULL || *str == '\0') return;
    
    size_t length = strlen(str);
    
    for (size_t i = 0, j = length - 1; i < j; i++, j--)
    {
        char c = str[i];
        str[i] = str[j];
        str[j] = c;
    }
}