from collections import deque
import csv
import functools
import itertools
import os
import sys

class Square:
    def __init__(self, small_width_in_cells, large_width_in_cells, values):
        self.large_width_in_cells = large_width_in_cells
        self.large_width_in_small_squares = int(large_width_in_cells / small_width_in_cells)
        assert(large_width_in_cells % small_width_in_cells == 0)
        self.small_width_in_cells = small_width_in_cells
        self.values = values

        self.matrix = list(itertools.repeat(None, large_width_in_cells*large_width_in_cells))
        self.sets = [list() for i in range(large_width_in_cells*large_width_in_cells)]
        self.unsolved = set([(row, column) for row in range(1, large_width_in_cells+1) for column in range(1, large_width_in_cells+1)]) #TODO: should be like queue
        self.init_columnsets()
        self.init_rowsets()
        self.init_squaresets()

    def init_columnsets(self):
        for column in range(1, self.large_width_in_cells+1):
            colset = set(range(1,self.values+1))
            for row in range(1, self.large_width_in_cells+1):
                self.sets[self.index(row,column)].append(colset)

    def init_rowsets(self):
        for row in range(1, self.large_width_in_cells+1):
            rowset = set(range(1,self.values+1))
            for column in range(1, self.large_width_in_cells+1):
                self.sets[self.index(row,column)].append(rowset)

    def init_squaresets(self):
        squaresets = [set(range(1,self.values+1)) for i in range(1, self.large_width_in_small_squares*self.large_width_in_small_squares+1)]
        for row in range(1, self.large_width_in_cells+1):
            for column in range(1, self.large_width_in_cells+1):
                self.sets[self.index(row,column)].append(
                    squaresets[self.square_index(row, column)]
                )

    def square_index(self, row, column):
        return (row-1)//self.small_width_in_cells*self.large_width_in_small_squares+(column-1)//self.small_width_in_cells
        #return int(((row-1)/self.small_width_in_cells)*self.large_width_in_small_squares+(column-1)/self.small_width_in_cells)

    def index(self, row, column):
        return (row-1)*self.large_width_in_cells+(column-1)

    def setValue(self, row, column, value):
        self.matrix[self.index(row, column)] = value
        self.unsolved.remove((row,column))
        for s in self.sets[self.index(row, column)]:
            s.remove(value)

    def getValue(self, row, column):
        return self.matrix[self.index(row, column)]

    def getAllowedValues(self, row, column):
        if self.getValue(row, column):
            return set()

        return functools.reduce(lambda x,y: x.intersection(y), self.sets[self.index(row,column)])

    def showMatrix(self):
        for row in range(1, self.large_width_in_cells+1):
            print(" ".join(str(self.getValue(row, col)) for col in range(1, self.large_width_in_cells+1)))


    def solve(self):
        solvedAtLeastOnceCell = True
        while solvedAtLeastOnceCell:
            solvedAtLeastOnceCell = False
            unsolved = list(self.unsolved)
            for next_unsolved in unsolved:
                allowed = self.getAllowedValues(next_unsolved[0], next_unsolved[1])
                if len(allowed)==1:
                    self.setValue(next_unsolved[0], next_unsolved[1], allowed.pop())
                    solvedAtLeastOnceCell = True
        return len(s.unsolved)==0

if (__name__=='__main__'):
    if len(sys.argv)==4:
        (small_square_width, large_square_width, values) = (int(x) for x in sys.argv[1:])
        s = Square(small_square_width, large_square_width, values)
        r = csv.reader(sys.stdin)
        for (row, line) in enumerate(r, 1):
            for (col, field) in enumerate(line, 1):
                if field is not None and len(field)>0:
                    s.setValue(row, col, int(field))

    else:
        s = Square(2, 4, 4)
        s.setValue(1, 2, 3)
        s.setValue(1, 4, 2)
        s.setValue(2, 3, 4)
        s.setValue(3, 2, 1)
        s.setValue(4, 1, 3)
        s.setValue(4, 3, 2)
        # Correct: [4, 3, 1, 2, 1, 2, 4, 3, 2, 1, 3, 4, 3, 4, 2, 1]

    print("Solved: "+str(s.solve()))
    s.showMatrix()
