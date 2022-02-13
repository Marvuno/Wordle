import random
from collections import Counter
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

entropy_list, train_list, test_list, frequency_chart, pattern_chart = {}, {}, [], {'1': 0, '2': 0, '3': 0, '4': 0,
                                                                                   '5': 0, '6': 0, '7': 0, '8': 0}, {}
# 12972 words
with open('full_word_list.txt') as f:
    paragraph = f.readlines()
    for line in paragraph:
        word = line.split(',')[0]
        number = int(line.split(',')[1]) * len(Counter(word))
        train_list[word] = number
# 2315 words for wordle_list
# 4980 words for custom_word_list
with open('wordle_list.txt') as f:
    paragraph = f.readlines()
    for line in paragraph:
        word = line.split(',')[0]
        test_list.append(word)
# list of first words and respective entropy
with open('entropy.txt') as f:
    paragraph = f.readlines()
    for line in paragraph:
        word = line.split(',')[0]
        first_word_entropy = float(line.split(',')[1])
        entropy_list[word] = first_word_entropy
    entropy_list = dict(sorted(entropy_list.items(), key=lambda item: item[1], reverse=True))
# best word after first word
with open('second_guess.txt') as f:
    paragraph = f.readlines()
    for line in paragraph:
        pattern = line.split(',')[0]
        word = line.split(',')[1].strip()
        pattern_chart[pattern] = word


# information theory
def algorithm(train):
    validation = list(train_list)
    max_entropy = 0

    # 50/50 in choosing answer between 2 words anyways
    if len(train) == 1:
        guess = train[0]
        return guess
    elif len(train) == 2:
        validation = train

    words_entropy, words_frequency = {}, {}
    for validate_words in validation:
        entropy, combination = 0, {}
        for train_words in train:
            pattern = ""
            for i in range(5):
                if validate_words[i] == train_words[i]:
                    pattern += "G"
                elif validate_words[i] in train_words:
                    pattern += "Y"
                elif validate_words[i] not in train_words:
                    pattern += "B"
            try:
                combination[pattern].append(train_words)
            except KeyError:
                combination[pattern] = []
                combination[pattern].append(train_words)

        for keys in combination:
            probability = len(combination[keys]) / len(train)
            entropy += probability * np.log2(1 / probability)
            max_entropy = max(max_entropy, entropy)
            words_entropy[validate_words] = entropy

    # Rank by entropy first, then by letter frequency
    for words, entropy in words_entropy.items():
        if entropy == max_entropy:
            words_frequency[words] = train_list[words]
    guess = (max(words_frequency, key=words_frequency.get))

    return guess


def validate(guess, answer, train):
    position = ""
    remaining = []
    for i in range(5):
        if guess[i] == answer[i]:
            position += 'G'
        elif guess[i] in answer:
            position += 'Y'
        else:
            position += 'B'

    for word in train:
        in_list = True
        for i in range(5):
            if position[i] == 'G' and word[i] != guess[i]:
                in_list = False
            elif position[i] == 'Y' and (guess[i] not in word or word[i] == guess[i]):
                in_list = False
            elif position[i] == 'B' and guess[i] in word:
                in_list = False
        if in_list and position != "GGGGG":
            remaining.append(word)
    print(len(remaining), remaining)
    return remaining, position


def play(times=1):
    total, winnable = 0, 0
    test = test_list
    random.shuffle(test)
    for i in range(times):
        answer = test[i]
        # in case original word list doesn't contain custom words
        if answer not in train_list:
            continue

        # best first word is TARES
        print(f"{i + 1} Answer: {answer}")
        print("TARES", end=" ")
        train, position = validate(guess="TARES", answer=answer, train=train_list)
        freq = 1
        while True:
            freq += 1

            # update second_guess.txt if needed
            try:
                if freq == 2:
                    guess = pattern_chart[position]
                else:
                    guess = algorithm(train)
            except KeyError:
                guess = algorithm(train)
                pattern_chart[position] = guess
                with open('second_guess.txt', 'a') as f:
                    f.write(f"{position},{guess}\n")
            print(guess, end=" ")

            train, position = validate(guess, answer, train)

            if guess == answer:
                frequency_chart[str(freq)] += 1
                total += freq
                print(f"Number of Guesses: {freq}\n")
                break

    print(f"Average Number of Attempts: {total / times}")
    print(frequency_chart)

    # bar chart
    plt.figure(figsize=(8, 8))
    plt.xlabel("Number of Guesses")
    plt.ylabel("Frequency")
    sns.set_theme(style="ticks")
    ax = sns.barplot(x=list(frequency_chart.keys()), y=list(frequency_chart.values()))
    ax.bar_label(ax.containers[0])
    plt.show()


def manual_play():
    guess = "TARES"
    print(guess)
    train = list(train_list)
    while True:
        remaining = []
        response = input("What is the combination? (G for green, Y for yellow, B for grey): ").upper()

        if response == "GGGGG":
            print("You Win!")
            break

        for word in train:
            in_list = True
            for i in range(5):
                if response[i] == 'G' and word[i] != guess[i]:
                    in_list = False
                elif response[i] == 'Y' and (guess[i] not in word or word[i] == guess[i]):
                    in_list = False
                elif response[i] == 'B' and guess[i] in word:
                    in_list = False
            if in_list:
                remaining.append(word)

        train = remaining
        guess = algorithm(remaining)
        print(guess)

"""
Custom Word List Stats
Average Number of Attempts: 4.048795180722892
{'1': 0, '2': 18, '3': 910, '4': 2963, '5': 989, '6': 93, '7': 6, '8': 0}

Wordle List Stats
Average Number of Attempts: 4.019006479481641
{'1': 0, '2': 6, '3': 422, '4': 1434, '5': 429, '6': 23, '7': 1, '8': 0}
JOLLY - 7 Attempts
"""
start = time.process_time()
play(times=2315)
end = time.process_time()
print(f'Time Taken: {round(end - start, 2)} Seconds')
