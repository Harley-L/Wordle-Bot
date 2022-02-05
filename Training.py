from Conditions import give_conditions


# Description: Open up the Wordle possible words and answers (alphabetically sorted) FOR TRAINING (Dict type)
# Return: list of all answers and list of all possible guesses - [dict[str, int], list of strings]
def read_training_data():
    all_words = dict()
    all_answers = list()

    f_all_words = open("TextFiles/wordle-words.txt")
    f_all_answers = open("TextFiles/wordle-answers-alphabetical.txt")

    for line in f_all_words:
        all_words[line[:-1]] = 0

    for line in f_all_answers:
        all_answers.append(line[:-1])

    return all_words, all_answers


# Description: Create a text file with all words and their associated score
# green_score: score associated with a green tile - int
# yellow_score: score associated with a yellow tile - int
def train(green_score, yellow_score):
    # Read in the training data
    all_words, all_answers = read_training_data()

    all_words_len = str(len(all_words))
    i = 0
    # for each possible word
    for test, test_val in all_words.items():
        i += 1
        print("\b" * 20 + str(i) + "/" + all_words_len, end="")
        # test against each possible solution
        for sol in all_answers:
            all_words[test] += score(test, sol, green_score, yellow_score)
    print("\b" * 20 + "Training Done")

    # Sort the dictionary by value
    sorted_aw = dict(sorted(all_words.items(), key=lambda item: item[1], reverse=True))

    # Write the dictionary to a text file
    f = open("TextFiles/all_words_values.txt", 'w')
    for word, val in sorted_aw.items():
        f.write(word + " " + str(val) + "\n")


# Description: scores how valuable a word is depending on the # of exact matches/letter in the word
# guess: a word - string
# solution: a word to compare against - string
# green_score: score associated with a green tile - int
# yellow_score: score associated with a yellow tile - int
# Return: the associated score - int
def score(guess, solution, green_score, yellow_score):
    score = 0
    str = give_conditions(guess, solution)
    for char in str:
        if char == 'G':
            score += green_score
        elif char == 'Y':
            score += yellow_score
    return score
