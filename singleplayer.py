from HelperFunctions import split
import random
from Conditions import update_conditions, compare_exact, check_wrong_spot, letters_ok, check_multiples
import string


# Description: Open up the Wordle possible words and answers and pick one randomly
# Returns: a random solution and a list of all of the allowed words - string, list of strings
def choose_random_word():
    # Read in words
    all_answers, allowed_words = read_data()
    return split(random.sample(all_answers, 1)[0].upper()), allowed_words


# Description: Open up the Wordle possible words and answers (alphabetically sorted)
# Return: list of all answers - [list of strings]
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


# Description: Find and guess the best next word for the Wordle by sorting through the past conditions
def machine_guess(grid):
    if not grid.done:
        allowed_words = grid.allowed_words
        allowed_alpha = list(string.ascii_lowercase)
        correct_placement = ['', '', '', '', '']
        incorrect_placement = [[], [], [], [], []]
        no_multiples = set()
        for i, word in enumerate(grid.past_words):
            # Update the conditions from the new conditions
            correct_placement, incorrect_placement, allowed_alpha, no_multiples = update_conditions(grid.past_conditions[i],
                                                                                                    split("".join(word).lower()),
                                                                                                    correct_placement,
                                                                                                    incorrect_placement,
                                                                                                    allowed_alpha,
                                                                                                    no_multiples)

        # Update the word list from the updated conditions
        good_guesses = update_words(allowed_words, correct_placement, incorrect_placement, allowed_alpha, no_multiples)

        grid.helper_guess(split(good_guesses[0].upper()))


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
