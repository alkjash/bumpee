# Block object stores image and position of block
import pygame

class Block:
    Basic = 1
    Engine = 2
    Left = 3
    Up = 4
    Right = 5
    Down = 6

    def __init__(self, color, block_type, x, y):
        self.color = color
        self.type = block_type
        self.x = x
        self.y = y

        # Load block type sprite
        img_path = "images/Block" + str(self.type) + ".png"
        self.img = pygame.image.load(img_path)

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

        # draw image sprite scaled to slightly inside square
        in_ratio = px_ratio * 4 / 5
        self.img = pygame.transform.scale(self.img, (in_ratio, in_ratio))
        screen.blit(self.img, (square[0] + px_ratio / 10, square[1] + px_ratio / 10))
