# this is the main file for the project - put your code here

import random
import pygame


class Block:
    # attributes of the block in game

    x = 0
    y = 0

    shapes = [
        # every shape in a 4x4 grid indexed 0-15
        # same line is different orientations of the same shape

        [[1, 5, 9, 13], [4, 5, 6, 7]],  # line
        [4, 5, 8, 9],   # square
        [[2, 6, 5, 9], [1, 5, 6, 10]],  # vertical z
        [[2, 3, 5, 6], [1, 2, 6, 7]],   # z shape
        [[4, 5, 6, 9], [1, 4, 5, 6], [1, 5, 9, 6], [1, 4, 5, 9]],   # T shape
        [[0, 4, 8, 9], [1, 5, 9, 8], [4, 0, 1, 2], [6, 2, 1, 0]]    # L shape
    ]

    colors = [
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
    ]

    def __init__(self, x, y):
        # picks a random shape and color for the block
        self.x = x
        self.y = y
        self.shape = random.randint(0, len(self.shapes) - 1)    # random shape
        self.color = random.randint(0, len(self.colors) - 1)    # random color
        self.orientation = 0   # orientation of the block

    def rotate(self):
        # rotates the block
        self.orientation = (self.orientation + 1) % len(self.shapes[self.shape])

    def image(self):
        # returns the shape and orientation of the block
        return self.shapes[self.shape][self.orientation]
    
class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_Block(self):
        self.figure = Block(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_Block()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
Green = (0, 150, 0)

size = (700, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Recycle Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_Block()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill("Light Green")

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, BLACK, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Times New Roman', 25, True, False)
    font1 = pygame.font.SysFont('Times New Roman', 25, True, False)
    text = font.render("Pounds of plastic: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Congratulations you recycled: " + str(game.score) + " Pounds of Plastic!", True, (0, 0, 0))
    text_game_over1 = font1.render("Press ESC to try again", True, (0, 0, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
