#include <cs50.h> 
#include <stdio.h>

// Prototype
float average(int lenght, int array[]);

// Constant
// const int N = 3;

int main(void)
{
    // Get scores
    int N = get_int("How many resuls? ");
    int scores[N];
    for (int i = 0; i < N; i++)
    {
        scores[i] = get_int("Scores: ");
    }

    // Print average
    printf("Average: %.2f\n", average(N, scores));
}

float average(int lenght, int array[])
{
    // Calculate average
    int sum = 0;
    for (int i = 0; i < lenght; i++)
    {
        sum += array[i];
    }
    return sum / (float) lenght;
}