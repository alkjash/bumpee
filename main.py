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

# --------- Initialize Board State ----------
pygame.init()

# Font for text
font_size = 18
myfont = pygame.font.SysFont("monospace", font_size)

# Holding down key count as repeat press every 200 ms after 500 ms delay
pygame.key.set_repeat(500, 200)

# Construct empty board object width x length
board = board.Board(14, 7, (black, blue, red))

# Set the height and width of the screen
# Leave one row's worth of space at bottom for text
px_ratio = 50
size=[board.width() * px_ratio, board.length() * px_ratio + px_ratio]
screen=pygame.display.set_mode(size)

pygame.display.set_caption("Bumpee")

# -------- BUILD Phase Loop -----------
# Used to manage how fast the screen updates
clock=pygame.time.Clock()

# Loop until the user clicks the close button
# or all blocks are placed
done = False

# Alternate between 1 and 2
turn = 1

# construct boundary rectangle for current cursor
boundary = [0, 0, board.width() / 2, board.length()]

# Queue of blocks to place
block_Q = [
        block.Block.Engine,
        block.Block.Left,
        block.Block.Up,
        block.Block.Right,
        block.Block.Down,
        block.Block.Basic,
        block.Block.Basic,
        block.Block.Basic,
        block.Block.Basic,
        block.Block.Basic,
          ]
cur_block = 0

# Construct a cursor block
cursor = block.Block(white, block_Q[cur_block], 0, 0)

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
                (x, y) = (cursor.x, cursor.y)
                if not board.place(block_Q[cur_block], turn, x, y):
                    break
                turn = 2
                cursor = block.Block(white, block_Q[cur_block], board.width()/2, 0)
                boundary = [board.width() / 2, 0, board.width() / 2, board.length()]
            elif (key, turn) == (pygame.K_RETURN, 2):
                (x, y) = (cursor.x, cursor.y)
                if not board.place(block_Q[cur_block], turn, x, y):
                    break
                turn = 1

                cur_block += 1
                if cur_block >= len(block_Q):
                    done = True
                else:
                    cursor = block.Block(white, block_Q[cur_block], 0, 0)
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
    # Cursor should blink on top of current block
    if pygame.time.get_ticks() % 1000 < 600:
        cursor.draw(screen, px_ratio)

    # Text command below
    command = "BUILD PHASE: Player " + str(turn)
    text = myfont.render(command, 1, white)
    screen.blit(text, (0, board.length() * px_ratio))
    command = "Use "
    if turn == 1:
        command += "WASD to move, L-Shift to confirm"
    if turn == 2:
        command += "Arrow Keys to move, Enter to confirm"
    text = myfont.render(command, 1, white)
    screen.blit(text, (0, board.length() * px_ratio + font_size))

    # Draw boundary around half of grid currently in use
    if turn == 1:
        c = blue
    elif turn == 2:
        c = red
    pygame.draw.rect(screen, c, map(lambda x: x * px_ratio, boundary), 2)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
if cur_block < len(block_Q):
    pygame.quit()

print "BUILD PHASE OVER!"
# -------- BUMP Phase Loop -----------
print "BUMP PHASE START!"

done = False

# direction that current move is in
cur_move = (0, 0)

# boundary set now to size of whole board
boundary = (0, 0, board.width(), board.length())

while done == False:
    # Handle user keystroke
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        # Handle Key Press
        # If key is WASD, move Player 1's entire car
        # If key is Left Shift, confirm Player 1's move
        # If key is LURD, move Player 2's entire car
        # If key is Enter, confirm Player 2's move
        elif event.type == pygame.KEYDOWN:
            print "You pressed {0}".format(event.key)
            key = event.key
            if (key, turn) in move_dict:
                next_move = move_dict[(key, turn)]
                # check that move is valid (i.e. have that motor block)
                valid = False
                for b in board.get_blocks():
                    if (b.color, turn) in [(blue, 1), (red, 2)] and (next_move, b.type) in [
                            ((1, 0), block.Block.Right),
                            ((-1, 0), block.Block.Left),
                            ((0, 1), block.Block.Down),
                            ((0, -1), block.Block.Up)]:
                        valid = True
                        break
                if valid:
                    cur_move = next_move
            # check for end turn: move car accordingly
            elif (key, turn) in [(pygame.K_LSHIFT, 1),
                                 (pygame.K_RETURN, 2)]:
                # move all blocks moved
                blocks = board.get_blocks()
                for b in blocks:
                    if (b.color, turn) in [(blue, 1), (red, 2)]:
                        b.x += cur_move[0]
                        b.y += cur_move[1]
                # handle collisions (with walls and other blocks)
                remove = [False for b in blocks]
                for i in range(len(blocks)):
                    b = blocks[i]
                    if b.x < boundary[0]:
                        remove[i] = True
                    elif b.y < boundary[1]:
                        remove[i] = True
                    elif b.x >= boundary[2] + boundary[0]:
                        remove[i] = True
                    elif b.y >= boundary[3] + boundary[1]:
                        remove[i] = True
                    for j in range(i+1, len(blocks)):
                        b1 = blocks[j]
                        if (b1.x, b1.y) == (b.x, b.y):
                            remove[i] = True
                            remove[j] = True
                blocks = [blocks[i] for i in range(len(blocks)) if not remove[i]]
                # check win condition
                win = 3
                for b in blocks:
                    if (b.color, b.type) == (blue, block.Block.Engine):
                        win -= 2
                    elif (b.color, b.type) == (red, block.Block.Engine):
                        win -= 1
                if win > 0:
                    done = True
                    if win == 3:
                        print "Tie!"
                    else:
                        print "Winner is " + str(win)

                turn = turn % 2 + 1
                cur_move = (0, 0)

    # Set the screen background
    screen.fill(black)

    # Limit to 20 frames per second
    clock.tick(20)

    # Display should have:
    # Display previous car position
    for b in board.get_blocks():
        b.draw(screen, px_ratio)

    # Display blinking copy of car moved in cur_move direction
    if pygame.time.get_ticks() % 1000 < 600:
        for b in board.get_blocks():
            if (b.color, turn) in ((blue, 1), (red, 2)):
                b_moved = block.Block(white,
                                    b.type,
                                    b.x + cur_move[0],
                                    b.y + cur_move[1])
                # check within bounds
                if b.x < boundary[0]:
                    continue
                elif b.y < boundary[1]:
                    continue
                elif b.x >= boundary[2] + boundary[0]:
                    continue
                elif b.y >= boundary[3] + boundary[1]:
                    continue
                b_moved.draw(screen, px_ratio)

    # Text command below
    command = "BUMP PHASE: Player " + str(turn)
    text = myfont.render(command, 1, white)
    screen.blit(text, (0, board.length() * px_ratio))
    command = "Use "
    if turn == 1:
        command += "WASD to move, L-Shift to confirm"
    if turn == 2:
        command += "Arrow Keys to move, Enter to confirm"
    text = myfont.render(command, 1, white)
    screen.blit(text, (0, board.length() * px_ratio + font_size))

    # Draw boundary around half of grid currently in use
    if turn == 1:
        c = blue
    elif turn == 2:
        c = red
    pygame.draw.rect(screen, c, map(lambda x: x * px_ratio, boundary), 2)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
