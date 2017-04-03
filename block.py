# Block object stores image and position of block
import pygame

class Block:
    def __init__(self, color, block_type, x, y):
        self.color = color
        self.type = block_type
        self.x = x
        self.y = y

    def move(self, d, boundary):
        self.x += d[0]
        self.y += d[1]
        # move back within bounds if went out
        if self.x < boundary[0]:
            self.x = boundary[0]
        elif self.y < boundary[1]:
            self.y = boundary[1]
        elif self.x >= boundary[2] + boundary[0]:
            self.x = boundary[2] + boundary[0] - 1
        elif self.y >= boundary[3] + boundary[1]:
            self.y = boundary[3] + boundary[1] - 1

    def pos(self):
        return (self.x, self.y)

    # only function in Block that knows about pixels
    def draw(self, screen, px_ratio):
        # draw a square with edge length size and upper left corner at (x, y)
        square = map(lambda x: x * px_ratio, [self.x, self.y, 1, 1])
        pygame.draw.rect(screen, self.color, square)
