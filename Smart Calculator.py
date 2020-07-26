# diccionario que va a guardar la variables
Dic_variables = {}

from collections import deque


def isOperand(n: str):
    operators = ['+', '-', '*', '/', '(', ')']
    return True if n not in operators else False


def isLeftParenthesis(n: str):
    return True if n == '(' else False


def isRightParenthesis(n: str):
    return True if n == ')' else False


def hasLessOrEqualPriority(n: str, operator: str):
    if n in ['+', '-'] and operator in ['+', '-']:
        return True
    elif n in ['*', '/'] and operator in ['*', '/']:
        return True
    elif n in ['+', '-'] and operator in ['*', '/']:
        return True
    else:
        return False


def makeup(infix: str):
    output = ''
    for n in infix.split():
        if n.startswith('('):
            output += '( ' + n[1:] + ' '
        elif n.endswith(')'):
            output += n[:len(n) - 1] + ' ) '
        else:
            output += n + ' '
    return output


def toPostfix(infix):
    stack = deque()
    postfix = ''
    for n in makeup(infix).split():
        if isOperand(n):
            postfix += n + ' '
        else:
            if isLeftParenthesis(n):
                stack.append(n)
            elif isRightParenthesis(n):
                operator = stack.pop()
                while not isLeftParenthesis(operator):
                    postfix += operator + ' '
                    operator = stack.pop()
            else:
                while (len(stack) != 0) and hasLessOrEqualPriority(n, stack[-1]):
                    postfix += stack.pop() + ' '
                stack.append(n)
    while len(stack) != 0:
        postfix += stack.pop() + ' '
    return postfix


def operation(postfix: str):
    stack = deque()
    for a in postfix.split():
        if a not in ['+', '-', '*', '/', '^']:
            value = int(Dic_variables[a]) if a in Dic_variables.keys() else int(a)
            stack.append(value)
            continue

        op1, op2 = stack.pop(), stack.pop()

        if a == '+':
            stack.append(op2 + op1)
        elif a == '-':
            stack.append(op2 - op1)
        elif a == '*':
            stack.append(op2 * op1)
        elif a == '/':
            stack.append(op2 / op1)
    return int(stack.pop())


def compute(input_: str):
    items = input_.split()
    result = int(Dic_variables[items[0]]) if items[0] in Dic_variables.keys() else int(items[0])
    for i in range(1, len(items), 2):
        operation = items[i]
        num = int(Dic_variables[items[i + 1]]) if items[i + 1] in Dic_variables.keys() else int(items[i + 1])
        if operation.startswith("+"):
            result += num
        elif operation.startswith("-"):
            if operation.count("-") % 2 == 1:
                result -= num
            else:
                result += num
        else:
            return "Invalid operation"
    return result


def variables(input_: str):
    nombre_variable = input_.replace(' ', '').split('=')[0]
    valor_variable = input_.replace(' ', '').split('=')[1]

    # comprobación de que los datos de entrada son correctos.
    if input_.count('=') > 1:
        print('Invalid assignment')
        return
    # comprobar que el nombre de la variabla solo tiene letras
    if not nombre_variable.isalpha():
        print('Invalid identifier')
        return
    # se comrurba si se quiere asignar de una variable a otra
    if valor_variable in Dic_variables.keys():
        valor_variable = Dic_variables[valor_variable]
    # comprobar que el valor a asociar es correcto
    if not valor_variable.isnumeric():
        print('Invalid assignment')
        return
    # gestión de la asignación al diccionari
    Dic_variables[nombre_variable] = valor_variable


while True:

    statement = input()
    if not statement:
        continue

    elif '=' in statement:
        variables(statement)

    elif statement in Dic_variables:
        print(Dic_variables[statement])

    elif statement == "/exit":
        break

    elif statement == "/help":
        print("The program calculates the sum of numbers")

    elif statement[0] == "/":
        print("Unknown command")

    elif statement.count('+') == 0 and statement.count('-') == 0 and statement.count('*') == 0 and statement.count(
            '/') == 0:
        print('Unknown variable')

    else:
        try:
            postfix = toPostfix(statement)
            print(operation(postfix))
        except:
            print('Invalid expression')

print("bye")