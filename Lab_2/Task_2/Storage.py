import os
import re


class Storage:
    storage: dict[str, set]
    currentUser: str
    currentContainer: set
    listOfCommands = ["add", "remove", "find", "load", "save", "switch", "grep", "stop", "help"]

    def __init__(self):
        self.storage = dict[str, set]()
        self.currentUser = ""
        self.currentContainer = set()

    def initialization(self):
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
            try:
                with open(filePath, "r") as file:
                    self.add(file.read().replace('\n', '').split(" "))
            except:
                print("File error: can not open the file")

    def save(self):
        filePath = input("Enter file path: ")
        if not os.path.exists(filePath):
            print("Path error: there is no corresponding file in this path")
        else:
            try:
                with open(filePath, "w") as file:
                    file.write(" ".join(self.currentContainer))
                    file.close()
            except:
                print("File error: can not open the file")

    def switch(self):
        answer = input("Do you want to save changes in the container?[y/n] ")
        if answer == "y":
            self.storage[self.currentUser] = self.currentContainer
        answer = input("Do you want to save container to file?[y/n]")
        if answer == "y":
            self.save()
        self.initialization()

    def commandControl(self):
        self.initialization()
        inputLine = input("> ")

        while inputLine != "stop":
            match = re.findall(r'\b\w+\b', inputLine)

            if len(match) == 0:
                print("Input is empty")
                inputLine = input("> ")
                continue

            command = match[0]
            arguments = match[1:len(match)]

            match command:
                case "add":
                    if len(arguments) == 0:
                        print(f"Too few arguments for this command. Expected: min 1, given: {len(arguments)}")
                    else:
                        self.add(arguments)
                case "remove":
                    if len(arguments) == 0:
                        print(f"Too few arguments for this command. Expected: 1, given: {len(arguments)}")
                    elif len(arguments) >= 2:
                        print(f"Too many arguments for this command. Expected: 1, given: {len(arguments)}")
                    else:
                        self.remove(arguments[0])
                case "find":
                    if len(arguments) == 0:
                        print(f"Too few arguments for this command. Expected: min 1, given: {len(arguments)}")
                    else:
                        self.find(arguments)
                case "list":
                    if not len(arguments) == 0:
                        print(f"Too many arguments for this command. Expected: 0, given: {len(arguments)}")
                    else:
                        self.list()
                case "grep":
                    if len(inputLine.split(" ")) == 1:
                        print(f"Too few arguments for this command. Expected: 1, given: {len(inputLine.split()) - 1}")
                    elif len(inputLine.split(" ")) >= 3:
                        print(f"Too many arguments for this command. Expected: 1, given: {len(inputLine.split()) - 1}")
                    else:
                        self.grep(inputLine)
                case "load":
                    if not len(arguments) == 0:
                        print(f"Too many arguments for this command. Expected: 0, given: {len(arguments)}")
                    else:
                        self.load()
                case "save":
                    if not len(arguments) == 0:
                        print(f"Too many arguments for this command. Expected: 0, given: {len(arguments)}")
                    else:
                        self.save()
                case "switch":
                    if not len(arguments) == 0:
                        print(f"Too many arguments for this command. Expected: 0, given: {len(arguments)}")
                    else:
                        self.switch()
                case "help":
                    if not len(arguments) == 0:
                        print(f"Too many arguments for this command. Expected: 0, given: {len(arguments)}")
                    else:
                        print(self.listOfCommands)
                case _:
                    print("No such command")

            inputLine = input("> ")
