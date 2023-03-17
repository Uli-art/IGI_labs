from constants import Operations as Op


def calculations(firstOperand, secondOperand, operation):
    if(isinstance(firstOperand, int | float)) and (isinstance(secondOperand, int | float)):
        match operation:
            case Op.add.value:
                return firstOperand + secondOperand
            case Op.sub.value:
                return firstOperand - secondOperand
            case Op.mult.value:
                return firstOperand * secondOperand
            case Op.div.value:
                if secondOperand:
                    return firstOperand / secondOperand
            case _:
                print("Unknown operator")
    else:
        print("Incorrect input")
