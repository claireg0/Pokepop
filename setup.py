import pygame
from pygame import *
from pygame.image import load

pygame.init()
clock = time.Clock()

# setting up window size
WIN_X = int(1000)

# how tall the screen is going to be
WIN_Y = int(750)

# set the screen
window = pygame.display.set_mode((WIN_X, WIN_Y))

# lists of animations for level selection
map1_animation = []
map2_animation = []
map3_animation = []

for i in range(1, 5):
    map1_animation.append(transform.scale(load("level animation/leaf" + str(i) + ".png"), (80, 110)))
    map2_animation.append(transform.scale(load("level animation/cactus" + str(i) + ".png"), (100, 120)))
for i in range(1, 9):
    map3_animation.append(transform.scale(load("level animation/cube" + str(i) + ".png"), (100, 103)))

animations = [map1_animation, map2_animation, map3_animation]

red = 255, 0, 0
blue = 0, 0, 255
black = 0, 0, 0
colours = [red, blue, black]

index=0
image=map1_animation[0]
numbers=[]
for i in range(1,7):
    numbers.append(transform.scale(load("level animation/Level " + str(i) + ".png"), (25, 50)))

signs = []
for i in range(1, 4):
    signs.append(load("choose maps/" + str(i) + ".png"))

sign_pos = [[280, 300], [700, 300], [500, 550]]
sign_size = [[230, 160], [232, 129], [204, 235]]

back_button = load("button/back.png")
back_button = transform.scale(back_button, (75, 75))
