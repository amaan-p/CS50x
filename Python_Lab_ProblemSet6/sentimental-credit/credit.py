from cs50 import get_string

global card_number


def main():
    # Ask for user for card
    card_number = get_string("Number: ")
    # ask for validating card
    if validate_card(card_number):
        # Identifies the company of the card
        company_card(card_number)
    else:
        print("INVALID\n")


def validate_card(card_number):
    sum_of_number_by_2 = 0
    temp_1 = int(card_number)
    # looping through second last digits to start alternately
    while temp_1 != 0:
        temp_1 = temp_1 // 10
        # multiplying it by 2
        rem = (temp_1 % 10)*2
        # performing addition on individual digits
        while rem != 0:
            new_rem = rem % 10
            sum_of_number_by_2 = sum_of_number_by_2 + new_rem
            rem = rem // 10
        temp_1 = temp_1 // 10

    alt_sum_of_number_by_2 = 0
    temp = int(card_number)
    # looping through last digits to start alternately
    while temp != 0:
        rem = temp % 10
        # adding sums of those digits
        alt_sum_of_number_by_2 = alt_sum_of_number_by_2+rem
        temp = temp // 10
        temp = temp // 10
    # addition of both sums
    final_sum = sum_of_number_by_2 + alt_sum_of_number_by_2
    if final_sum % 10 == 0:
        return True
    else:
        return False


def company_card(card_number):
    # checks if card is american express
    if card_number[0] == "3" or card_number[1] == "4" or card_number[1] == "7" and len(card_number) == 15:
        print("AMEX")
    # checks if card is mastercard
    elif card_number[0] == "5" and card_number[1] == "1" or card_number[1] == "2" or card_number[1] == "3" or card_number[1] == "4" or card_number[1] == "5" and len(card_number) == 16:
        print("MASTERCARD")
    # checks if card is visa
    elif card_number[0] == "4" and len(card_number) == 13 or len(card_number) == 16:
        print("VISA")
    else:
        print("INVALID\n")


# main function
main()
