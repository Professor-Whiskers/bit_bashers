def strtoint(str):
    try:
        return int(str)
    except ValueError:
        print "Not an int"
        return None


# C -> F = 9 / 5 * C + 32
def cel_to_far(cel):
    return (9 / 5.0) * cel + 32


def far_to_cel(far):
    return (far - 32) * 5 / 9.0


# Print table of values
if __name__ == '__main__':
    
    # Header:
    print 'Celsius\tFahrenheit'
    print '-------\t----------'

    # Contents:
    for cel in range(-100, 100, 20):
        if len(str(cel)) > 2:
            print cel, '\t', cel_to_far(cel)
        else:
            print cel, '\t\t', cel_to_far(cel)

