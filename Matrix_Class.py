class Matrix(object):

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

    def multiply(self, b):
        if self.columns != b.rows:
            print 'Undefined'
            return 1
        product = []
        for r in range(self.rows):
            product.append([])
        for r in product:
            for c in range(b.columns):
                r.append(0)
        for r in range(self.rows):
            for c in range(b.columns):
                row = self.byrow[r]
                col = list(n[c] for n in b.byrow)
                product[r][c] = sum(list(row[i] * col[i] for i in range(self.columns)))
        return Matrix(product)

    def scale(self, m):
        product = []
        for r in range(self.rows):
            row = []
            for c in range(self.columns):
                row.append(self.byrow[r][c] * m)
            product.append(row)
        return Matrix(product)

    def add(self, b):
        if self.rows != b.rows or self.columns != b.columns:
            print 'Dimension Error. Cannot add matrices'
            return None
        else:
            sums = []
            for r in range(self.rows):
                row = []
                for c in range(self.columns):
                    row.append(self.byrow[r][c] + b.byrow[r][c])
                sums.append(row)
            return Matrix(sums)

    # Multiply row
    def mrow(self, row, factor):
        self.byrow[row] = list(n * factor for n in self.byrow[row])

    # Multiply row and add
    def mrow_add(self, row, factor, dest):
        for n in range(self.columns):
            self.byrow[dest][n] += factor * self.byrow[row][n]

    # Reduced Row Echelon Form. Returns the inverse.
    def rref(self):
        if not self.isSquare:
            print 'Dimension Error. Only square matrices have rref.'
            return None
        else:
            i = Identity(self.rows)
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

    def divide(self, b):
        return self.multiply(b.rref())

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.add(other.scale(-1))

    def __mul__(self, other):
        return self.multiply(other)

    def __pow__(self, power):
        if int(power) != power:
            print 'Domain Error. A Matrix can not be put to a fractional power.'
        if int(power) == -1:
            pass
        result = Matrix(self.byrow[:])
        for i in range(int(power)-1):
            result = result * self
        return result

    def __div__(self, other):
        return self.multiply(other.rref())

    def __lt__(self, other):
        return self.rows * self.columns < other

    def ___le__(self, other):
        return self.rows * self.columns <= other

    def __eq__(self, other):
        return self.rows * self.columns == other

    def __ne__(self, other):
        return self.rows * self.columns != other

    def __gt__(self, other):
        return self.rows * self.columns > other

    def __ge__(self, other):
        return self.rows * self.columns >= other

    def __str__(self):
        return str(self.byrow)

    def pprint(self):
        s = [[str(e) for e in row] for row in self.byrow]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = ['|' + fmt.format(*row) + '|' for row in s]
        print '\n'.join(table)

    @classmethod
    def identity(cls, size):
        matrix = []
        for r in range(size):
            row = []
            for c in range(size):
                if c == r:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)
        identity_matrix = cls(matrix)
        return identity_matrix


if __name__ == '__main__':
    a = Matrix([[2, 3], [3, 2], [3, 4]])
    b = Matrix([[2, 1], [0, 2]])
    i = Matrix.identity(4)
    i.pprint()
    print '\n',
    (a * b).pprint()
