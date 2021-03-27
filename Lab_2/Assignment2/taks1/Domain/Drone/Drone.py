import pygame


class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def map_with_drone(self, map_image):
        drona = pygame.image.load("drona.png")
        map_image.blit(drona, (self.y * 20, self.x * 20))

        return map_image
