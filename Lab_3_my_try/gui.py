# -*- coding: utf-8 -*-

import pygame
import time

from domain import *


def initPyGame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePyGame():
    # closes the pygame
    running = True
    # loop for events
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    pygame.quit()


def movingDrone(currentMap, droneCoordinates, path, speed=1, markSeen=True):
    # animation of a drone on a path

    screen = initPyGame((currentMap.n * 20, currentMap.m * 20))

    drone = pygame.image.load("drona.png")

    path = [droneCoordinates] + path
    print(path)

    for i in range(len(path)):
        screen.blit(image(currentMap), (0, 0))
        current_path = [0, 0]
        for j in range(i + 1):

            if markSeen:
                brick = pygame.Surface((20, 20))
                brick.fill(GREEN)
                current_path[0], current_path[1] = (current_path[0] + path[j][0], current_path[1] + path[j][1])
                for direction in DIRECTIONS:
                    x, y = (current_path[0] + direction[0], current_path[1] + direction[1])
                    while 0 <= x < currentMap.n and 0 <= y < currentMap.m and currentMap.surface[x][y] != 1:
                        screen.blit(brick, (x * 20, y * 20))
                        x += direction[0]
                        y += direction[1]

        screen.blit(drone, (current_path[0] * 20, current_path[1] * 20))
        pygame.display.flip()
        time.sleep(2 * speed)
    closePyGame()


def image(currentMap, colour=BLUE, background=WHITE):
    # creates the image of a map

    imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
    brick = pygame.Surface((20, 20))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(currentMap.n):
        for j in range(currentMap.m):
            if currentMap.surface[i][j] == 1:
                imagine.blit(brick, (i * 20, j * 20))

    return imagine
