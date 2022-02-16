import main
import string


def manual_helper():
    all_answers, word_values = main.read_data()

    # Initialize conditions and previous guess list
    guess_list = list()
    allowed_alpha = list(string.ascii_lowercase)
    correct_placement = ['', '', '', '', '']
    incorrect_placement = [[], [], [], [], []]
    no_multiples = set()
    guess_num = 1
    guess = "AAAAA"
    exit_flag = "Y"

    while exit_flag != "N" and exit_flag != "n":
        guess = input(f"{guess_num} Guess: ").lower()
        condition = main.split(input(f"{guess_num} Color: ").upper())
        guess_num += 1
        # Update the conditions from the new conditions
        correct_placement, incorrect_placement, allowed_alpha, no_multiples = main.update_conditions(condition,
                                                                                                guess,
                                                                                                correct_placement,
                                                                                                incorrect_placement,
                                                                                                allowed_alpha,
                                                                                                no_multiples)
        # Update the word list from the updated conditions
        word_values = main.update_words(word_values, correct_placement, incorrect_placement, allowed_alpha, no_multiples)
        print(f"Remaining words {len(word_values)}: " + str(word_values))
        exit_flag = input("Another Guess(Y/N)? ")


if __name__ == "__main__":
    manual_helper()
