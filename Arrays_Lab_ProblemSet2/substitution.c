#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int validatekey(string key);

int main(int argc, string argv[])
{
    //check if number of arguments are incorrect
    if (argc > 2)
    {
        printf("Usage: ./Substitution key\n");
        return 1;
    }
    else if (argc < 2)
    {
        printf("Usage: ./Substitution key\n");
        return 1;
    }
    else
    {
        string key = argv[1];
        int validate = validatekey(key);
        if (validate != 0)
        {
            return 1;
        }
        else
        {
            //we prompt user to get plain key
            string word = get_string("plaintext: ");
            string ciphertext = malloc(strlen(word) + 1);
            char chr;
            ciphertext[0] = '\0';

            //make cipher text
            for (int i = 0; i < strlen(word); i++)
            {
                if (word[i] < 123 && word[i] > 96)
                {
                    // lower-casing corresponding plaintext to key into cipher
                    int index = (word[i] - 32) % 65;
                    chr = tolower(key[index]);
                    strncat(ciphertext, &chr, 1);

                }
                else if (word[i] < 65 || word[i] > 122)
                {
                    // handling special characters
                    chr = word[i];
                    strncat(ciphertext, &chr, 1);
                }
                else
                {
                    // upper-casing corresponding plaintext to key into cipher
                    int index = word[i] % 65;
                    chr = toupper(key[index]);
                    strncat(ciphertext, &chr, 1);
                }
            }
            //prints ciphertext
            printf("ciphertext: %s\n", ciphertext);
        }
    }
    return 0;
}

int validatekey(string key)
{
    //variables
    int alphacounter = 0;
    int repcounter = 0;
    //check if key contains 26 characters
    if (strlen(key) != 26)
    {
        printf("The Key must contain 26 characters\n");
        return 1;
    }
    else
    {
        //check if key is all alphabetical
        for (int i = 0; i < strlen(key); i++)
        {
            if (isalpha(key[i]))
            {
                alphacounter++;
            }
        }
        if (alphacounter != 26)
        {
            printf("Key must only contain alphabetic characters\n");
            return 1;
        }
        else
        {
            //check if key doent contain repeated characters
            for (int i = 0; i < strlen(key); i++)
            {
                for (int j = 0; j < strlen(key); j++)
                {
                    if (key[i] == key[j])
                    {
                        repcounter++;
                    }

                }
            }
        }
        //if not the under condition that means repatation occured
        if (repcounter != 26)
        {
            printf("Key must not contain repeated characters\n");
            return 1;
        }
    }
    return 0;
}