def is_sorted(num):
    for n in range(len(num)-1):
            if not num[n] <= num[n+1]:
                return False
    else:
        return True


def sort(num):
    while not is_sorted(num):
        for n in range(len(num)-1):
            if num[n] > num[n+1]:
                num[n], num[n+1] = num[n+1], num[n]
    return num
