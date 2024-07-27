import math
from math import *
from balls import *
from pygame import transform


def rotate_shooter(window, x, y, mouse_pos, image):
    run, rise = (mouse_pos[0]-x, mouse_pos[1]-y)
    angle = math.degrees(math.atan2(rise, run))

    rotimage = transform.rotate(image, -angle - 90)
    rect = rotimage.get_rect(center=(x, y))
    window.blit(rotimage, rect)


def follow_shooter(window, ball, center, distance):
    mx, my = pygame.mouse.get_pos()
    run, rise = mx - center[0], center[1] - my
    diff = sqrt(pow(run, 2) + pow(rise, 2))
    x, y = center
    if diff != 0:
        x = center[0] + run * distance / diff - ball.rect.width/2
        y = center[1] - rise * distance / diff - ball.rect.height/2
    ball.pos = x, y
    if rise > 0:
        ball.angle = -atan((pygame.mouse.get_pos()[0] - center[0])/(center[1] - pygame.mouse.get_pos()[1])) * 180 / math.pi
    elif rise < 0:
        ball.angle = -atan((pygame.mouse.get_pos()[0] - center[0])/(center[1] - pygame.mouse.get_pos()[1])) * 180 / math.pi + 180
    elif run < 0:
        ball.angle = 90
    else:
        ball.angle = 270
    ball.draw(window)


def draw_shooter(map, window, front, back, pos, speed):
    if map == 0:
        size = 112, 190
        distance = 85, -34.8
    elif map == 1:
        size = 140, 190
        distance = 100, -30
    else:
        size = 160, 150
        distance = 80, -25
    shooter = pygame.image.load("shooter " + str(map + 1) + ".png")
    shooter = transform.scale(shooter, size)
    if int(speed) == 1:
        follow_shooter(window, front, pos, distance[0])
    rotate_shooter(window, pos[0], pos[1], pygame.mouse.get_pos(), shooter)
    if int(speed) == 1:
        follow_shooter(window, back, pos, distance[1])
