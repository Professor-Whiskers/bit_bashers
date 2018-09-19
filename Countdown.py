from random import *
from itertools import permutations, product


def brackets(n):
    return ')' * n


def calc(a1, operator, a2):  # A basic function for calculating with
    if operator == ' + ':
        return a1 + a2
    if operator == ' - ':
        return a1 - a2
    if operator == ' / ':
        if a2 == 0:
            return 10000000
        else:
            return a1 / float(a2)
    if operator == ' * ':
        return a1 * a2


def add_solution(result):
    if len(solutions) < limit and result not in solutions:
        solutions.append(result)
        if len(solutions) == limit:
            print_solutions()


def solve():
    
    bracket = 0
    
    global limit
    # limit = int(raw_input("How many answers do you want? \n"))  # asks the user how many answers they want
    limit = 10
    if target in number:
        add_solution(str(target) + ' = ' + str(target))
        
    for num_perm in set(permutations(number, 2)):
        for o1 in op:
            result = calc(num_perm[0], o1, num_perm[1])
            if result == target:
                solution_str = ''.join(str(num_perm[0]) + o1 + str(num_perm[1]) + ' = ' + str(result))  
                add_solution(solution_str)

    for num_perm in set(permutations(number, 3)):
        for op_perm in (p for p in product(op, repeat=2)):
            result = calc(num_perm[0], op_perm[0], calc(num_perm[1], op_perm[1], num_perm[2]))
            
            if result == target:
                if op_perm[1] == ' - ' or op_perm[1] == ' + ' and op_perm[0] == ' * ' or op_perm[0] == ' / ':
                    solution_str = ''.join(str(num_perm[0]) + op_perm[0] + '(' + str(num_perm[1]) + op_perm[1]
                                           + str(num_perm[2]) + ')' + ' = ' + str(result))
                else:
                    solution_str = ''.join(str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + op_perm[1]
                                           + str(num_perm[2]) + ' = ' + str(result))
                add_solution(solution_str)

            result = calc(calc(num_perm[0], op_perm[0], num_perm[1]), op_perm[1], num_perm[2])

            if result == target:
                if op_perm[0] == ' - ' or op_perm[0] == ' + ' and op_perm[1] == ' * ' or op_perm[1] == ' / ':
                    solution_str = ''.join('(' + str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + ')' + op_perm[1]
                                           + str(num_perm[2]) + ' = ' + str(result))
                else:
                    solution_str = ''.join(str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + op_perm[1]
                                           + str(num_perm[2]) + ' = ' + str(result))
                add_solution(solution_str)

    for num_perm in set(permutations(number, 4)):
        for op_perm in (p for p in product(op, repeat=3)):
            
            result = calc(num_perm[0], op_perm[0], calc(num_perm[1], op_perm[1],
                                                        calc(num_perm[2], op_perm[2], num_perm[3])))
            if result == target:
                solution_str = []
                if (op_perm[1] == ' - ' and op_perm[0] != ' + ') or (op_perm[1] == ' + ' and op_perm[0] != ' + ') \
                        or op_perm[1] == ' / ':
                    solution_str.append(str(num_perm[0]) + op_perm[0] + '(' + str(num_perm[1]) + op_perm[1])
                    bracket = bracket + 1
                else:
                    solution_str.append(str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + op_perm[1])
                if (op_perm[2] == ' - ' and op_perm[1] != ' + ') or (op_perm[2] == ' + ' and op_perm[1] != ' + ')\
                        or op_perm[2] == ' / ':
                    solution_str.append(
                        '(' + str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + brackets(bracket + 1) + ' = ' + str(
                            result))
                else:
                    solution_str.append(
                        str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + brackets(bracket) + ' = ' + str(result))
                add_solution(''.join(solution_str))
            bracket = 0

            result = calc(calc(num_perm[0], op_perm[0], num_perm[1]), op_perm[1],
                          calc(num_perm[2], op_perm[2], num_perm[3]))
            if result == target:
                solution_str = []
                if (op_perm[1] == ' - ' and op_perm[0] != ' + ') or (op_perm[1] == ' + '
                                                                     and op_perm[0] != ' + ') or op_perm[1] == ' / ':
                    solution_str.append(str(num_perm[0]) + op_perm[0] + '(' + str(num_perm[1]) + op_perm[1])
                    bracket = bracket + 1
                else:
                    solution_str.append(str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + op_perm[1])
                if (op_perm[2] == ' - ' and op_perm[1] != ' + ') or (op_perm[2] == ' + ' and op_perm[1] != ' + ')\
                        or op_perm[2] == ' / ':
                    solution_str.append('(' + str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + brackets(bracket + 1))
                else:
                    solution_str.append(str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + brackets(bracket))
                solution_str.append(' = ' + str(result))
                add_solution(''.join(solution_str))

            bracket = 0

            result = calc(num_perm[0], op_perm[0],
                          calc(calc(num_perm[1], op_perm[1], num_perm[2]), op_perm[2], num_perm[3]))
            if result == target:
                solution_str = []
                if (op_perm[1] == ' - ' and op_perm[0] != ' + ') or (op_perm[1] == ' + ' and op_perm[0] != ' + ')\
                        or op_perm[1] == ' / ':
                    solution_str.append(str(num_perm[0]) + op_perm[0] + '(' + str(num_perm[1]) + op_perm[1])
                    bracket = bracket + 1
                else:
                    solution_str.append(str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + op_perm[1])
                if (op_perm[2] == ' - ' and op_perm[1] != ' + ') or (op_perm[2] == ' + '
                                                                     and op_perm[1] != ' + ') or op_perm[2] == ' / ':
                    solution_str.append('(' + str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + brackets(bracket + 1))
                else:
                    solution_str.append(str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + brackets(bracket))
                solution_str.append(' = ' + str(result))
                add_solution(''.join(solution_str))
    for num_perm in set(permutations(number, 5)):
        for op_perm in (p for p in product(op, repeat=4)):
            
            result = calc(num_perm[0], op_perm[0],
                          calc(num_perm[1], op_perm[1],
                               calc(num_perm[2], op_perm[2],
                                    calc(num_perm[3], op_perm[3], num_perm[4]))))
            if result == target:
                solution_str = []

                if (op_perm[1] == ' - ' and op_perm[0] != ' + ') or (op_perm[1] == ' + ' and op_perm[0] != ' + ')\
                        or op_perm[1] == ' / ':
                    solution_str.append(str(num_perm[0]) + op_perm[0] + '(' + str(num_perm[1]) + op_perm[1])
                    bracket = bracket + 1
                else:
                    solution_str.append(str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + op_perm[1])

                if (op_perm[2] == ' - ' and op_perm[1] != ' + ') or (
                        op_perm[2] == ' + ' and op_perm[1] == ' * ' or op_perm[1] == ' / ' or op_perm[1] == ' - ')\
                        or op_perm[2] == ' / ':
                    solution_str.append('(' + str(num_perm[2]) + op_perm[2])
                    bracket = bracket + 1
                else:
                    solution_str.append(str(num_perm[2]) + op_perm[2])

                if (op_perm[3] == ' - ' and op_perm[2] == ' * ' or op_perm[2] == ' / ' or op_perm[2] == ' - ') or (
                        op_perm[3] == ' + ' and op_perm[2] == ' * ' or op_perm[2] == ' / ' or op_perm[2] == ' - ')\
                        or op_perm[3] == ' / ':

                    solution_str.append('(' + str(num_perm[3]) + op_perm[3] + str(num_perm[4]) + brackets(
                        bracket + 1) + ' = ' + str(result))
                else:
                    solution_str.append(
                        str(num_perm[3]) + op_perm[3] + str(num_perm[4]) + brackets(bracket) + ' = ' + str(result))

                add_solution(''.join(solution_str))

            bracket = 0
            
            result = calc(calc(calc(num_perm[0], op_perm[0], num_perm[1]), op_perm[1],
                               calc(num_perm[2], op_perm[2], num_perm[3])), op_perm[3], num_perm[4])

            if result == target:
                solution_str = []

                if op_perm[3] == ' * ' and (op_perm[1] != ' * ' or op_perm[1] != ' / '):
                    solution_str.append('(')
                    bracket = 1

                if ((op_perm[0] == ' - ' or op_perm[0] == ' + ') and op_perm[1] != ' + ' and op_perm[1] != ' - ')\
                        or op_perm[1] == ' / ':
                    solution_str.append('(' + str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + ')' + op_perm[1])
                else:
                    solution_str.append(str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + op_perm[1])

                if (op_perm[2] == ' - ' and op_perm[1] != ' + ') or (op_perm[2] == ' + ' and op_perm[1] != ' + ')\
                        or op_perm[2] == ' / ':
                    solution_str.append(
                        '(' + str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + ')' + brackets(bracket) +
                        op_perm[3] + str(num_perm[4]) + ' = ' + str(result))
                else:
                    solution_str.append(
                        str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + brackets(bracket) + op_perm[3] + str(
                            num_perm[4]) + ' = ' + str(result))

                add_solution(''.join(solution_str))
            bracket = 0
            
            result = calc(calc(num_perm[0], op_perm[0], num_perm[1]), op_perm[1],
                          calc(num_perm[2], op_perm[2], calc(num_perm[3], op_perm[3], num_perm[4])))

            if result == target:

                solution_str = []

                if ((op_perm[0] == ' - ' or op_perm[0] == ' + ') and op_perm[1] != ' + ' and op_perm[1] != ' - ')\
                        or op_perm[1] == ' / ':
                    solution_str.append('(' + str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + ')' + op_perm[1])
                else:
                    solution_str.append(str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + op_perm[1])

                if (op_perm[2] == ' - ' and op_perm[1] != ' + ') or (op_perm[2] == ' + ' and op_perm[1] != ' + ')\
                        or op_perm[2] == ' / ':
                    solution_str.append('(' + str(num_perm[2]) + op_perm[2])
                    bracket = 1
                else:
                    solution_str.append(str(num_perm[2]) + op_perm[2])

                if (op_perm[3] == ' + ' and op_perm[2] == ' * ' or op_perm[2] == ' / ' or op_perm[2] == ' - ')\
                        or op_perm[3] == ' / ':
                    solution_str.append('(' + str(num_perm[3]) + op_perm[3] + str(num_perm[4]) + ')' + brackets(
                        bracket) + ' = ' + str(result))
                else:
                    solution_str.append(
                        str(num_perm[3]) + op_perm[3] + str(num_perm[4]) + brackets(bracket) + ' = ' + str(result))

                add_solution(''.join(solution_str))
    for num_perm in set(permutations(number, 6)):
        for op_perm in (p for p in product(op, repeat=5)):

            result = calc(num_perm[0], op_perm[0],
                          calc(num_perm[1], op_perm[1],
                               calc(num_perm[2], op_perm[2],
                                    calc(num_perm[3], op_perm[3], calc(num_perm[4], op_perm[4], num_perm[5])))))
            if result == target:
                solution_str = []
                bracket = 0

                if (op_perm[1] == ' - ' and op_perm[0] != ' + ') or (
                        op_perm[1] == ' + ' and op_perm[0] != ' + ') or op_perm[1] == ' / ':
                    solution_str.append(
                        str(num_perm[0]) + op_perm[0] + '(' + str(num_perm[1]) + op_perm[1])
                    bracket = bracket + 1
                else:
                    solution_str.append(str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + op_perm[1])

                if (op_perm[2] == ' - ' and op_perm[1] != ' + ') or (
                        op_perm[2] == ' + ' and op_perm[1] != ' + ') or op_perm[2] == ' / ':
                    solution_str.append('(' + str(num_perm[2]) + op_perm[2])
                    bracket = bracket + 1
                else:
                    solution_str.append(str(num_perm[2]) + op_perm[2])

                if (op_perm[3] == ' - ' and op_perm[2] != ' + ') or (
                        op_perm[3] == ' + ' and op_perm[2] != ' + ') or op_perm[3] == ' / ':
                    solution_str.append('(' + str(num_perm[3]) + op_perm[3])
                    bracket = bracket + 1
                else:
                    solution_str.append(str(num_perm[3]) + op_perm[3])

                if (op_perm[4] == ' - ' and op_perm[3] != ' + ') or (
                        op_perm[4] == ' + ' and op_perm[3] != ' + ') or op_perm[4] == ' / ':
                    solution_str.append('(' + str(num_perm[4]) + op_perm[4] + str(num_perm[5]) + brackets(
                        bracket + 1) + ' = ' + str(result))
                else:
                    solution_str.append(str(num_perm[4]) + op_perm[4] + str(num_perm[5]) + brackets(
                        bracket) + ' = ' + str(result))

                add_solution(''.join(solution_str))

            result = calc(calc(calc(num_perm[0], op_perm[0], num_perm[1]), op_perm[1],
                               calc(num_perm[2], op_perm[2], num_perm[3])), op_perm[3],
                          calc(num_perm[4], op_perm[4], num_perm[5]))

            if result == target:

                solution_str = []

                if op_perm[3] == ' * ' and (op_perm[1] != ' * ' or op_perm[1] != ' / ') or op_perm[4] != ' * ':
                    solution_str.append('(')
                    bracket = 1

                if ((op_perm[0] == ' - ' or op_perm[0] == ' + ') and op_perm[1] != ' + ' and op_perm[1] != ' - ')\
                        or op_perm[1] == ' / ':
                    solution_str.append(
                        '(' + str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + ')' + op_perm[1])
                else:
                    solution_str.append(str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + op_perm[1])

                if (op_perm[2] == ' - ' and op_perm[1] != ' + ') or (
                        op_perm[2] == ' + ' and op_perm[1] != ' + ') or op_perm[2] == ' / ':
                    solution_str.append(
                        '(' + str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + ')' + brackets(
                            bracket) + op_perm[3])
                else:
                    solution_str.append(
                        str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + brackets(bracket) + op_perm[3])

                if (op_perm[4] == ' - ' and op_perm[3] != ' + ') or (
                        op_perm[4] == ' + ' and op_perm[3] != ' + ') or op_perm[4] == ' / ':
                    solution_str.append(
                        '(' + str(num_perm[4]) + op_perm[4] + str(num_perm[5]) + ')' + ' = ' + str(
                            result))
                else:
                    solution_str.append(
                        str(num_perm[4]) + op_perm[4] + str(num_perm[5]) + ' = ' + str(result))

                add_solution(''.join(solution_str))

            first = 0
            bracket = 0

            solution_str = []

            result = calc(calc(num_perm[0], op_perm[0],
                               calc(calc(num_perm[1], op_perm[1], num_perm[2]), op_perm[2],
                               calc(num_perm[3], op_perm[3], num_perm[4]))), op_perm[4], num_perm[5])

            if result == target:

                if ((op_perm[0] == ' - ' or op_perm[0] == ' + ') and op_perm[4] != ' + ' and op_perm[4] != ' - ')\
                        or op_perm[4] == ' / ':
                    solution_str.append('(' + str(num_perm[0]) + op_perm[0])
                    bracket = 1
                    first = 1
                else:
                    solution_str.append(str(num_perm[0]) + op_perm[0])

                if op_perm[2] == ' + ' and op_perm[0] == ' - ' or op_perm[2] == ' - '\
                        and op_perm[0] == ' - ' or op_perm[2] == ' - ' and op_perm[0] == ' + ' or op_perm[2] == ' / ':
                    solution_str.append('(')
                    bracket = bracket + 1

                if (op_perm[1] == ' + ' or op_perm[1] == ' - ' and (
                        (op_perm[0] != ' + ' and first != 1) or op_perm[2] != ' + ')) or op_perm[1] == ' / ':
                    solution_str.append(
                        '(' + str(num_perm[1]) + op_perm[1] + str(num_perm[2]) + ')' + op_perm[2])
                else:
                    solution_str.append(str(num_perm[1]) + op_perm[1] + str(num_perm[2]) + op_perm[2])

                if (op_perm[3] == ' + ' or op_perm[1] == ' - ' and (
                        op_perm[1] != ' + ' or (op_perm[2] != ' + ' and first != 1))) or op_perm[1] == ' / ':
                    solution_str.append('(' + str(num_perm[3]) + op_perm[3] + str(num_perm[4]) + brackets(
                        bracket + 1) + op_perm[4] + str(num_perm[5]) + ' = ' + str(result))
                else:
                    solution_str.append(
                        str(num_perm[3]) + op_perm[3] + str(num_perm[4]) + brackets(bracket) +
                        op_perm[4] + str(num_perm[5]) + ' = ' + str(result))

                add_solution(''.join(solution_str))
    print_solutions()


def print_solutions():
    if len(solutions) > 0:  # checks if it found anything
        for te in solutions:  # prints it
            print te
        print("Done.")
        print(str(len(solutions)) + " results were found.")  # tells the user how many result were found
        exit(0)


number = list(randint(1, 20) for i in range(6))

print 'Numbers:', number

target = randint(40, 100)

print 'Target:', target

solutions = []

numbers = []

# string_num = raw_input("What are the Numbers? \nPlease ensure that the numbers are separated by a comma.\n")

solution = []

# number = map(int, string_num.split(','))  # splits the numbers as per ',' and then changes their format to an integer

# target = int(raw_input("What is the Target?\n"))  # Asks the user for the target and converts it to an integer

op = (' + ', ' - ', ' / ', ' * ')  # represents plus, subtract, divide and times


solve()  # initiates the program
