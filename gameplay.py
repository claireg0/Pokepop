# https://stackoverflow.com/questions/70419688/find-size-of-rotated-rectangle-that-covers-orginal-rectangle

import pygame.draw
from pygame.image import load
from pygame.time import wait
import balls
from main import try_exit
from main import aftergame
from lines import *
from shooter import *
from balls import *


def find_length(ball_list, count, push, toadd):
    start, end = count, count
    while start > 0 and ball_list[start].type == ball_list[start - 1].type and (ball_list[start].move ==
            ball_list[start - 1].move or dist(ball_list[start].pos, ball_list[start - 1].pos) <= 30):
        start -= 1
    while end < len(ball_list) - 2 and ball_list[end].type == ball_list[end + 1].type and (ball_list[end].move ==
            ball_list[end + 1].move or dist(ball_list[end].pos, ball_list[end + 1].pos) <= 30):
        end += 1
    if end == toadd - 1 and ball_list[toadd].type == ball_list[count].type:
        end += 1
    if end == toadd and push == ball_list[start].type:
        end += 1
    return start, end


def find_stopped(ball_list, start):
    while start + 1 < len(ball_list) and not ball_list[start + 1].move and dist(ball_list[start].pos, ball_list[start + 1].pos) <= 30:
        start += 1
    return start


def game(map, level):
    ball_list = generate_ball(level, map)  # randomly generate a list of balls
    front = pokeballs(pick_ball(), -30, -30, 0, 0, 0)  # front ball on shooter
    back = pokeballs(pick_ball(), -30, -30, 0, 0, 0)  # second shooter ball
    shooter_pos = [[500, 450], [500, 640], [280, 460]]  # the center for shooters on different maps
    fly = []  # to store balls shot out
    speedup = False  # if the ball touches the end and speed up to leave
    speed = 6  # the number of times moving the ball
    add_index = -1
    ingame = True
    win = False
    change_move = map1
    if map == 1:
        change_move = map2
    elif map == 2:
        change_move = map3

    while ingame:
        if len(ball_list) == 0:
            ingame = False
            win = True
            print("you win")
        elif (ball_list[len(ball_list) - 1].x_move + ball_list[len(ball_list) - 1].y_move == 0):
            ingame = False
            win = False

        push = -1  # the ball type to add at the end of the list
        clock.tick(60)
        start, end = 0, 0
        # the bottom background
        window.blit(load("backgrounds/" + str(map) + "a.png"), (0, 0))
        # move the balls along the path, detect collision
        for count in range(len(ball_list)):
            ball = ball_list[count]
            length = len(ball_list)
            ball.rect.topleft = ball.pos
            # balls off the path at the start
            if ball.pos[0] < 100 and ball.pos[1] <= 200:
                for _ in range(int(speed)):
                    ball.shooter_move(True)
                ball.rotate = ball_list[count - 1].rotate
            else:
                balls.balls_exist.add(ball.type)
                pos = ball.pos[0] + 15, ball.pos[1] + 15
                for flying in fly:
                    angle = flying.angle
                    half = 15 * (abs(cos(angle)) + abs(sin(angle)))  # reference
                    center = (flying.pos[0] + half, flying.pos[1] + half)
                    if dist(pos, center) <= 30:
                        notmove = find_stopped(ball_list, count)
                        if ball.move or dist(ball_list[notmove].pos, ball_list[notmove + 1].pos) <= 60:
                            add_index = length - 1
                        else:
                            add_index = notmove
                        push = ball_list[add_index].type
                        for i in range(add_index, count, -1):
                            ball_list[i].type = ball_list[i - 1].type
                        ball_list[count].type = flying.type
                        fly.remove(flying)
                        start, end = find_length(ball_list, count, push, add_index)
                        break
                if ball.move:
                    for _ in range(int(speed)):
                        speedup = change_move(ball, speedup)
                        ball.shooter_move(True)
                elif count + 1 == length or (ball_list[count + 1].move and dist(ball_list[count + 1].pos, ball.pos) <= 30):
                    for j in range(count, -1, -1):
                        if j + 1 == length or dist(ball_list[j].pos, ball_list[j + 1].pos) <= 30:
                            ball_list[j].move = True
                        else:
                            break
                ball.draw(window)

        if speedup:
            speed += 0.2
        elif int(speed) > 1 and not speedup:
            speed -= 0.1

        if push > -1:
            last = ball_list[add_index]
            x, y = last.pos
            x -= 30 * last.x_move / last.speed
            y -= 30 * last.y_move / last.speed
            new_ball = pokeballs(push, x, y, last.rotate, last.x_move, last.y_move)
            new_ball.road_h, new_ball.road_v = last.road_h, last.road_v
            new_ball.speed, new_ball.move, new_ball.angle = last.speed, last.move, last.angle
            new_ball.draw(window)
            ball_list.insert(add_index + 1, new_ball)

        window.blit(load("backgrounds/" + str(map) + "b.png"), (0, 0))

        if end - start + 1 >= 3:
            # deleted = ball_list[start].type
            # balls_exist.remove(ball_list[start].type)
            if end != len(ball_list) - 1:
                for i in range(0, start):
                    ball_list[i].move = False
            for i in range(start, end + 1):
                ball_list.remove(ball_list[start])

        for event in pygame.event.get():
            try_exit(event)
            if event.type == pygame.MOUSEBUTTONUP and int(speed) == 1:
                run, rise = (front.pos[0] + 14 - shooter_pos[map][0], front.pos[1] + 15 - shooter_pos[map][1])
                diff = sqrt(pow(run, 2) + pow(rise, 2))
                fly.append(front)
                fly[len(fly) - 1].x_move = run / diff * 20
                fly[len(fly) - 1].y_move = rise / diff * 20
                front = back
                back = pokeballs(pick_ball(), 0, 0, 0, 0, 0)

        if not fly == []:
            out = 0
            for ball in fly:
                if not (0 - 30 < ball.pos[0] < WIN_X and -30 < ball.pos[1] < WIN_Y):
                    out = ball
                ball.shooter_move()
                ball.draw(window)
            if out != 0:
                fly.remove(out)
        window.blit(load("backgrounds/" + str(map) + "c.png"), (0, 0))
        front.type = pick_ball(front.type)
        back.type = pick_ball(back.type)
        draw_shooter(map, window, front, back, shooter_pos[map], speed)
        balls.balls_exist = set()
        pygame.display.update()
    aftergame(win, map, level)
