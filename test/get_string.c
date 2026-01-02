#include <cs50.h>
#include <stdio.h>

int main(void) {
    string name = get_string("Quel est ton nom? ");
    printf("Bonjour, %s\n", name);
}