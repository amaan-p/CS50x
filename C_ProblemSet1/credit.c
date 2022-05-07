#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //declaration of variables
    long cntr = 0;
    long rem = 0;
    long newrem = 0;
    long remofnewrem = 0;
    long sum1 = 0;
    long sum2 = 0;
    long checksum = 0;
    long counter = 0;
    //take input
    long card_number = get_long("Number: ");
    long temp = card_number;
    long temp1 = card_number;
    long temp2 = card_number;
    //checksum
    while (temp != 0)
    {
        temp = temp / 10;
        rem = temp % 10;
        newrem = rem * 2;
        while (newrem != 0)
        {
            remofnewrem = newrem % 10;
            sum1 = sum1 + remofnewrem;  // adding individual digits
            newrem = newrem / 10;
        }
        temp = temp / 10;
    }
    while (temp1 != 0)
    {
        rem = temp1 % 10;
        sum2 = sum2 + rem;
        temp1 = temp1 / 10;
        temp1 = temp1 / 10;
    }
    while (card_number != 0)
    {
        cntr++;
        card_number = card_number / 10;
    }
    counter = cntr;
    while (temp2 != 0)  //counter for checking starting digits
    {
        temp2 = temp2 / 10;
        if (counter == 3)   //starting 2 digits
        {
            rem = temp2;
        }
        else if (counter == 2) // starting 1 digit
        {
            newrem = temp2;
        }
        counter--;
    }
    checksum = sum1 + sum2;
    if (checksum % 10 == 0 && (cntr == 13 || cntr == 16) && newrem == 4)
    {
        printf("VISA\n");
    }
    else if (checksum % 10 == 0 && cntr == 16 && (rem == 51 || rem == 52 || rem == 53 || rem == 54 || rem == 55))
    {
        printf("MASTERCARD\n");
    }
    else if (checksum % 10 == 0 && cntr == 15 && (rem == 34 || rem == 37))
    {
        printf("AMEX\n");
    }
    else
    {
        printf("INVALID\n");
    }

}

