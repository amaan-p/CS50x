#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    int cntr = 0;
    do
    {
        n = get_int("Height: ");   //ask user for input
    }
    while (n < 1 ||  n > 8);

    for (int i = n ; i > 0 ; i--)
    {
        int scntr = n - cntr - 1;             //scntr control spaces of left triangle
        for (int j = 0; j < n; j++)    //makes left side
        {
            if (j >= scntr)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        printf("  ");
        for (int j = 0 ; j <= n; j++)     //make right side
        {
            if (j > cntr)
            {
                printf("");
            }
            else
            {
                printf("#");
            }
        }
        cntr++;
        scntr--;                      //counter to control flow of right pyramind
        printf("\n");
    }
}
