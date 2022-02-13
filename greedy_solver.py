import random
from collections import Counter
import time

# # Adding frequency of letters for each word
# alphabet = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0,
#             'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0,
#             'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
# guess_list = []
# with open('full_word_list.txt') as book:
#     bk = book.readlines()
#     for line in bk:
#         word = line.strip()
#         guess_list.append(word)
#         for letter in word:
#             alphabet[letter] += 1
# print(alphabet)
# with open('full_word_list.txt', 'w') as book:
#     for word in guess_list:
#         freq = 0
#         for letter in word:
#             freq += alphabet[letter]
#         book.write(f"{word},{freq}\n")


# 4980 words
train_list, test_list = {}, []
with open('full_word_list.txt') as f:
    paragraph = f.readlines()
    for line in paragraph:
        word = line.split(',')[0]
        number = int(line.split(',')[1]) * len(Counter(word))
        train_list[word] = number
with open('wordle_list.txt') as f:
    paragraph = f.readlines()
    for line in paragraph:
        word = line.split(',')[0]
        test_list.append(word)


# print(word_list)


def validate(guess, answer, train, verbose=False):
    position = []
    ans = {}
    for i in range(5):
        if guess[i] == answer[i]:
            position += 'G'
        elif guess[i] in answer:
            position += 'Y'
        else:
            position += 'B'

    for word, num in train.items():
        in_list = True
        for i in range(5):
            if position[i] == 'G' and word[i] != guess[i]:
                in_list = False
            elif position[i] == 'Y' and (guess[i] not in word or word[i] == guess[i]):
                in_list = False
            elif position[i] == 'B' and guess[i] in word:
                in_list = False
        if in_list:
            ans[word] = num

    if verbose:
        print(f"ANSWER: {answer} | GUESS: {guess} {position} {len(ans)}")

    return ans


def play(times=1, verbose=False):
    total, winnable = 0, 0
    test = test_list
    random.shuffle(test)
    for i in range(times):
        train = train_list
        answer = test[i]

        freq = 0
        while True:
            freq += 1
            guess = (max(train, key=train.get))
            train = validate(guess, answer, train, verbose=True)
            if guess == answer:
                if verbose:
                    print(answer, freq)
                if freq <= 6:
                    winnable += 1
                total += freq
                break
    print(f"Average Number of Attempts: {total / times}\nWinnable in Wordle: {winnable}")


start = time.process_time()
play(times=2315, verbose=True)
end = time.process_time()
print(f'Time Taken: {round(end - start, 2)} Seconds')
