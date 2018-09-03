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
            copy = Matrix(self.byrow[:])
            for c in range(self.columns):
                i.mrow(c, copy.byrow[c][c] ** -1)
                copy.mrow(c, copy.byrow[c][c] ** -1)
                for r in range(self.rows):
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
        # Matrices can only be put to integer powers
        if int(power) != power:
            print 'Domain Error. A Matrix can not be put to a fractional power.'
        if int(power) == -1:
            pass
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
        return str(self.byrow)

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
        print '\n'.join(table)

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


if __name__ == '__main__':
    a = Matrix([[2, 3], [3, 2], [3, 4]])
    b = Matrix([[2, 2], [0, 2]])
    i = Matrix.identity(4)
    i.pprint()
    print '\n',
    (a * b).pprint()
