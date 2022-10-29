# this is the main file for the project - put your code here

# This code creates the different tetris shapes
class shapes:
    x = 0
    y = 0

    shapes = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], # line
        [4, 5, 8, 9], # square
        [[2, 6, 5, 9], [1, 5, 6, 10]], # vertical z
        [[2, 3, 5, 6], [1, 2, 6, 7]], # z shape
        [[4, 5, 6, 9], [1, 4, 5, 6], [1, 5, 9, 6], [1, 4, 5, 9]], # T shape
        [[0, 4, 8, 9], [1, 5, 9, 8], [4, 0, 1, 2], [6, 2, 1, 0]] # L shape
    ]

print("hello world")
