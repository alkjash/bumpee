# Board object stores current board state, all blocks currently on board

class Board:
    def __init__(self, width, length):
        self.w = width
        self.l = length
        self.arr = [[(0, 0) for i in range(self.w)] for j in range(self.l)]
        assert(width % 2 == 0) # board must be two equal halves

    def width(self):
        return self.w

    def length(self):
        return self.l

    def place(self, block_type, owner, x, y):
        self.arr[x][y] = (block_type, owner)
