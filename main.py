from Conditions import give_conditions, update_conditions, compare_exact, check_wrong_spot, letters_ok, check_multiples
from HelperFunctions import split, print_statistics
import string


# Description: Main function
def main():
    # Read in words
    all_answers, word_values = read_data()

    # Guess every possible word in the Wordle solution list
    list = []
    for i in range(2315):
        list.append(daily_wordle(all_answers, word_values, i))

    # Print out statistics
    print_statistics(list, 100)


# Description: One iteration of the daily WORDLE (from picking solution to guessing it correctly)
# all_answers: all possible WORDLE answers (2315 words long) - list of strings
# word_values: all possible WORDLE guesses (12972 words long) - list of strings
# num: Iteration number (Only for printing reasons) - int
# debug=False: option to show debug messages - bool
# debug_word='': option to pick a specific word to guess - string
# Return: solution and number of guesses it took - list [string, int]
def daily_wordle(all_answers, word_values, num, debug=False, debug_word=''):
    # Pick a solution
    if debug_word == '':
        solution = split(all_answers[num])
    else:
        solution = split(debug_word)

    # Printing
    if not debug:
        print("\b" * 40 + "Solution: " + "".join(solution) + " Itr: " + str(num+1) + "/" + "2315", end="")
    else:
        print("\n=======\n\nSolution: " + "".join(solution) + " Itr: " + str(num) + "/" + "2315", end="")

    # Initialize conditions and previous guess list
    guess_list = list()
    allowed_alpha = list(string.ascii_lowercase)
    correct_placement = ['', '', '', '', '']
    incorrect_placement = [[], [], [], [], []]
    no_multiples = set()
    guess_num = -1

    # Loop until the word is found.
    while solution != correct_placement:
        guess_num += 1  # increment guess number

        # Guess a word. Picks the first word from an already sorted list in terms of rarity
        guess_list.append(split(word_values[0]))
        if debug:
            print("\nGuess " + str(guess_num+1) + ": " + "".join(guess_list[guess_num]))

        # Determines the conditions from that word (Would normally be done in WORDLE) ALLOWED TO SEE THE SOLUTION
        condition = give_conditions(guess_list[guess_num], "".join(solution))
        if debug:
            print("Condition: " + "".join(condition))

        # Update the conditions from the new conditions
        correct_placement, incorrect_placement, allowed_alpha, no_multiples = update_conditions(condition,
                                                                                  guess_list[guess_num],
                                                                                  correct_placement,
                                                                                  incorrect_placement,
                                                                                  allowed_alpha,
                                                                                  no_multiples)

        # Update the word list from the updated conditions
        word_values = update_words(word_values, correct_placement, incorrect_placement, allowed_alpha, no_multiples)
        if debug:
            print("Remaining words: ", end='')
            print(len(word_values))
            print("Number of remaining words: " + str(word_values))

        # Exit in case it breaks
        if guess_num > 50:
            print("\n====================\n==== FAIL ====\n====================\n")
            exit(0)

    return ["".join(solution), guess_num+1]  # Return the solution and the number of guesses it took


# Description: Open up the Wordle possible words and answers (alphabetically sorted)
# Return: list of all answers and list of all possible guesses - [list of strings, list of strings]
def read_data():
    all_answers = list()
    word_values = list()
    f_all_answers = open("TextFiles/wordle-answers-alphabetical.txt")
    f_word_values = open("TextFiles/all_words_values.txt")

    for line in f_all_answers:
        all_answers.append(line[:-1])

    for line in f_word_values:
        arr = line.split()
        word_values.append(arr[0])

    return all_answers, word_values


# Description: Refine the list of words based on the conditions
# words: list of all possible words that can be guessed - list of strings
# correct_placement: correct word so far (based on green tiles) - list of chars
# incorrect_placement: in each spot, a list of chars that have incorrectly been placed there - list of list of chars
# allowed_alpha: list of allowed alphabet chars - list of chars
# no_multiples: list of letter and it's associated non-allowed occurrence number - list of tuple(char, int)
# debug=False: option to print out why a word was removed from the word list - bool
# Return: a new word list with all the words that satisfy the new conditions - list of strings
def update_words(words, correct_placement, incorrect_placement, allowed_alpha, no_multiples, debug=False):
    temp = list()
    for word in words:
        split_word = split(word)
        # Were there any green letters?
        if not compare_exact(split_word, correct_placement):
            if debug:
                print("REMOVE - Green: " + word)
            continue
        # Were there any yellow letters?
        if not check_wrong_spot(split_word, incorrect_placement):
            if debug:
                print("REMOVE - Yellow: " + word)
            continue
        # Grey letter list
        if not letters_ok(split_word, allowed_alpha):
            if debug:
                print("REMOVE - Letters: " + word)
            continue
        # Check if there are multiples of certain letters
        if not check_multiples(split_word, no_multiples):
            if debug:
                print("REMOVE - Double: " + word)
            continue
        temp.append(word)
    return temp


main()
