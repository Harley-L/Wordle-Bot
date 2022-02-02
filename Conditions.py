from HelperFunctions import split
from collections import Counter


# Description: Gives the WORDLE colours based on guess and solution
# guess: the guess - string
# solution: the solution to the wordle - string
# Return: list of O, G or Y inplace of the WORDLE colours - list of chars
def give_conditions(guess, solution):
    test_a = split(guess)
    sol_a = split(solution)

    # Direct Matches (Green)
    for i, char in enumerate(test_a):
        if char == sol_a[i]:
            test_a[i] = 'G'
            sol_a[i] = '&'

    # In word. (Yellow)
    for i, char in enumerate(test_a):
        if char in sol_a:
            test_a[i] = 'Y'
            sol_a[sol_a.index(char)] = '&'

    # Get rid of others (Grey)
    for i, char in enumerate(test_a):
        if char != 'G' and char != 'Y':
            test_a[i] = 'O'
    return test_a


# Description: Checks if two words are the same (ignoring '' chars of not found yet letters)
# word: the guess - list of chars
# correct_letters: correct word so far (based on green tiles) - list of chars
# Return: true if words are the same - bool
def compare_exact(word, correct_letters):
    for i, char in enumerate(correct_letters):
        if char != '':
            if word[i] != char:
                return False
    return True


# Description: Checks if a word contains the incorrect placement characters
# word: the guess - list of chars
# incorrect_placement: in each spot, a list of chars that have incorrectly been placed there - list of list of chars
# Return: the word's compatibility with the placement - bool
def check_wrong_spot(word, incorrect_placement):
    for i, spot in enumerate(incorrect_placement):
        for char in spot:
            if char not in word or word[i] == char:
                return False
    return True


# Description: Checks if a word contains any non-allowed chars
# word: the guess - list of chars
# alpha: list of allowed alphabet chars - list of chars
# Return: the word's compatibility with the placement - bool
def letters_ok(word, alpha):
    for char in word:
        if char not in alpha:
            return False
    return True


# Description: Checks if a word contains more than allowed multiple count for the solution
# word: the guess - list of chars
# no_multiples: list of letter and it's associated non-allowed occurrence number - list of tuple(char, int)
# Return: the word's compatibility with the placement - bool
def check_multiples(word, no_multiples):
    occ_dict = Counter(word)
    for char, num in occ_dict.items():
        if num > 1:
            for tuple in no_multiples:
                if char == tuple[0] and num >= tuple[1]:
                    return False
    return True


# Description: Updates the conditions based on the give_conditions function and the guess
# condition: condition list (O,G,Y) - list of chars
# guess: the guess - list of chars
# correct_placement: correct word so far (based on green tiles) - list of chars
# incorrect_placement: in each spot, a list of chars that have incorrectly been placed there - list of list of chars
# allowed_alpha: list of allowed alphabet chars - list of chars
# no_multiples: list of letter and it's associated non-allowed occurrence number - list of tuple(char, int)
# Return: the updated conditions - [list of chars, list of list of chars, list of chars, list of tuple(char, int)]
def update_conditions(condition, guess, correct_placement, incorrect_placement, allowed_alpha, no_multiples):
    occurrences = Counter(guess)  # Check how many of each character there is

    # loop through each character in the guess
    for i, char in enumerate(guess):
        # Were there any green letters?
        if condition[i] == 'G':
            correct_placement[i] = char

        # Were there any yellow letters?
        elif condition[i] == 'Y':
            incorrect_placement[i].append(char)

        # Update the grey letter list
        else:
            try:
                # IF there exists the same 2+ letters with one being special,
                # add to multiple occurrence list (special case)
                if occurrences[char] > 1:
                    no_multiples.add((char, occurrences[char]))
                    continue

                # If char in the word in another spot DON'T remove
                # If char in the word same spot DON'T remove
                flag = False
                for spot in incorrect_placement:
                    if char in spot:
                        flag = True
                if char not in correct_placement and not flag:
                    allowed_alpha.remove(char)

            # If already removed
            except ValueError:
                pass
    return correct_placement, incorrect_placement, allowed_alpha, no_multiples
