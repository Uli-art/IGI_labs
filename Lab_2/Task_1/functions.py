import re
from constants import rxForSentences, rxForNameAbbreviations, rxForNonDeclarative, rxForWords, rxForNumbers


def countOfSentences(text: str):
    notASentence = re.findall(rxForNameAbbreviations, text)
    matches = re.findall(rxForSentences, text)
    print(matches)
    return len(matches) - len(notASentence)


def nonDeclarativeSentences(text: str):
    matches = re.findall(rxForNonDeclarative, text)
    return len(matches)


def textLength(text: str):
    wordMatches = re.findall(rxForWords, text)
    numbersMatches = re.findall(rxForNumbers, text)
    textLen = 0
    for word in wordMatches:
        if not (word in numbersMatches):
            textLen = textLen + len(word)
    return textLen


def listOfWords(text: str):
    wordMatches = re.findall(rxForWords, text)
    numbersMatches = re.findall(rxForNumbers, text)
    textLen = []
    for word in wordMatches:
        if not (word in numbersMatches):
            textLen.append(word)
    return textLen


def averageLengthOfSentence(text: str):
    countOfSent = countOfSentences(text)
    return textLength(text) / countOfSent if countOfSent != 0 else 0


def averageLengthOfWord(text: str):
    return textLength(text) / len(listOfWords(text)) if len(listOfWords(text)) != 0 else 0


def topKRepeatedNGrams(text: str, k=10, n=4):
    dictionary = {}
    listOfWord = listOfWords(text)
    countOfWord = len(listOfWords(text))
    if countOfWord < n:
        print("")
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
