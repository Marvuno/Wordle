import random
from collections import Counter

# # Adding frequency of letters for each word
# alphabet = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0,
#             'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0,
#             'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
# guess_list = []
# with open('guess_list.txt') as book:
#     bk = book.readlines()
#     for line in bk:
#         word = line.strip()
#         guess_list.append(word)
#         for letter in word:
#             alphabet[letter] += 1
# print(alphabet)
# with open('guess_list.txt', 'w') as book:
#     for word in guess_list:
#         freq = 0
#         for letter in word:
#             freq += alphabet[letter]
#         book.write(f"{word},{freq}\n")


# 4980 words
word_list = {}
with open('word_list.txt') as f:
    paragraph = f.readlines()
    for line in paragraph:
        word = line.split(',')[0]
        number = int(line.split(',')[1]) * len(Counter(word))
        word_list[word] = number
# print(word_list)


def validate(guess, answer, possible_ans, verbose=False):
    position = []
    ans = {}
    for i in range(5):
        if guess[i] == answer[i]:
            position += 'G'
        elif guess[i] in answer:
            position += 'Y'
        else:
            position += 'B'

    for word, num in possible_ans.items():
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
        print(f"ANSWER: {answer}\nGUESS: {guess} {position}\n{ans}")

    return ans


def play(times=1, verbose=False):
    total, winnable = 0, 0
    played_word = []
    for _ in range(times):
        possible_ans = word_list
        answer = random.choice(list(word_list))
        while answer in played_word:
            answer = random.choice(list(word_list))
        played_word.append(answer)

        freq = 0
        while True:
            freq += 1
            guess = (max(possible_ans, key=possible_ans.get))
            possible_ans = validate(guess, answer, possible_ans, verbose=False)
            if guess == answer:
                if verbose:
                    print(answer, freq)
                if freq <= 6:
                    winnable += 1
                total += freq
                break
    print(f"Average Number of Attempts: {total/times}\nWinnable in Wordle: {winnable}")


play(times=1000, verbose=True)