#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void fill_random(int arr[], int n, int m);
void print_array(int arr[], int n);
void insertion_sort(int arr[], int n);

int main(void)
{
    srand(time(NULL));
    int N = get_int("Taille de la suite: ");
    int M = get_int("Max: ");

    int arr[N];

    fill_random(arr, N, M);

    print_array(arr, N);

    insertion_sort(arr, N);

    print_array(arr, N);
    
    return 0;
}

void fill_random(int arr[], int n, int m)
{
    for (int i = 0; i < n; i++)
    {
        arr[i] = (rand() / ((double) RAND_MAX + 1)) * m;
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

void insertion_sort(int arr[], int n)
{
    for (int i = 1; i < n; i++)
    { 
            int key = arr[i];
            int j = i - 1;

            while (j >= 0 && key < arr[j])
            {
                arr[j + 1] = arr[j];
                j--;
            }
            arr [j + 1] = key;   
    }
}
