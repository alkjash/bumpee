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
board = board.Board(10, 5, (black, blue, red))

# Set the height and width of the screen
# Leave one row's worth of space at bottom for text
px_ratio = 50
size=[board.width() * px_ratio, board.length() * px_ratio + px_ratio]
screen=pygame.display.set_mode(size)

pygame.display.set_caption("Bumpee")

# -------- BUILD Phase Loop -----------
# Used to manage how fast the screen updates
clock=pygame.time.Clock()

# Loop until the user clicks the close button.
done = False

# Alternate between 1 and 2
turn = 1

# Movement keys by turn
move_dict = {
        (pygame.K_w,     1) : ( 0, -1),
        (pygame.K_a,     1) : (-1,  0),
        (pygame.K_s,     1) : ( 0,  1),
        (pygame.K_d,     1) : ( 1,  0),
        (pygame.K_UP,    2) : ( 0, -1),
        (pygame.K_LEFT,  2) : (-1,  0),
        (pygame.K_DOWN,  2) : ( 0,  1),
        (pygame.K_RIGHT, 2) : ( 1,  0)
            }

# Construct a cursor block
cursor = block.Block(white, 0, 0, 0)

# construct boundary rectangle for current cursor
boundary = [0, 0, board.width() / 2, board.length()]

while done == False:
    # handle user keystroke
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        # Handle Key Press
        # If key is WASD, move Player 1's current block
        # If key is Left Shift, place Player 1's current block
        # If key is LURD, move Player 2's current block
        # If key is Enter, place Player 2's current block
        elif event.type == pygame.KEYDOWN:
            print "You pressed {0}".format(event.key)
            key = event.key
            if (key, turn) in move_dict:
                cursor.move(move_dict[(key, turn)], boundary)
            # check for end turn: move cursor and boundary accordingly
            elif (key, turn) == (pygame.K_LSHIFT, 1):
                (x, y) = cursor.pos()
                if not board.place(0, turn, x, y):
                    break
                turn = 2
                cursor = block.Block(white, 0, board.width()/2, 0)
                boundary = [board.width() / 2, 0, board.width() / 2, board.length()]
            elif (key, turn) == (pygame.K_RETURN, 2):
                (x, y) = cursor.pos()
                if not board.place(0, turn, x, y):
                    break
                turn = 1
                cursor = block.Block(white, 0, 0, 0)
                boundary = [0, 0, board.width() / 2, board.length()]

    # Set the screen background
    screen.fill(black)

    # Limit to 20 frames per second
    clock.tick(20)

    # Display should have:
    # Display blocks currently placed
    for b in board.get_blocks():
        b.draw(screen, px_ratio)

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
    c = blue
    if turn == 2:
        c = red
    pygame.draw.rect(screen, c, map(lambda x: x * px_ratio, boundary), 2)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
