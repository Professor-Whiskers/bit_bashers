class Matrix(object):
    """
    A class for Matrices. Input should be in by-row format:
    |a b|
    |c d|     ---- > [[a,b],[c,d],[e,f]]
    |e f|
    """
    def __init__(self, n):
        self.byrow = n
        self.rows = len(self.byrow)
        self.columns = len(self.byrow[0])
        for row in self.byrow:
            if len(row) != self.columns:
                print "Invalid Matrix. Filling gaps with 0s."
                max_column = 0
                for nrow in self.byrow:
                    if len(nrow) > max_column:
                        max_column = len(nrow)
                for nrow in self.byrow:
                    while len(nrow) != max_column:
                        nrow.append(0)
        if self.columns == self.rows:
            self.isSquare = True
        else:
            self.isSquare = False

    # Conforms to matrix multiplication. Returns a matrix object.
    def multiply(self, b):
        if self.columns != b.rows:  # Checks to see if matrices are compatible
            print 'Undefined'
            return
        product = []
        # Create the empty matrix
        for r in range(self.rows):
            product.append([])
        for r in product:
            for c in range(b.columns):
                r.append(0)
        # Perform the multiplication
        for r in range(self.rows):
            for c in range(b.columns):
                row = self.byrow[r]
                col = list(n[c] for n in b.byrow)  # grabs the num in the desired column for every row
                product[r][c] = sum(row[i] * col[i] for i in range(self.columns))  # See dot product
        return Matrix(product)

    # Scales a matrix by a constant factor
    def scale(self, f):
        # Create empty matrix
        product = []
        # Iterate over every number and multiply it by factor
        for r in range(self.rows):
            # Create empty row
            row = []
            for c in range(self.columns):
                # Multiply number at row r and column c by f
                row.append(self.byrow[r][c] * f)
            # Append row to resultant matrix
            product.append(row)
        return Matrix(product)

    # Adds two matrices of identical dimensions
    def add(self, b):
        # Check if matrices are the same size
        if self.rows != b.rows or self.columns != b.columns:
            print 'Dimension Error. Cannot add matrices'
            return
        else:
            # Create empty matrix
            sums = []
            # Iterate over every number in both matrices and add them
            for r in range(self.rows):
                # Create empty row
                row = []
                for c in range(self.columns):
                    # Add numbers at row r and column c together
                    row.append(self.byrow[r][c] + b.byrow[r][c])
                # Append row to resultant matrix
                sums.append(row)
            return Matrix(sums)

    # Multiply row (Operation)
    def mrow(self, row, factor):
        self.byrow[row] = list(n * factor for n in self.byrow[row])

    # Multiply row and add (Operation)
    def mrow_add(self, row, factor, dest):
        for n in range(self.columns):
            self.byrow[dest][n] += factor * self.byrow[row][n]

    # Reduced Row Echelon Form. Returns the inverse.
    def rref(self):
        if not self.isSquare:
            print 'Dimension Error. Only square matrices have rref.'
            return None
        else:
            i = Matrix.identity(self.rows)
            i = Matrix.fractionalise(i)
            copy = Matrix.copy(self)
            copy = Matrix.fractionalise(copy)
            for c in range(copy.columns):
                i.mrow(c, copy.byrow[c][c] ** -1)
                copy.mrow(c, copy.byrow[c][c] ** -1)
                for r in range(copy.rows):
                    if r == c:
                        continue
                    i.mrow_add(c, -1 * copy.byrow[r][c], r)
                    copy.mrow_add(c, -1 * copy.byrow[r][c], r)
            return i

    # Multiplies matrix by inverse of other matrix (divides)
    def divide(self, b):
        return self.multiply(b.rref())

    # Adds two matrices. Overloads + operator
    def __add__(self, other):
        return self.add(other)

    # Subtracts two matrices. Overloads - operator
    def __sub__(self, other):
        return self.add(other.scale(-1))

    # Multiplies two matrices. Overloads * operator
    def __mul__(self, other):
        if type(self) == type(other):
            return self.multiply(other)
        else:
            return self.scale(other)

    # Scales the matrix. Accounts for Scalar * Matrix Case
    def __rmul__(self, other):
        return self.scale(other)

    # Raises a matrix to a power. Overloads ** operator
    def __pow__(self, power):
        if not self.isSquare:
            print 'Only square Matrices can be put to a power.'
        # Matrices can only be put to integer powers
        elif int(power) != power:
            print 'Domain Error. A Matrix can not be put to a fractional power.'
        elif power == 1:
            return self
        elif power == -1:
            return self.rref()
        elif power == 0:
            return Matrix.identity(self.rows)
        elif power < 0:
            inverse = Matrix(self.byrow[:]).rref()
            result = Matrix.copy(inverse)
            for i in range(abs(power) - 1):
                result = result * inverse
        else:
            result = Matrix(self.byrow[:])
            for i in range(int(power)-1):
                result = result * self
            return result

    # Divides two. Overloads / operator
    def __div__(self, other):
        return self.divide(other)

    # Returns True if dimensions are equal. Overloads == operator
    def __eq__(self, other):
        return self.rows == other.rows and self.columns == other.columns

    # Returns True if dimensions aren't equal. Overloads != operator
    def __ne__(self, other):
        return self.rows != other.rows and self.columns != other.columns

    # Defines str() function
    # Allows for print() calls
    def __str__(self):
        return self.pprint()

    # Defines object representation.
    def __repr__(self):
        return self.pprint()

    # Pretty print function
    def pprint(self):
        """
        Format:
        |a  b|
        |c  d|
        |e  f|

        """
        # Convert every int to a str
        s = [[str(e) for e in row] for row in self.byrow]
        # Get the length of the longest str for each column
        lens = [max(map(len, col)) for col in zip(*s)]
        # Format table with appropriate spacing
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        # Fill table
        table = ['|' + fmt.format(*row) + '|' for row in s]
        # Print table
        table = '\n'.join(table)
        return table

    # method for creating an identity matrix
    @classmethod
    def identity(cls, size):
        matrix = []
        for r in range(size):
            row = []
            for c in range(size):
                # Check if on diagonal
                if c == r:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        identity_matrix = cls(matrix)
        return identity_matrix

    @classmethod
    def copy(cls, matrix):
        new = []
        for n in matrix.byrow:
            new.append(list(x for x in n))
        return cls(new)

    # Converts numbers in list to fractions if they aren't already
    @classmethod
    def fractionalise(cls, matrix):
        frac_m = []
        for r in matrix.byrow:
            frac_r = []
            for c in r:
                if isinstance(c, Fraction):
                    frac_r.append(c)
                else:
                    frac_r.append(Fraction(c, 1))
            frac_m.append(frac_r)
        return cls(frac_m)


class Fraction(object):

    def __init__(self, num, den):
        self.num = num  # numerator
        self.den = den  # denominator
        self.check_factors()

    # Multiplies the fraction
    def multiply(self, x):
        if type(self) == type(x):
            return Fraction(self.num * x.num, self.den * x.den)
        else:
            return Fraction(self.num * x, self.den * 1)

    # Divides the fraction
    def divide(self, x):
        if type(self) == type(x):
            return Fraction(self.num * x.den, self.den * x.num)
        else:
            return Fraction(self.num * 1, self.den * x)

    # returns the sum of two numbers
    def add(self, x):
        if type(self) == type(x):
            new_den = self.den * x.den
            new_num = x.den * self.num + self.den * x.num
            return Fraction(new_num, new_den)
        else:
            new_num = self.num + x * self.den
            return Fraction(new_num, self.den * 1)

    # returns the difference between two numbers.
    def subtract(self, x):
        if type(self) == type(x):
            new_den = self.den * x.den
            new_num = x.den * self.num - self.den * x.num
            return Fraction(new_num, new_den)
        else:
            new_num = self.num - (x * self.den)
            return Fraction(new_num, self.den * 1)

    # Returns inverse of fraction. (a/b)^ -1 = b/a
    def inverse(self):
        return Fraction(self.den * 1, self.num * 1)

    # Checks to make sure fraction is in its simplest form
    def check_factors(self):
        if self.num < 0 and self.den < 0:
            self.num = abs(self.num)
            self.den = abs(self.den)
        elif self.den < 0:
            self.num = self.num * -1
            self.den = abs(self.den)

        if self.num == 0:
            return
        else:
            num_factors = reduce(
                list.__add__,
                ([i, abs(self.num) / i] for i in range(1, int(abs(self.num) ** 0.5 + 1)) if not abs(self.num) % i))
            den_factors = reduce(
                list.__add__, ([i, self.den / i] for i in range(1, int(abs(self.den) ** 0.5 + 1)) if not self.den % i))
            num_factors.sort()
            for n in num_factors[::-1]:
                if n in den_factors:
                    self.num /= n
                    self.den /= n
                    break

    # Adds two fractions. Overloads + operator
    def __add__(self, other):
        return self.add(other)

    def __radd__(self, other):
        return self.add(other)

    # Subtracts two fractions. Overloads - operator
    def __sub__(self, other):
        return self.subtract(other)

    def __rsub__(self, other):
        return self.subtract(other)

    # Multiplies two fractions. Overloads * operator
    def __mul__(self, other):
        return self.multiply(other)

    # Scales the Fraction. Accounts for Scalar * Fraction Case
    def __rmul__(self, other):
        return self.multiply(other)

    # Raises a fraction to a power. Overloads ** operator
    def __pow__(self, power):
        if int(power) != power:
            print 'Fraction doesn\'t handle fractional powers atm'
        elif power == 1:
            return self
        elif power == -1:
            return self.inverse()
        elif power == 0:
            return Fraction(1, 1)
        elif power < 0:
            return Fraction(self.den ** abs(power), self.num ** abs(power))
        else:
            return Fraction(self.num ** power, self.den ** power)

    # Divides two. Overloads / operator
    def __div__(self, other):
        return self.divide(other)

    # Returns True if dimensions are equal. Overloads == operator
    def __eq__(self, other):
        return self.num == other.num and self.den == other.den

    # Returns True if dimensions aren't equal. Overloads != operator
    def __ne__(self, other):
        return self.num != other.num and self.den != other.den

    def __str__(self):
        if self.den == 1:
            return str(self.num)
        elif self.num == 0:
            return '0'
        else:
            return '{0}/{1}'.format(self.num, self.den)


if __name__ == '__main__':
    a = Matrix([[2, 3], [3, 2]])
    b = Matrix([[2, 2], [0, 2]])
    i = Matrix.identity(2)
    print i
    print a/b + i



