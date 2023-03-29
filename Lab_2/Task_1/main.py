from functions import countOfSentences, nonDeclarativeSentences, averageLengthOfSentence, averageLengthOfWord, \
    topKRepeatedWordNGrams, topKRepeatedSymbolNGrams
from helpFunctions import readFromFile


if __name__ == '__main__':
    answer = "y"
    while answer == "y":
        readTextFromFile = input("Do you want to read text from file?[y/n] ")

        if readTextFromFile == "y":
            filePath = str(input("Enter file path: "))
            text = readFromFile(filePath)
        else:
            text = input("Enter text to analyze: ")

        enterNgrams = input("Do you want to enter n and k for n-grams?[y/n] ")

        if enterNgrams == "y":
            try:
                k = int(input("k = "))
                n = int(input("n = "))
            except:
                print("Input error. Use default values (k = 10, n = 4)")
                k = 10
                n = 4

        print(f"\nStatistics:\n"
              f"amount of sentences: {countOfSentences(text)}\n"
              f"amount of non-declarative sentences: {nonDeclarativeSentences(text)}\n"
              f"average length of the sentence(in characters): {averageLengthOfSentence(text)}\n"
              f"average length of the word: {averageLengthOfWord(text)}\n"
              f"N-grams:\n")
        if enterNgrams == "y":
            print(f"word n-grams: {topKRepeatedWordNGrams(text, k, n)}\n"
                  f"symbol n-grams: {topKRepeatedSymbolNGrams(text, k, n)}\n")
        else:
            print(f"word n-grams: {topKRepeatedWordNGrams(text)}\n"
                  f"symbol n-grams: {topKRepeatedSymbolNGrams(text)}\n")
        answer = input("Do you want to continue?[y/n]")
