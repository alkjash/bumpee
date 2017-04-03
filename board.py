# Board object stores current board state, all blocks currently on board
import pygame
import block

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
        for b in self.blocks:
            if b.pos() == (x, y):
                return False
        b = block.Block(self.colors[owner], block_type, x, y)
        self.blocks.append(b)
        return True

    def get_blocks(self):
        return self.blocks
