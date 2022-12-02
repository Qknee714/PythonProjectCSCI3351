import pygame
import random

# block colors represent different kinds of trash
colors = [
    "Teal", "Dim Grey", "Dark Red", "Dark Blue", "Dark Green", "Golden Rod"
]


class Block:
    # every block has its own shape, color, and position

    x = 0
    y = 0

    # each shape is represented in a 4x4 square indexed 0-15
    shapes = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],                                  # line
        [[4, 5, 9, 10], [2, 6, 5, 9]],                                  # z
        [[6, 7, 9, 10], [1, 5, 6, 10]],                                 # s
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],      # backwards L
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],    # L
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],       # T
        [[1, 2, 5, 6]],                                                 # square
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.shapes) - 1)     # selects a random shape for the block
        self.color = random.randint(1, len(colors) - 1)         # selects a random color
        self.rotation = 0

    def image(self):
        return self.shapes[self.type][self.rotation]

    def rotate(self):
        # image() will return the next rotation of the block in the shapes list
        self.rotation = (self.rotation + 1) % len(self.shapes[self.type])


class Tetris:
    block = None
    level = 2   # determines the difficutly / how fast the blocks fall
    score = 0
    state = "start"
    field = []  # represents the playing field in height x width
    height = 0
    width = 0

    x = 100     # the x position of the top left corner of the grid
    y = 50      # the y position of the top left corner of the grid
    zoom = 40   # how big the grid is

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"

        # following loops create the playing field in height x width
        for i in range(height):
            # for the height of the playing field
            new_line = []   # new list of tiles

            for j in range(width):
                # for the width of the playing field
                new_line.append(0)  # 0 represents an unfilled tile

            self.field.append(new_line)     # adds the line to the playing field

    def new_block(self):
        # generates a new block, x parameter should be changed if the field size is changed
        self.block = Block(3, 0)   # the block is 3 tiles from the left, top row

    def intersects(self):
        # checks if the current block intersectis with a fixed block

        intersection = False

        # iterate through the 4x4 space the block is represented in
        for i in range(4):      # i is the row
            for j in range(4):  # j is the column

                if i * 4 + j in self.block.image():
                    # if that tile is part of the current block

                    if i + self.block.y > self.height - 1 or \
                            j + self.block.x > self.width - 1 or \
                            j + self.block.x < 0 or \
                            self.field[i + self.block.y][j + self.block.x] > 0:
                        # there is an intersection if the block reaches the bottom,
                        # the block reaches the right wall,
                        # the block reaches the left wall,
                        # or if the block's position contacts a filled tile
                        intersection = True

        return intersection

    def freeze(self):
        # set the block in place when it reaches the bottom

        # iterate through the 4x4 space the block is represented in
        for i in range(4):      # i is the row
            for j in range(4):  # j is the column

                if i * 4 + j in self.block.image():
                    # if that tile is part of the current block
                    # set that block as a filled tile in the playing field
                    self.field[i + self.block.y][j + self.block.x] = self.block.color

        self.break_lines()      # check for full lines
        self.new_block()        # make a new block

        if self.intersects():
            # if the new block intersects, the game is over
            self.state = "gameover"

    def break_lines(self):
        # checks for full lines in the playing field

        lines = 0

        for i in range(1, self.height):
            # loop through every row from top to bottom

            zeros = 0

            for j in range(self.width):
                # loop through every tile in the row
                if self.field[i][j] == 0:
                    # if there is a zero in the row, the line is not full
                    zeros += 1

            if zeros == 0:
                # if the line has no empty tiles
                lines += 1

                for i1 in range(i, 1, -1):          # from the row thats being destroyed to the top
                    for j in range(self.width):     # for every tile in the row
                        # fill that tile with the tile above it
                        self.field[i1][j] = self.field[i1 - 1][j]

        self.score += lines ** 2

    def go_space(self):
        # immediate brings the block to the bottom
        while not self.intersects():
            # lowers the block's position until it reaches the bottom
            self.block.y += 1

        # raise the block by 1 to freeze it in bounds
        self.block.y -= 1
        self.freeze()

    def go_down(self):
        # lower the block by 1
        self.block.y += 1

        if self.intersects():
            # if it intersects, raise it by 1 to freeze it in bounds
            self.block.y -= 1
            self.freeze()

    def go_side(self, dx):
        # move the block left or right

        old_x = self.block.x    # save the blocks current x position
        self.block.x += dx      # move the block by the specified increment

        if self.intersects():
            # if the block intersects, move it back
            self.block.x = old_x

    def rotate(self):
        # rotate the block

        old_rotation = self.block.rotation  # save the current rotation
        self.block.rotate()

        if self.intersects():
            # if the block intersects, rotate it back
            self.block.rotation = old_rotation


# initialize game engine
pygame.init()

# size of the screen
size = (1200, 900)    # x, y
screen = pygame.display.set_mode(size)

# background image
bg = pygame.image.load('bg.jpg')    # image needs to be in same directory as main

# window title
pygame.display.set_caption("Recycle Tetris")

# loop until the user clicks the close button
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)   # size of the playing field in height x width
counter = 0

pressing_down = False

while not done:

    # background settings
    screen.fill("Black")       # background color
    screen.blit(bg, (0, 0))       # background image

    if game.block is None:
        # make a new block if there isn't one
        game.new_block()

    # constantly increment the counter
    counter += 1
    if counter > 100000:
        counter = 0

    # drops the block every 25/2/2 = 6 ticks
    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    # event handling for the game
    for event in pygame.event.get():

        # ends the game when the window is closed
        if event.type == pygame.QUIT:
            done = True

        # keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:        # up arrow = rotate
                game.rotate()
            if event.key == pygame.K_DOWN:      # down arrow = go down
                pressing_down = True
            if event.key == pygame.K_LEFT:      # left arrow = go left
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:     # right arrow = go right
                game.go_side(1)
            if event.key == pygame.K_SPACE:     # space = drop to bottom
                game.go_space()
            if event.key == pygame.K_ESCAPE:    # escape = restart game
                game.__init__(20, 10)

        # reverts pressing_down if the down arrow key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    # draws the game board
    for i in range(game.height):
        for j in range(game.width):

            # draws the grid
            pygame.draw.rect(screen, "Teal", [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)

            # draws the filled tiles
            if game.field[i][j] > 0:
                pygame.draw.rect(
                    screen, colors[game.field[i][j]],
                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1]
                )

    # draws the current block
    if game.block is not None:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in game.block.image():
                    pygame.draw.rect(screen, colors[game.block.color],
                                     [game.x + game.zoom * (j + game.block.x) + 1,
                                      game.y + game.zoom * (i + game.block.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    # font settings
    font = pygame.font.SysFont('Courier New', 25, True, False)
    font1 = pygame.font.SysFont('Courier New', 30, True, False)     # bigger than other font

    # text settings
    score_text = font1.render("Recycled: " + str(game.score), True, "White")
    text_game_over = font.render("Congratulations, you recycled:", True, "White")
    text_game_over3 = font.render("Try again! You recycled:", True, "White")
    text_game_over1 = font.render("        " + str(game.score) + " Pounds of Plastic!", True, "White")
    text_game_over2 = font.render("Press ESC to try again.", True, "White")

    # set text to screen
    screen.blit(score_text, [100, 10])   # current score

    # displays gameover text
    if game.state == "gameover":

        if game.score < 1:
            # bad ending if score is 0
            screen.blit(text_game_over3, [550, 60])
        else:
            screen.blit(text_game_over, [550, 60])
        screen.blit(text_game_over1, [550, 100])
        screen.blit(text_game_over2, [550, 140])

    pygame.display.flip()   # refreshes the screen
    clock.tick(fps)         # determines speed of game

pygame.quit()
