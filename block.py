# Block object stores image and position of block
import pygame

class Block:
    def __init__(self, color, block_type, x, y):
        self.color = color
        self.type = block_type
        self.x = x
        self.y = y

    def handle_keys(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            self.y += 1
        elif key[pygame.K_UP]:
            self.y -= 1
        elif key[pygame.K_RIGHT]:
            self.x += 1
        elif key[pygame.K_LEFT]:
            self.x -= 1

    def draw(self, screen, px_ratio):
        # draw a square with edge length size and upper left corner at (x, y)
        square = map(lambda x: x * px_ratio, [self.x, self.y, 1, 1])
        pygame.draw.rect(screen, self.color, square)
