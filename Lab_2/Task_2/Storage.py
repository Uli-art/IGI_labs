import os
import re


class Storage:
    storage: dict[str, set]
    currentUser: str
    currentContainer: set
    listOfCommands = ["add", "remove", "find", "load", "save", "switch", "grep", "stop"]

    def __init__(self):
        self.storage = dict[str, set]()
        self.currentUser = ""
        self.currentContainer = set()

    def initialisation(self):
        self.currentUser = input("Enter username:")
        answer = input("Do you want to load container from file?[y/n]")
        if answer == "y":
            self.storage[self.currentUser] = set()
            self.currentContainer = set()
            self.load()
        else:
            if self.currentUser in self.storage.keys():
                self.currentContainer = self.storage[self.currentUser]
            else:
                self.storage[self.currentUser] = set()
                self.currentContainer = set()

    def add(self, arguments):
        self.currentContainer.update(arguments)

    def remove(self, argument):
        try:
            self.currentContainer.remove(argument)
        except:
            print("No such element in container")

    def find(self, arguments):
        result = []
        for key in arguments:
            if key in self.currentContainer:
                result.append(key)
        if len(result) == 0:
            print("No such elements")
        else:
            print(result)

    def list(self):
        print(self.currentContainer)

    def grep(self, inputLine):
        arguments = re.findall(r'\'.+\'', inputLine)
        regex = "".join(arguments).replace("\'", "")
        if regex == "":
            print("Regex cannot be found: regex must be in quotes('regex')")
        else:
            result = []
            for key in self.currentContainer:
                match = re.fullmatch(regex, str(key))
                if match is not None:
                    result.append(match.group())
            if len(result) == 0:
                print("No such elements")
            else:
                print(result)

    def load(self):
        filePath = input("Enter file path: ")
        if not os.path.exists(filePath):
            print("Path error: there is no corresponding file in this path")
        else:
            with open(filePath, "r") as file:
                self.add(file.read().split(" "))

    def save(self):
        filePath = input("Enter file path: ")
        if not os.path.exists(filePath):
            print("Path error: there is no corresponding file in this path")
        else:
            with open(filePath, "w") as file:
                file.write(" ".join(self.currentContainer))
                file.close()