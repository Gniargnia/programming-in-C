#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Exercice : Palindrome
// Objectif : Vérifier si une chaîne est un palindrome

bool est_palindrome(string str);

int main(void)
{
    string s = get_string("Entrez une chaîne : ");
    if (est_palindrome(s))
    {
        printf("C'est un palindrome.\n");
    }
    else
    {
        printf("Ce n'est pas un palindrome.\n");
    }
    return 0;
}

// TODO : Implémentez la fonction est_palindrome
bool est_palindrome(string str)
{
    // Votre code ici
    if (str == NULL || *str == '\0') return false;

    size_t length = strlen(str);

    for (size_t i = 0, j = length - 1; i < j; i++, j--)
    {
        if (str[i] != str[j])
        {
            return false;
        }
    }
    return true;
}