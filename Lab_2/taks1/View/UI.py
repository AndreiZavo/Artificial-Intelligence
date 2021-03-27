from random import randint

import pygame
import time

from Controller.Controller import Controller
from Domain.Settings import *


class Ui:
    def __init__(self, m, d):
        self._controller = Controller(m, d)

    @staticmethod
    def display_with_path(image, path1, path2):
        mark_a = pygame.Surface((20, 20))
        mark_c = pygame.Surface((20, 20))
        mark_g = pygame.Surface((20, 20))
        mark_a.fill(GREEN)
        mark_c.fill(YELLOW)
        mark_g.fill(RED)
        for move in path1:
            if move in path2:
                mark = mark_c
            else:
                mark = mark_a
            image.blit(mark, (move[1] * 20, move[0] * 20))
        list_pos = []
        for pos in path2:
            if pos not in path1:
                list_pos.append(pos)
        for move in list_pos:
            image.blit(mark_g, (move[1] * 20, move[0] * 20))
        return image

    def run(self):
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        # we position the drone somewhere in the area

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(WHITE)

        # define a variable to control the main loop
        running = True

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

            screen.blit(self._controller.d.map_with_drone(self._controller.m.image()), (0, 0))
            pygame.display.flip()

        fx = randint(0, 19)
        fy = randint(0, 19)
        while fx == self._controller.d.x and fy == self._controller.d.y:
            fx = randint(0, 19)
            fy = randint(0, 19)

        start1 = time.time()
        path1 = self._controller.a_star_search(self._controller.d.x, self._controller.d.y, fx, fy)
        end1 = time.time()
        print(end1 - start1)

        start2 = time.time()
        path2 = self._controller.greedy_search(self._controller.d.x, self._controller.d.y, fx, fy)
        end2 = time.time()
        print(end2 - start2)

        screen.blit(self.display_with_path(self._controller.m.image(), path1, path2), (0, 0))

        pygame.display.flip()
        time.sleep(15)
        pygame.quit()
