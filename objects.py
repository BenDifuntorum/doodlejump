from dataclasses import dataclass
from enum import Enum, auto
import pyxel

class Quirk(Enum):
    NONE = pyxel.COLOR_WHITE
    JUMP = pyxel.COLOR_DARK_BLUE
    BREAK = pyxel.COLOR_ORANGE
    LIFE = pyxel.COLOR_GREEN
    POINT = pyxel.COLOR_YELLOW
    DEATH = pyxel.COLOR_RED
    NULL = auto()

@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float

    @property
    def top(self):
        return self.y
    
    @property
    def bottom(self):
        return self.y + self.height
    
    @property
    def left(self):
        return self.x
    
    @property
    def right(self):
        return self.x + self.width
    
@dataclass
class Platform(Rectangle):
    def __init__(self, x: float, y: float, width: float, v_x: float = 9999, quirk: Quirk = Quirk.NULL) -> None:
        super().__init__(x, y, width, 4)
        if v_x == 9999:
            raise ValueError('Enter a proper v_x')
        
        if quirk == Quirk.NULL:
            raise ValueError('Enter a proper quirk')
        
        self.v_x: float = v_x
        self.quirk: Quirk = quirk



 