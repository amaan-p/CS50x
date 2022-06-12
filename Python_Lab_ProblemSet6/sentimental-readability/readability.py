from cs50 import get_string
import re


def main():
    text = get_string("Text: ")
    # no of letters
    no_of_letters = count_letters(text)
    # no of words
    no_of_words = count_words(text)
    # no of sentences
    no_of_sentences = count_sentences(text)
    # Coleman-Liau Index
    index = 0.0588 * (100 * no_of_letters / no_of_words) - 0.296 * (100 * no_of_sentences / no_of_words) - 15.8
    grade = round(index)
    # gives grade
    if grade < 1:
        print("Before Grade 1\n")
    elif grade > 16:
        print("Grade 16+\n")
    else:
        print(f"Grade {grade}\n")


def count_letters(text):
    count = 0
    for i in text:
        if i.isalpha():
            count += 1
    return count


def count_words(text):
    count = 0
    text_list = text.split(" ")
    for i in text_list:
        count += 1
    return count


def count_sentences(text):
    count = 0
    text_list = re.split('[.!?]', text)
    print(text_list)
    for i in text_list:
        count += 1
    return count - 1


main()