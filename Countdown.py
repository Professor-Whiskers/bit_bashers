from random import *
from itertools import permutations, product
from time import time


def calc(a1, operator, a2):  # A basic function for calculating with
    global n_calc
    n_calc += 1
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


def counter(string, char):
    count = 0
    for c in string:
        if c == char:
            count += 1
    return count


def add_solution(result):
    result = remove_brackets(result)
    if len(solutions) < limit and result not in solutions:
        solutions.append(result)
        if len(solutions) == limit:
            print_solutions()


def compare_operators(first, second, pos):
    if first == '+':
        if second == '+':
            return True
        elif second == '-':
            if pos:
                return True
            else:
                return False
        elif second == '*':
            return False
        elif second == '/':
            return False
    elif first == '-':
        if second == '+':
            return True
        elif second == '-':
            if pos:
                return True
            else:
                return False
        elif second == '*':
            return False
        elif second == '/':
            return False
    elif first == '*':
        if second == '+':
            return True
        elif second == '-':
            return True
        elif second == '*':
            return True
        elif second == '/':
            if pos:
                return True
            else:
                return False
    elif first == '/':
        if second == '+':
            return True
        elif second == '-':
            return True
        elif second == '*':
            return True
        elif second == '/':
            if pos:
                return True
            else:
                return False


def remove_brackets(string):
    no_close_brackets = counter(string, ')')
    open_brackets = []
    firsts_to_skip = []
    brackets_to_remove = []
    first_op = '+'
    for i in range(len(string)):
        if string[i] == '(':
            open_brackets.append(i)
        elif string[i] == ')':
            for x in range(open_brackets[-1], i):
                if x not in firsts_to_skip and string[x] in ['+', '-', '/', '*']:
                    first_op = string[x]
                    firsts_to_skip.append(x)
                    break
            if len(firsts_to_skip) == no_close_brackets:
                for x in range(len(string)):
                    if x not in firsts_to_skip and string[x] in ['+', '-', '/', '*']:
                        if x > i:
                            pos = 1
                        else:
                            pos = 0
                        if compare_operators(first_op, string[x], pos):
                            brackets_to_remove.append(open_brackets[-1])
                            brackets_to_remove.append(i)

            if len(open_brackets) == 1 or open_brackets[-1] - 1 == open_brackets[-2]:
                pos = 1  # AFTER
                for x in range(i, len(string)):
                    if string[x] in ['+', '-', '/', '*']:
                        if compare_operators(first_op, string[x], pos):
                            brackets_to_remove.append(open_brackets[-1])
                            brackets_to_remove.append(i)
                        break
            else:  # BEFORE
                pos = 0
                for x in range(open_brackets[-2], open_brackets[-1]):
                    if string[x] in ['+', '-', '/', '*'] and x not in firsts_to_skip:
                        if compare_operators(first_op, string[x], pos):
                            brackets_to_remove.append(open_brackets[-1])
                            brackets_to_remove.append(i)
            open_brackets = open_brackets[:-1]
    new_string = list('' for i in range(len(string)))
    for i in range(len(string)):
        if i not in brackets_to_remove:
            new_string[i] = string[i]
    return ''.join(new_string)


def solve():
    global n_comp
    if target in number:
        add_solution(str(target) + ' = ' + str(target))
        
    for num_perm in set(permutations(number, 2)):
        for o1 in op:
            result = calc(num_perm[0], o1, num_perm[1])
            n_comp += 1
            if result == target:
                solution_str = ''.join(str(num_perm[0]) + o1 + str(num_perm[1]) + ' = ' + str(result))  
                add_solution(solution_str)

    for num_perm in set(permutations(number, 3)):
        for op_perm in (p for p in product(op, repeat=2)):
            result = calc(num_perm[0], op_perm[0], calc(num_perm[1], op_perm[1], num_perm[2]))
            # a + (b + c)
            n_comp += 1
            if result == target:
                solution_str = str(num_perm[0]) + op_perm[0] + '(' +\
                               str(num_perm[1]) + op_perm[1] + str(num_perm[2]) + ')' + ' = ' + str(result)
                add_solution(solution_str)

            result = calc(calc(num_perm[0], op_perm[0], num_perm[1]), op_perm[1], num_perm[2])
            # (a + b) + c
            n_comp += 1
            if result == target:
                solution_str = '(' + str(num_perm[0]) + op_perm[0] + \
                               str(num_perm[1]) + ')' + op_perm[1] + str(num_perm[2]) + ' = ' + str(result)
                add_solution(solution_str)

    for num_perm in set(permutations(number, 4)):
        for op_perm in (p for p in product(op, repeat=3)):
            
            result = calc(num_perm[0], op_perm[0], calc(num_perm[1], op_perm[1],
                                                        calc(num_perm[2], op_perm[2], num_perm[3])))
            # a + (b + (c + d))
            n_comp += 1
            if result == target:
                solution_str = str(num_perm[0]) + op_perm[0] + '(' + str(num_perm[1]) + op_perm[1] + '(' +\
                               str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + ')) = ' + str(result)
                add_solution(solution_str)

            result = calc(calc(num_perm[0], op_perm[0], num_perm[1]), op_perm[1],
                          calc(num_perm[2], op_perm[2], num_perm[3]))
            # (a + b) + (c + d)
            n_comp += 1
            if result == target:
                solution_str = '(' + str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + ')' + op_perm[1] + '(' + \
                               str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + ') = ' + str(result)
                add_solution(solution_str)

            result = calc(num_perm[0], op_perm[0],
                          calc(calc(num_perm[1], op_perm[1], num_perm[2]), op_perm[2], num_perm[3]))
            # a + ((b + c) + d)
            n_comp += 1
            if result == target:
                solution_str = str(num_perm[0]) + op_perm[0] + '((' + str(num_perm[1]) + op_perm[1] + \
                               str(num_perm[2]) + ')' + op_perm[2] + str(num_perm[3]) + ') = ' + str(result)
                add_solution(solution_str)
    for num_perm in set(permutations(number, 5)):
        for op_perm in (p for p in product(op, repeat=4)):
            n_comp += 1
            result = calc(num_perm[0], op_perm[0],
                          calc(num_perm[1], op_perm[1],
                               calc(num_perm[2], op_perm[2],
                                    calc(num_perm[3], op_perm[3], num_perm[4]))))
            # a + (b + (c + (d + e)))
            if result == target:
                solution_str = str(num_perm[0]) + op_perm[0] + '(' + str(num_perm[1]) + op_perm[1] + \
                               '(' + str(num_perm[2]) + op_perm[2] + '(' + str(num_perm[3]) + op_perm[3]\
                               + str(num_perm[4]) + '))) = ' + str(result)
                add_solution(solution_str)
            n_comp += 1
            result = calc(calc(calc(num_perm[0], op_perm[0], num_perm[1]), op_perm[1],
                               calc(num_perm[2], op_perm[2], num_perm[3])), op_perm[3], num_perm[4])
            # ((a + b) + (c + d)) + e
            if result == target:
                solution_str = '((' + str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + ')' + op_perm[1] + \
                               '(' + str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + '))' + op_perm[3] \
                               + str(num_perm[4]) + ' = ' + str(result)
                add_solution(solution_str)
            n_comp += 1
            result = calc(calc(num_perm[0], op_perm[0], num_perm[1]), op_perm[1],
                          calc(num_perm[2], op_perm[2], calc(num_perm[3], op_perm[3], num_perm[4])))
            # (a + b) + (c + (d + e))
            if result == target:
                solution_str = '(' + str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + ')' + op_perm[1] + \
                               '(' + str(num_perm[2]) + op_perm[2] + '(' + str(num_perm[3]) + op_perm[3] \
                               + str(num_perm[4]) + ')) = ' + str(result)
                add_solution(solution_str)

    for num_perm in set(permutations(number, 6)):
        for op_perm in (p for p in product(op, repeat=5)):
            n_comp += 1
            result = calc(num_perm[0], op_perm[0],
                          calc(num_perm[1], op_perm[1],
                               calc(num_perm[2], op_perm[2],
                                    calc(num_perm[3], op_perm[3], calc(num_perm[4], op_perm[4], num_perm[5])))))
            # a + (b + (c + (d + (e + f))))
            if result == target:
                solution_str = str(num_perm[0]) + op_perm[0] + '(' + str(num_perm[1]) + op_perm[1] + \
                               '(' + str(num_perm[2]) + op_perm[2] + '(' + str(num_perm[3]) + op_perm[3] \
                               + '(' + str(num_perm[4]) + op_perm[4] + str(num_perm[5]) + ')))) = ' + str(result)
                add_solution(solution_str)
            n_comp += 1
            result = calc(calc(calc(num_perm[0], op_perm[0], num_perm[1]), op_perm[1],
                               calc(num_perm[2], op_perm[2], num_perm[3])), op_perm[3],
                          calc(num_perm[4], op_perm[4], num_perm[5]))
            # ((a + b) + (c + d)) + (e + f)
            if result == target:
                solution_str = '((' + str(num_perm[0]) + op_perm[0] + str(num_perm[1]) + ')' + op_perm[1] + \
                               '(' + str(num_perm[2]) + op_perm[2] + str(num_perm[3]) + '))' + op_perm[3] \
                               + '(' + str(num_perm[4]) + op_perm[4] + str(num_perm[5]) + ') = ' + str(result)
                add_solution(solution_str)
            n_comp += 1
            result = calc(calc(num_perm[0], op_perm[0],
                               calc(calc(num_perm[1], op_perm[1], num_perm[2]), op_perm[2],
                               calc(num_perm[3], op_perm[3], num_perm[4]))), op_perm[4], num_perm[5])
            # (a + ((b + c) + (d + e))) + f
            if result == target:
                solution_str = '(' + str(num_perm[0]) + op_perm[0] + '((' + str(num_perm[1]) + op_perm[1] +\
                               str(num_perm[2]) + ')' + op_perm[2] + '(' + str(num_perm[3]) + op_perm[3] \
                               + str(num_perm[4]) + ')))' + op_perm[4] + str(num_perm[5]) + ' = ' + str(result)
                add_solution(solution_str)
    print_solutions()


def print_solutions():
    time_d = time() - now
    if len(solutions) > 0:  # checks if it found anything
        for te in solutions:  # prints it
            print(te)
    print("Done.")
    print(str(len(solutions)) + " results were found.")  # tells the user how many result were found
    print('Time = ', time_d)
    print('Calculations performed', n_calc)
    print('Comparisons: ', n_comp)
    exit(0)


if __name__ == '__main__':
    number = [1, 2, 3, 4, 5, 6]
    print('Numbers:', number)

    # target = randint(40, 100)
    target = 582
    print('Target:', target)

    solutions = []

    numbers = []
    n_calc = 0
    # string_num = raw_input("What are the Numbers? \nPlease ensure that the numbers are separated by a comma.\n")
    n_comp = 6

    limit = 1

    solution = []

    # number = map(int, string_num.split(','))

    # target = int(raw_input("What is the Target?\n"))  # Asks the user for the target and converts it to an integer

    op = (' + ', ' - ', ' / ', ' * ')  # represents plus, subtract, divide and times

    now = time()

    solve()  # initiates the program

