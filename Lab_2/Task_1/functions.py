import re
from constants import rxForSentences, rxForNameAbbreviations, rxForNonDeclarative, rxForWords, rxForNumbers
from helpFunctions import textLength, listOfWords


def countOfSentences(text: str):
    notASentence = re.findall(rxForNameAbbreviations, text)
    matches = re.findall(rxForSentences, text)
    return len(matches) - len(notASentence)


def nonDeclarativeSentences(text: str):
    matches = re.findall(rxForNonDeclarative, text)
    return len(matches)


def averageLengthOfSentence(text: str):
    countOfSent = countOfSentences(text)
    return float(textLength(text)) / countOfSent if countOfSent != 0 else 0


def averageLengthOfWord(text: str):
    return textLength(text) / len(listOfWords(text)) if len(listOfWords(text)) != 0 else 0


def topKRepeatedWordNGrams(text: str, k=10, n=4):
    dictionary = {}
    listOfWord = listOfWords(text)
    countOfWord = len(listOfWords(text))
    if countOfWord < n:
        print(f"n = {n} more than the number of words({countOfWord}) in the text")
    else:
        for i in range(0, countOfWord - n + 1):
            combination = ' '.join(listOfWord[i:i+n])
            if combination not in dictionary:
                dictionary[combination] = 1
            else:
                dictionary[combination] += 1
    dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    if len(dictionary) <= k:
        return dictionary
    return dictionary[0: k]


def topKRepeatedSymbolNGrams(text: str, k=10, n=4):
    dictionary = {}
    listOfWord = listOfWords(text)
    countOfWord = len(listOfWords(text))
    lenOfText = textLength(text)
    if lenOfText < n:
        print(f"n = {n} more than the number of symbols({lenOfText}) in the text")
    else:
        for i in range(0, countOfWord):
            if len(listOfWord[i]) < n:
                continue
            for j in range(0, len(listOfWord[i]) - n + 1):
                combination = listOfWord[i][j:j+4]
                if combination not in dictionary:
                    dictionary[combination] = 1
                else:
                    dictionary[combination] += 1
    dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    if len(dictionary) <= k:
        return dictionary
    return dictionary[0: k]

