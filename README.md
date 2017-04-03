# Bumpee

Simple 2D 2-player game.

Build phase: take turns placing blocks on your half of the 5x10 board

Blocks: Engine Block, 4 Motor Blocks (Left, Up, Right, Down), 5 Basic Blocks

Bump phase: take turns moving in a single valid direction (valid if your motor block in that direction is left)
When two blocks collide, or when a block collides with a wall, all involved blocks are destroyed. 
Blocks disconnected from your engine are destroyed.
Must move every turn unless all Motor Blocks destroyed.

Last player with engine wins.
