#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string s = get_string("Input:  ");
    printf("Output: ");
    for (int i = 0, n = strlen(s); i < n; i++ )
    {
        // Compare la valeur ASCII des caractères, c'est une manipulation d'int en fait.
        if (s[i] >= 'a' && s[i] <= 'z')
        {
            // Capitalise les lettres minuscules
            printf("%c", s[i] - ('a' - 'A'));
        }
        else
        {
            // Laisse les lettres majuscules intactes
            printf("%c", s[i]);
        }
    }
    printf("\n");
    
    // Version compacte avec la fonction toupper()
    printf("Output: ");
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        printf("%c", toupper(s[i]));
    }
    printf("\n");
    
}