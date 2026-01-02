#include <cs50.h>
#include <stdio.h>
#include <string.h>

int string_lenght(string s);

int main(void)
{
    string name = get_string("Name: ");
    int lenght = string_lenght(name);
    int lenght_2 = strlen(name);
    // Produit 2 lettres pour les lettres avec accents
    printf("Il y a %i (%i) lettres dans ton nom.\n", lenght, lenght_2);

}

int string_lenght(string s)
{
    int lenght = 0;
    int i = 0;
    while (s[i] != '\0')
    {
        if (s[i] != ' ')
        {
            lenght++;
        }
    i++;
    }
    return lenght;
}