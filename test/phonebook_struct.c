#include <cs50.h>
#include <stdio.h>
#include <string.h>

/* Créer un type structure */
typedef struct
{
    string name;
    string number;

} person;

int main(void)
{
    person people[3];

    // Pour accéder au composants de la structure, on utilise le '.'
    people[0].name = "David";
    people[0].number = "893-2344";

    people[1].name = "John";
    people[1].number = "324-2342";

    people[2].name = "Jo";
    people[2].number = "243-2342";

    string name = get_string("Name: ");
    for (int i = 0; i < 3; i++)
    {
        if (strcmp(people[i].name, name) == 0)
        {
            printf("Found: %s\n", people[i].number);
            return 0;
        }
    }
    printf("Not found\n");
    return 1;
}