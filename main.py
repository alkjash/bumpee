#! /usr/bin/env python
import pygame
import board

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)


# --------- Initialize Board State ----------
pygame.init()

# Construct empty board object width x length
board = board.Board(10, 5)

# Set the height and width of the screen
px_ratio = 50
size=[board.length() * px_ratio, board.width() * px_ratio]
screen=pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# -------- BUILD Phase Loop -----------
# Used to manage how fast the screen updates
clock=pygame.time.Clock()

#Loop until the user clicks the close button.
done = False

while done == False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            print "You pressed {0}".format(event.key)
        elif event.type == pygame.KEYUP:
            print "You released {0}".format(event.key)
    # Set the screen background
    screen.fill(black)

    # Limit to 20 frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
