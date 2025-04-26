from game import Model, View, Controller
from enum import Enum
import pyxel

class Specs(Enum):
    FPS = 60
    WIDTH = 500
    HEIGHT = 1000


if __name__ == "__main__":
    
    model = Model(fps=Specs.FPS.value, width=Specs.WIDTH.value, height=Specs.HEIGHT.value)
    view = View()
    controller = Controller(model, view)

    pyxel.run(controller.update, controller.draw)