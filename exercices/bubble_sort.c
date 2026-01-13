#define _DEFAULT_SOURCE
#include <cs50.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

void bubble_sort(int arr[], int n);
void fill_random(int arr[], int n, int e);
void print_array(int arr[], int n);

int main(void)
{
    srandom(time(NULL));

    int N = get_int("Taille de la suite: ");
    int I = get_int("Invervalle de la suite: ");

    int arr[N];

    fill_random(arr, N, I);

    print_array(arr, N);
    
    bubble_sort(arr, N);

    print_array(arr, N);

    printf("\n");
    return 0;
}

void fill_random(int arr[], int n, int e)
{
    for (int i = 0; i < n; i++)
    {
        arr[i] = (random() / ((double) RAND_MAX + 1)) * e;
    }
}

void print_array(int arr[], int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void bubble_sort(int arr[], int n)
{
    int swapped = 1;
    int pass = 0;

    while (swapped)
    {
        swapped = 0;
        for (int i = 0; i < n - 1 - pass; i++)
        {
            if (arr[i] > arr[i + 1])
                {
                    int tmp = arr[i];
                    arr[i] = arr[i + 1];
                    arr[i + 1] = tmp;
                    swapped = 1;
                }           
        }
        pass ++;
    }
}