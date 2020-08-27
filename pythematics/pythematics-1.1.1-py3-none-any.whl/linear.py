"""
    Contains a series of functions and custom classes,\n
    concerning the base of linear algebra,
    Matrices and Vectors

    Here are the operations:
    -- Vectors : 
        ** Vector Dot 
        ** Vector Cross (3D ONLY)
        ** Vector Addition and Subtraction
        ** Vector-Scalar Operations
    -- Matrices:
        ** Matrix Multiplication
        ** Matrix Addition and subtraction
        ** Matrix-Scalar Operations
        ** Trace
        ** Identity Matrix Generator
        ** Determinant
        ** Inverse Matrix
            ** Cofactors
            ** adjugate (transpose)
            ** Minors
"""

from .basic import isNumber
from typing import Union

WHITESPACE = ' '

class Vector:
    def __init__(self,array):
        for item in array:
            if not isNumber(item):
                raise ValueError("Vector arguments must be a list of {} or {} not {}".format(int,float,type(item)))
        self.matrix = array
        self.rows = len(self.matrix)
        self.collumns = 1

    def __str__(self):
        print("")
        i = 1
        for item in self.matrix:
            print(f'R{i}| {item:>3}')
            i+=1
        s2 = "\n{} x {} Vector array\n".format(self.rows,self.collumns)
        return s2

    def getMatrix(self):
        return self.matrix

    def getSize(self):
        return self.rows

    def __add__(self,value):
        empty = []
        if type(value) == Vector:
            if value.getSize() != self.getSize():
                raise ValueError("Cannot multiply non equal-size collumns ({} with {})".format(value.getSize(),self.getSize()))
            for i in range(self.getSize()):
                empty.append(value.getMatrix()[i] + self.getMatrix()[i])
            return Vector(empty)
        raise TypeError("Cannot perform addition on Vector with {}".format(type(value)))

    def __sub__(self,value):
        empty = []
        if type(value) == type(self):
            if value.getSize() != self.getSize():
                raise ValueError("Cannot multiply non equal-size collumns ({} with {})".format(value.getSize(),self.getSize()))
            for i in range(self.getSize()):
                empty.append(value.getMatrix()[i] - self.getMatrix()[i])
            return Vector(empty)
        else:
            raise ValueError("Cannot Perform subtraction : {} with {}".format(type(self),type(value)))

    def __len__(self):
        return self.rows

    def __mul__(self,value):
        """Vector Multiplication by scalar
            if other value is Vector,
            the dot product is returned
        """
        empty = []
        if isNumber(value): #Scalar
            for item in self.matrix:
                empty.append(value*item)
            return Vector(empty)
        elif type(value) == type(self):
            if value.getSize() != self.getSize():
                raise ValueError("Cannot multiply non equal-size collumns ({} with {})".format(value.getSize(),self.getSize()))
            for num in range(self.getSize()):
                empty.append(value.getMatrix()[num] * self.getMatrix()[num])
            return sum(empty)

    def __rmul__(self,scalar : Union[int,float]):
        if type(scalar) in (int,float):
            return self.__mul__(scalar)
        raise TypeError("Cannot perform '*' operation on Vector with {}")

    def dot(self,Vector) -> Union[float,int]:
        return self.__mul__(Vector) 
    
    # def cross(self,Vector)


class Matrix:
    """
    The as you known it from math 'Matrix'\n
    It includes custom operations for the following:
        ** Multiplication
        ** Addition
        ** Subtraction

    These are also supported not as methods but as seperate functions:
        ** determinant
        ** inverse
        ** Transpose (adjugate)
        ** Matrix of co-factors (Alternating-Chess pattern sign)
        ** Matrix of  Minors (for each element hide the current row and collumn and find the determinant of the following) 

    You must pass an array of arrays,\n
    Inside the base array the nested lists are considered as the rows,\n
    and the collumns are determined vertically\n
    Matrices shall be passed in the following format :

    [   
            #Col1  #Col2  #Col3
     #Row 1 [num1 , num2 , num3 ],
     #Row 2 [num4,  num5 , num6 ],
                ..........
     #Row n [numK,numL,numO]
    ]

        Input :
        A = Matrix([
            [1,2,3],
            [4,5,6],
            [7,8,9]
        ])

        Output :
                C1      C2      C3

        R1 |    1        2       3
        R2 |    4        5       6
        R3 |    7        8       9

    for more specific methods you can use the dir() function

    """
    def __init__(self,matrix):
        """Takes an array of arrays of numbers
            The arrays inside the array as seen as the rows
        """
        if type(matrix) != list:
            raise ValueError("Matrix must be an array of arrays.")
        
        self.ROW_LENGTHS = []

        for row in matrix:
            if type(row) == list:
                self.ROW_LENGTHS.append(len(row))
                for num in row:
                    if not isNumber(num):
                        raise TypeError("Row : {} , does not contain an argument or {} or {} but instead {}!".format(matrix.index(row),type(1),type(1.0),type(num)))
            else:
                raise ValueError("Every argument inside the base array which is considered as a row should be of type {} not {}".format(list,type(matrix)))
        if len(self.ROW_LENGTHS) != self.ROW_LENGTHS.count(self.ROW_LENGTHS[0]):
            raise ValueError("All rows of a matrix shall only be of same size. not {}".format(self.ROW_LENGTHS))

        self.matrix = matrix
        self.rows = len(self.matrix)
        self.collumns = self.ROW_LENGTHS[0]
        self.isSquare = self.rows == self.collumns

        self.cols = []
        for j in range(self.ROW_LENGTHS[0]):
            self.cols.append([])

        for row in self.matrix:
            i = 0
            for value in row:
                self.cols[i].append(value)
                i+=1

    def rawMatrix(self):
        """Returns the raw array passed in (self.matrix)"""
        return self.matrix

    def colls(self,index : int = 0) -> list:
        """Returns a collumn when an index is specified (default is 0)"""
        return self.cols[index]
    
    def is_square(self) -> bool:
        return self.isSquare

    def collsAll(self) -> list:
        """Returns an array of all the collumns"""
        return self.cols

    def row(self,index : int = 0):
        """Returns a specific row given an index (default is 0)"""
        return self.matrix[index]

    def __len__(self):
        """Returns a tuple containng number of rows and collumns (rows,collumns)"""
        return (self.rows,self.collumns) # (number of rows,number of collumns)

    def __str__(self):
        """Returns a visual representation of the Matrix"""
        print("")
        x = [item[:] for item in self.matrix]
        k = 0
        for item in x:
            j = 0
            if len(item) > 8:
                x[k] = item[1:9]
                x[k].append("...")
                x[k].append(self.cols[-1][j])
                j+=1
            k+=1
        k = 0        
        y = []    
        for iteration in range(self.collumns):
            if iteration >=8:
                y.append("...")
                y.append(f'C{self.collumns}')
                break
            y.append(f"C{iteration+1}")
        x.insert(0,y)
        j = 1
        for item in x:
            if j > 9:
                print("\n   .........")
                print(f' R{len(x)-1}|',*x[-1])
                break
            item[0] = f'\t{item[0]}'
            if j==1:
                print(' CI |',"\t".join(f'{val:>3}' for val in item))
                j+=1
                continue
            print(f' R{j-1} |',"\t".join(f'{val:>3}' for val in item))
            j+=1
        # i = 0
        # for item in x:
        #     if i!=0:
        #         print(f'R{i+1}|',"\t".join([f'{val:>3}' for val in item]))
        #     else:
        #         print('   ',"\t".join([f'{val:>3}' for val in item]))
        #         print("")
        #     i+=1
        # i = 0
        # for item in x:
        #     print(f' R{i+1} |',*[f'{val:>3}' for val in item])
        #     i+=1
        return f'\n{self.rows} x {self.collumns} Matrix\n'

    def __rmul__(self,scalar):
        """Matrix multiplication by scalar"""
        if type(scalar) in (int,float):
            new_matrix = [[] for i in range(self.rows)] #Add the rows
            i = 0
            for row in self.matrix:
                for constant in row:
                    new_matrix[i].append(constant * scalar)
                i+=1
            return Matrix(new_matrix)
        else:
            raise TypeError("You may only multiply a {} object with either a {} or a {}".format(type(self),int,float))

    def __neg__(self):
        return (-1) * self
    
    def __add__(self,Matrx):
        if type(Matrx) != type(self):
            raise ValueError("A Matrix may only be added with another Matrix not {}!".format(type(Matrx)))
        if self.__len__() != Matrx.__len__():
            raise ValueError("Rows and Collumns must be equal! {} != {}".format(self.__len__(),Matrx.__len__()))
        new_matrix = [[] for row in range(self.rows)]
        i = 0
        for row in self.matrix:
            k = 0 
            for num in row:
                new_matrix[i].append(num+Matrx.rawMatrix()[i][k])
                k +=1
            i+=1
        return Matrix(new_matrix)

    def __sub__(self,Matrx):
        if type(Matrx) != type(self):
            raise ValueError("A Matrix may only be added with another Matrix not {}!".format(type(Matrx)))
        if self.__len__() != Matrx.__len__():
            raise ValueError("Rows and Collumns must be equal! {} != {}".format(self.__len__(),Matrx.__len__()))
        new_matrix = [[] for row in range(self.rows)]
        i = 0
        for row in self.matrix:
            k = 0 
            for num in row:
                new_matrix[i].append(num-Matrx.rawMatrix()[i][k])
                k +=1
            i+=1
        return Matrix(new_matrix)

    def __mul__(self,value):
        if type(value) in (int,float):
            return self.__rmul__(value)
        row_0 = self.__len__()
        col_0 = value.__len__()
        if row_0[1] != col_0[0]: 
            raise ValueError(f"\nCannot multiply a {row_0[0]} x {row_0[1]} with a {col_0[0]} x {col_0[1]} Matrix,\nMatrix 1 must have the same number of rows as the number of collumns in Matrix 2 \n({row_0[1]} != {col_0[0]})")
        new_matrix = [[] for i in range(row_0[0])]
        COLS_M2 = value.collsAll()
        j = 0
        for row in self.matrix:
            for collumn in COLS_M2:
                iterations = 0
                total = 0
                for scalar in collumn:
                    total += scalar*row[iterations]
                    iterations+=1
                new_matrix[j].append(total)
            j+=1
        return Matrix(new_matrix)


def removeCollumn(matrix : Matrix,index : int) -> Matrix:
    """Returns a reduced collumn version of a Matrix"""
    raw_matrix = [item[:] for item in matrix.rawMatrix()]
    for row in raw_matrix:
        row.pop(index)
    return Matrix(raw_matrix)

def determinant(matrix : Matrix) -> float:
    dimensions = matrix.__len__()
    if not matrix.is_square():
        raise ValueError("Cannot compute determinant of non square matrix : {}".format(dimensions))
    if dimensions[0] == 2:
        return matrix.rawMatrix()[0][0] * matrix.rawMatrix()[-1][-1] - matrix.rawMatrix()[0][-1]* matrix.rawMatrix()[-1][0]
    raw_matrix = matrix.rawMatrix()
    tmp = [item[:] for item in raw_matrix]
    tmp.pop(0)
    i = 0 
    STORAGE = []
    for i in range(matrix.__len__()[0]): #Loop throw the first row
        y = removeCollumn(Matrix(tmp),i)
        multiplier = raw_matrix[0][i] if (i+1)%2!=0 else -raw_matrix[0][i]
        STORAGE.append(multiplier * determinant(y))
        i+=1
    return sum(STORAGE)


def MatrixOfCofactors(matrix : Matrix) -> float:
    """
        Given any NxM Matrix \n : 
        it reutrns a new Matrix,
        that follows the chessboard pattern
    """

    if matrix.__len__()[0] == 2:
        raise ValueError("Matrix must be more than 2 dimensional")
    array = [item[:] for item in matrix.rawMatrix()]
    new_array = [[] for item in matrix.rawMatrix()]
    i = 0
    positive = True
    positive_col = True
    for row in array:
        j = 0
        for number in row:
            if positive:
                new_array[i].append(number)
            else:
                new_array[i].append(-number)

            if j+1 != len(row):
                positive = not positive
            
            else:
                positive_col = not positive_col
                positive = positive_col
            j+=1
        i+=1
    return Matrix(new_array)


def adjugate(matrix : Matrix) -> float:
    """It transposes a given Matrix,"""
    array = [item[:] for item in matrix.rawMatrix()]
    arrays = [[] for item in matrix.rawMatrix()]
    for row in array:
        i = 0
        for num in row:
            arrays[i].append(num)
            i+=1
    return Matrix(arrays)


def MatrixOfMinors(matrix : Matrix) -> Matrix:
    """
        Given an square Matrix that is not 2x2 it returns a new Matrix,\n
        The new Matrix is generated by the determinants generated by the following:\n
            ** For each item in the Matrix :
                ** 'Hide' the current collumn and row
                ** Now compute the determinant of the remaining Matrix
    """
    matrix_len = matrix.__len__()
    if not matrix.is_square():
        raise ValueError("Cannot perfrom Matrix of minors on non-square matrix : {}".format(matrix_len))
    matrix_array = [row[:] for row in matrix.rawMatrix()]
    j=0
    DETERMINANTS = [[] for row in matrix.rawMatrix()]
    for row in matrix_array:
        i = 0 
        reduced = [item[:] for item in matrix_array]
        reduced.pop(j)
        for num in row:
            x = removeCollumn(Matrix(reduced),i)
            DETERMINANTS[j].append(determinant(x))
            i+=1
        j+=1
    return Matrix(DETERMINANTS)

def inverse(matrix : Matrix) -> Matrix:
    """
        => Find 'Matrix of Minors'; #New Matrix with the determinants of each item of the array
        => Find Matrix of co-factors of the previous Matrix; #Alternating chessboard sign
        => Transpose (adjugate) that Matrix
        => Multiply by 1 / determinant
    """
    assert matrix.is_square() , "Cannot Invert non square matrix : {}".format(matrix.__len__())
    if matrix.__len__()[0] == 2:
        raw = matrix.rawMatrix()
        return (1 / determinant(matrix)) * Matrix(
            [[raw[-1][-1],-raw[0][-1]],
            [-raw[-1][0],raw[0][0]]
        ])
    try:
        inverse_determinant = 1 /  determinant(matrix)
    except:
        raise ZeroDivisionError("Determinant is 0")
    return inverse_determinant * adjugate(MatrixOfCofactors(MatrixOfMinors(matrix)))


def cross(vector_1 : Vector,vector_2 : Vector) -> Vector:
    if (type(vector_1),type(vector_2)).count(Vector) != 2:
        raise TypeError("Both arguments must be Vectors not {} and {}".format(type(vector_1),type(vector_2)))
    if (len(vector_1.getMatrix()),len(vector_2.getMatrix())).count(3) != 2:
        raise ValueError("Cannot perform cross product on non 3-dimensional Vectors : ({},{})".format(len(vector_1.getMatrix()),len(vector_2.getMatrix())))
    A = [vector_1.getMatrix(),vector_2.getMatrix()]
    DETERMINANTS = []
    for i in range(3):
        if (i+1)%2==0:
            DETERMINANTS.append(-determinant(removeCollumn(Matrix(A),i)))
            continue
        DETERMINANTS.append(determinant(removeCollumn(Matrix(A),i)))
    return Vector(DETERMINANTS)

def IdenityMatrix(dimensions : int) -> Matrix:
    if dimensions <= 1:
        raise ValueError("Dimensions must be at least 2 (not {}).".format(dimensions))
    matrix = []
    for i in range(dimensions):
        row = []
        for k in range(dimensions):
            if k == i:
                row.append(1)
                continue
            row.append(0)
        matrix .append(row)
    return Matrix(matrix)

def Trace(matrix : Matrix) -> Union[int,float]:
    """Returns the sum of the diagnals of a matrix"""
    if type(matrix) != Matrix:
        raise TypeError("Cannot only perform 'Trace' operation on {} (not {})".format(Matrix,type(matrix)))
    if not matrix.is_square():
        raise ValueError("Cannot only perform 'Trace' operation square matrices (not {})".format(matrix.__len__()))
    raw_matrix = matrix.rawMatrix()
    diagnals = []
    i = 0 #Track of row_matrix.index(row)
    for row in raw_matrix: 
        j = 0
        for num in row:
            if j==i:
                diagnals.append(num)
                break
            j+=1
        i+=1
    return sum(diagnals)

if __name__ == "__main__":
    A = Matrix([
            [1,2],
            [4,5]
            ])


    print(A)

