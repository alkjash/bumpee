# Block object stores image and position of block
import pygame

class Block:
    def __init__(self, color, block_type, x, y):
        self.color = color
        self.type = block_type
        self.x = x
        self.y = y

    def move(self, d):
        self.x += d[0]
        self.y += d[1]

    # only function in Block that knows about pixels
    def draw(self, screen, px_ratio):
        # draw a square with edge length size and upper left corner at (x, y)
        square = map(lambda x: x * px_ratio, [self.x, self.y, 1, 1])
        pygame.draw.rect(screen, self.color, square)
