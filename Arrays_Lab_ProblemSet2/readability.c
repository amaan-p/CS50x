#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int main(void)
{
    //decalring variables
    float no_of_letters = 0;
    float no_of_words = 0;
    float no_of_sentences = 0;
    float index = 0;
    int grade = 0;
    //taking input
    string text = get_string("Text: ");
    //assinging values in variables
    no_of_letters = count_letters(text);
    no_of_words = count_words(text);
    no_of_sentences = count_sentences(text);
    //testing
    //printf("%f\n",no_of_letters);
    // printf("%f\n",no_of_words);
    // printf("%f\n",no_of_sentences);

    //Coleman-Liau Index
    index = 0.0588 * (100 * no_of_letters / no_of_words) - 0.296 * (100 * no_of_sentences / no_of_words) - 15.8;
    grade = round(index);
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", grade);
    }


}


//function to count letters
int count_letters(string text)
{
    int length = strlen(text);
    int no_letters = 0;
    for (int i = 0; i < length; i++)
    {
        if (isalpha(text[i]))
        {
            no_letters++;
        }
    }
    return no_letters;
}
//function to count words
int count_words(string text)
{
    int length = strlen(text);
    int no_words = 0;
    for (int i = 0; i < length; i++)
    {
        if (text[i] == 32)
        {
            no_words++;
        }
    }
    return no_words + 1;
}
//functions to count sentences
int count_sentences(string text)
{
    int length = strlen(text);
    int no_sentences = 0;
    for (int i = 0; i < length; i++)
    {
        //ascii 46 ".", 33 "!",63 "?"
        if (text[i] == 46 || text[i] == 33 || text[i] == 63)
        {
            no_sentences++;
        }
    }
    return no_sentences;
}