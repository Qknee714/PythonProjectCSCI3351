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
        # add colors later
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


print("this is our project")
