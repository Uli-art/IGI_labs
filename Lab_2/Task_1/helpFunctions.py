import re
import os.path
from constants import rxForWords, rxForNumbers


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
    wordList = []
    for word in wordMatches:
        if not (word in numbersMatches):
            wordList.append(word)
    return wordList


def readFromFile(filePath: str):
    if not os.path.exists(filePath):
        filePath = "/home/ulya/Documents/IGI_labs/Lab_2/Task_1/test.txt"
    with open(filePath, "r") as file:
        return file.read()
