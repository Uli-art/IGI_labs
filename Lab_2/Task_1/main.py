from functions import countOfSentences, nonDeclarativeSentences, averageLengthOfSentence, averageLengthOfWord, topKRepeatedNGrams


if __name__ == '__main__':
    text = input("Enter text to analyze: ")
    print(f"{countOfSentences(text)} {nonDeclarativeSentences(text)} {averageLengthOfSentence(text)} {averageLengthOfWord(text)} {topKRepeatedNGrams(text)}")
