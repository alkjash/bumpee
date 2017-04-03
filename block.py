# Block object stores image and position of block 
import pygame

class Block:
    def __init__(self, color, size):
        self.color = color
        self.size = size
        self.x = 0 
        self.y = 0 

    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = self.size  # distance moved in 1 frame
        if key[pygame.K_DOWN]:
            self.y += dist
        elif key[pygame.K_UP]:
            self.y -= dist
        elif key[pygame.K_RIGHT]:
            self.x += dist
        elif key[pygame.K_LEFT]:
            self.x -= dist

    def draw(self, screen):
        # draw a square with edge length size and upper left corner at (x, y)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size)) 
