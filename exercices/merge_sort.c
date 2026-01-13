#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void fill_random(int arr[], int n, int m);
void print_array(int arr[], int n);
void merge_sort(int arr[], int n);
void merge_sort_recursion(int arr[], int l, int r);
void merge_sorted_array(int arr[], int l, int m, int r);

int main(void)
{
    srand(time(NULL));
    int N = get_int("Taille de la suite: ");
    int M = get_int("Max: ");

    int arr[N];

    fill_random(arr, N, M);

    print_array(arr, N);

    merge_sort(arr, N);

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

void merge_sort(int arr[], int n)
{
    merge_sort_recursion(arr, 0, n - 1);
}

void merge_sort_recursion(int arr[], int l, int r)
{
    if (l < r)
    {
        int m = l + (r - l) / 2;

        merge_sort_recursion(arr, l, m);
        merge_sort_recursion(arr, m + 1, r);

        merge_sorted_array(arr, l, m, r);
    } 
}

void merge_sorted_array(int arr[], int l, int m, int r)
{
    int left_lenght = m - l + 1;
    int right_lenght = r - m;

    int temp_left[left_lenght];
    int temp_right[right_lenght];

    for (int i = 0; i < left_lenght; i++)
    {
        temp_left[i] = arr[l + i];
    }

    for (int i = 0; i < right_lenght; i++)
    {
        temp_right[i] = arr[m + 1 + i];
    }
    
    for(int i = 0, j = 0, k = l; k <= r; k++)
    {
        if ((i < left_lenght) && 
            (j >= right_lenght || temp_left[i] <= temp_right[j]))
        {
            arr[k] = temp_left[i];
            i++;
        }
        else
        {
            arr[k] = temp_right[j];
            j++;
        }
    }
}
