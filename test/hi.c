#include <cs50.h>
#include <stdio.h>

int main(void)
{
    char c1 = 'H';
    char c2 = 'I';
    char c3 = '!';
    
    string s = "HI!";
    
    string words[2];
    words[0] = "HI!";
    words[1] = "BYE!";

    printf("%c%c%c\n", c1, c2, c3);
    printf("%i %i %i\n", c1, c2, c3);
    
    printf("%s\n", s);
    // string is a specific kind of array!!!
    printf("%c%c%c\n", s[0], s[1], s[2]);
    printf("%i %i %i %i\n", s[0], s[1], s[2], s[3]);

    printf("%s\n%s\n", words[0], words[1]);
    // print each letter of each word, it's an array of an array.
    printf("%c%c%c\n", words[0][0], words[0][1], words[0][2]);
    printf("%c%c%c%c\n", words[1][0], words[1][1], words[1][2], words[1][3]);
    
}