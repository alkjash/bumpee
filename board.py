# Board object stores current board state, all blocks currently on board
import pygame
import block

adj = {(0, 1), (0, -1), (1, 0), (-1, 0)}

class Board:
    def __init__(self, width, length, colors):
        self.w = width
        self.l = length
        self.colors = colors
        self.blocks = []
        assert(width % 2 == 0) # board must be two equal halves

    def width(self):
        return self.w

    def length(self):
        return self.l

    def place(self, block_type, owner, x, y):
        # Check if block conflicts
        for b in self.blocks:
            if (b.x, b.y) == (x, y):
                return False

        # Check that non-engine block is adjacent to some block of same owner
        if block_type != block.Block.Engine:
            adjacent = False
            for b in self.blocks:
                if (b.x - x, b.y - y) in adj:
                    adjacent = True
            if not adjacent:
                return False

        # Construct and add block to block list
        b = block.Block(self.colors[owner], block_type, x, y)
        self.blocks.append(b)
        return True

    def get_blocks(self):
        return self.blocks
