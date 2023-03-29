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
        print("Path error: there is no corresponding file in this path")
        answer = input("Do you want to use the default file?[y/n] ")
        if answer == "y":
            filePath = "/home/ulya/Documents/IGI_labs/Lab_2/Task_1/test.txt"
        else:
            return ""
    try:
        with open(filePath, "r") as file:
            return file.read()
    except:
        print("File error: can not open the file")
        return ""
