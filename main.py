#! /usr/bin/env python
import pygame
import board
import block

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)

# --------- Initialize Board State ----------
pygame.init()

# Font for text
font_size = 18
myfont = pygame.font.SysFont("monospace", font_size)

# Holding down key count as repeat press every 200 ms after 500 ms delay
pygame.key.set_repeat(500, 200)

# Construct empty board object width x length
board = board.Board(10, 5, (black, red, blue))

# Set the height and width of the screen
# Leave one row's worth of space at bottom for text
px_ratio = 50
size=[board.width() * px_ratio, board.length() * px_ratio + px_ratio]
screen=pygame.display.set_mode(size)

# Construct a cursor block
cursor = block.Block(white, 0, 0, 0)

pygame.display.set_caption("Bumpee")

# -------- BUILD Phase Loop -----------
# Used to manage how fast the screen updates
clock=pygame.time.Clock()

# Loop until the user clicks the close button.
done = False

# Alternate between 1 and 2
turn = 1

# test
board.place(1, 1, 3, 2)
board.place(1, 2, 2, 1)

while done == False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            print "You pressed {0}".format(event.key)
            cursor.handle_keys()
            # Handle Key Press
            # If key is WASD, move Player 1's current block
            # If key is Left Shift, place Player 1's current block
            # If key is LURD, move Player 2's current block
            # If key is Enter, place Player 2's current block

    # Set the screen background
    screen.fill(black)

    # Limit to 20 frames per second
    clock.tick(20)

    # Display should have:
    # Display blocks currently placed
    for block in board.get_blocks():
        block.draw(screen, px_ratio)

    # Display white "cursor" block
    cursor.draw(screen, px_ratio)

    # Text command below
    command = "BUILD PHASE: Player " + str(turn)
    text = myfont.render(command, 1, white)
    screen.blit(text, (0, board.length() * px_ratio))
    command = "Use "
    if turn == 1:
        command += "WASD to move and L-Shift to confirm"
    if turn == 2:
        command += "Arrow Keys to move and Enter to confirm"
    text = myfont.render(command, 1, white)
    screen.blit(text, (0, board.length() * px_ratio + font_size))

    # Draw boundary around half of grid currently in use
    rect = [0, 0, board.width() / 2 * px_ratio, board.length() * px_ratio]
    if turn == 2:
        rect[0] += board.width() / 2 * px_ratio
    pygame.draw.rect(screen, red, rect, 2)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
