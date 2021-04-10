# -*- coding: utf-8 -*-


# imports
import gui as gui
import pygame
from controller import Controller


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls

def print_menu():
    print("")
    print("-----------MENU-----------")
    print("1.Map options:")
    print("\t11.Create a random map\n\t12.Load a map from a file\n\t13.Save the current map in a file\n\t14.Print "
          "current map")
    print("2.EA options:")
    print("\t21.Setup parameters\n\t22.Run solver\n\t23.See stats\n\t24.See drone moving on a given path")
    print("0.Exit")


def create_map(controller):
    try:
        width = int(input("Map width: "))
        height = int(input("Map height: "))
        fill = float(input("Wall probability: "))
        controller.create_map(width, height, fill)
    except ValueError:
        print("Invalid command")


def load_map(controller):
    filepath = input("Input the path to the file: ")
    controller.load_map(filepath)


def save_map(controller):
    filepath = input("Input the path to the file: ")
    controller.save_map(filepath)


def print_map(controller):
    print(str(controller.map))
    screen = gui.initPyGame(controller.get_size_of_map())
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        image = gui.image(controller.map)
        screen.blit(image, (0, 0))
        pygame.display.flip()

    pygame.quit()


def setup_parameters(controller):
    filepath = input("File path: ")

    with open(filepath, "r") as f:
        try:
            l1 = f.readline().split(",")
            x, y = int(l1[0]), int(l1[1])
            population_size = int(f.readline())
            generations = int(f.readline())
            battery = int(f.readline())

            controller.set_drone_coordinates((x, y))
            controller.set_population_size(population_size)
            controller.set_generations(generations)
            controller.set_battery(battery)
        except ValueError:
            print("Invalid file")


def runSolver(controller):
    try:
        count = int(input("Number of runs: "))
        controller.solver(count)
    except ValueError:
        print("Invalid command")


def printStats(controller):
    controller.statistics()


def seeDrone(controller):
    path = controller.get_best_path()
    gui.movingDrone(controller.map, controller.current_coordinates, path)


def run():
    running = True
    controller = Controller()

    controller.load_map("1.map")
    with open("in.txt", "r") as f:
        try:
            l1 = f.readline().split(",")
            x, y = int(l1[0]), int(l1[1])
            population_size = int(f.readline())
            generations = int(f.readline())
            battery = int(f.readline())

            controller.set_drone_coordinates((x, y))
            controller.set_population_size(population_size)
            controller.set_generations(generations)
            controller.set_battery(battery)
        except ValueError:
            print("Invalid file")

    commands = {
        11: create_map,
        12: load_map,
        13: save_map,
        14: print_map,
        21: setup_parameters,
        22: runSolver,
        23: printStats,
        24: seeDrone,
    }
    while running:
        print_menu()
        command = int(input(">>>"))
        if command in commands:
            commands[command](controller)
        elif command == 0:
            running = False
        else:
            print("Invalid command!")
