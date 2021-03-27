from random import randint

from Domain.Drone import Drone
from Domain.Map import Map
from View import UI

map_maze = Map()
map_maze.load_map("test1.map")
x = randint(0, 20)
y = randint(0, 20)
d = Drone(x, y)
ui = UI.Ui(map_maze, d)

ui.run()
