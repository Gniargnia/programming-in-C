#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int dollar = 1;
    while (true)
    {
        char c = get_char("Je te donne %i $. Double le et donne le à la prochaine personne ? ", dollar);
        if (c == 'y')
        {
            dollar *= 2;
        }
        else
        {
            break;
        }
    } 
}

