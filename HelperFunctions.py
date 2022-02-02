import random


# Description: changes the format of a word to list of chars
# word: a word - string
# Return: the word as a list of chars - list of chars
def split(word):
    return [char for char in word]


# Description: prints out the statistics of a bunch of guessed words
# wlist: list of guessed words and their associated attempt number - list of list [string, int]
def print_statistics(wlist, subset=-1):
    wsum = 0
    wmax = ["", 0]
    wmin = ["", 10000]
    for each in wlist:
        wsum += each[1]
        if wmin[1] > each[1]:
            wmin = each
        if wmax[1] < each[1]:
            wmax = each

    print("\nAVERAGE: " + str(wsum / 2315))
    print("MAX: " + wmax[0] + " " + str(wmax[1]))
    print("MIN: " + wmin[0] + " " + str(wmin[1]))

    if subset > 0:
        sub_list = random.sample(wlist, subset)
        for pair in sub_list:
            print(pair[0] + ": " + str(pair[1]), end='\t')
