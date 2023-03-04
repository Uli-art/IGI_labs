from helloWord import printHelloWorld
from calculations import calculations
from evenNumbers import evenNumbers
from random import sample


def main():
    # task 1
    printHelloWorld()

    # task 2
    firstNum = 4
    secondNum = 5
    print(f'Calculations with {firstNum} and {secondNum}:\n',
          calculations(firstNum, secondNum, "add"),
          calculations(firstNum, secondNum, "sub"),
          calculations(firstNum, secondNum, "mult"),
          calculations(firstNum, secondNum, "div"))

    # task 3
    listOfNumbers = [number for number in sample(range(100), 10)]
    print('List of numbers:', listOfNumbers)
    print('List of even numbers:', evenNumbers(listOfNumbers))


if __name__ == '__main__':
    main()
