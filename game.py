from enum import Enum, auto
from physics_engine.physics import PhysicsModel
from physics_engine.physics_types import Ball, Surface
from objects import Platform, Quirk

import random as r
import pyxel


class GameState(Enum):
    """Game state for the game."""
    START = auto()
    PLAYING = auto()
    END = auto()
    PAUSE = auto()



class Model(PhysicsModel):
    def __init__(self, fps: int, width: int, height: int):
        super().__init__(fps, width, height)
        self.start_game()
        self._platform_list: list[Platform] = [
            Platform(x=width//2, y=height-200, width=150, v_x=0, quirk=Quirk.NONE),
            Platform(x=width//2, y=height-400, width=150, v_x=0, quirk=Quirk.NONE),
        ]
        self._points: int = 0

        pyxel.init(width, height, fps=fps, title='DOODLEJUMP')
        pyxel.mouse(True)


    def _init_ball(self):
        self._ball = Ball(
            x=self._width//2, 
            y=self._height-600, 
            v_x=0, 
            v_y=0, 
            a_x=0, 
            a_y=self._gravity,
            radius=5, 
            )
        
    def start_game(self):
        self._game_state = GameState.START

    def play_game(self):
        self._game_state = GameState.PLAYING

    def pause_game(self):
        self._game_state = GameState.PAUSE
        

    @property
    def game_state(self):
        return self._game_state

    @property
    def platform_list(self):
        return self._platform_list
    
    def check_collision(self):
        for key, platform in enumerate(self._platform_list):
            if (((self._ball.bottom >= platform.top >= self._ball.bottom - self._ball.v_y) 
                or (self._ball.top >= platform.bottom >= self._ball.top + self._ball.v_y)) 
                and platform.left < self._ball.x < platform.right 
                and self._ball.v_y > 0):
                col_p = self._platform_list.pop(key)
                return col_p

    @property        
    def closest_surface(self) -> Surface:
        dist = self.ball_dist_from_next_surface
        if self._platform_list
        if dist == self._ball.left-0:
            return Surface.LEFT

        elif dist == self._width-self._ball.right:
            return Surface.RIGHT

        elif dist == self._ball.top-0:
            return Surface.TOP

        else:
            assert dist == self._height-self._ball.bottom
            return Surface.BOTTOM
    
    def platform_collision(self):
        

    def quirk_release(self, quirk: Quirk):
        match quirk:
            case Quirk.NONE:
                pass
            
            case Quirk.JUMP:
                self._ball.v_y = -2 * self._ball.v_y
            
            case Quirk.BREAK:
                self._platform_list.pop()
            
            case Quirk.LIFE:
                self._ball.v_y = -self._ball.v_y
            
            case Quirk.POINT:
                self._points += 1500

            case Quirk.DEATH:
                self._game_state = GameState.END

            case _:
                pass

    def _generate_platform(self, quirk: Quirk) -> Platform:
        """Generate a platform with random position and velocity."""

        match quirk:
            case Quirk.NONE:
                v_x = r.uniform(-1, 1)
            
            case Quirk.JUMP:
                v_x = r.choice([r.uniform(-2, -1), r.uniform(1, 2)])
            
            case Quirk.BREAK:
                v_x = r.uniform(-1, 1)
            
            case Quirk.LIFE:
                v_x = r.choice([r.uniform(-2, -1), r.uniform(1, 2)])
            
            case Quirk.POINT:
                v_x = r.choice([r.uniform(-3, -2), r.uniform(2, 3)])

            case Quirk.DEATH:
                v_x = r.uniform(-1, 1)

            case _:
                raise ValueError('Invalid quirk type')

        last_platform: Platform = self._platform_list[-1]

        x: float = r.randint(50, self._width - 50)
        return Platform(x=x, y=last_platform.y-200, width=150, v_x=v_x, quirk=quirk)
    
    
    def new_platform(self):
        """Add a platform to the list of platforms."""
        # choices: list[Quirk] = [Quirk.NONE, Quirk.BREAK, Quirk.DEATH]
        # weights: list[float] = [0.75, 0.2, 0.05]

        # quirk: Quirk = r.choices(choices, weights=weights, k=1)[0]
        quirk: Quirk = Quirk.NONE
        
        platform = self._generate_platform(quirk)
        
        self._platform_list.append(platform)


    def new_quirked_platform(self):
        """Add a quirked platform to the list of platforms."""
        quirk: Quirk = r.choice(list(filter(lambda q: q != Quirk.NONE, list(Quirk))))
        
        platform = self._generate_platform(quirk)
        
        self._platform_list.append(platform)
        

    def manage_platform(self):
        if len(self._platform_list) <= 5:
            self.new_platform()
        
        elif self._platform_list[-1].y >= 750:
            self.new_platform()

        # if r.random() >= 0.99:
        #     self.new_quirked_platform()

    def auto_screen(self):
        if self._ball.y <= self._height//2 and self._ball.v_y < 0:
            self._ball.y -= self._ball.v_y//2
            for platform in self._platform_list:
                platform.y -= self._ball.v_y//2


class View:
    def start_screen(self, mouse_x: float, mouse_y: float):
        pyxel.cls(col=pyxel.COLOR_PINK)
        pyxel.rect(x=mouse_x-5, y=mouse_y-5, w=10, h=10, col=pyxel.COLOR_RED)
    
    def playing_screen(self, ball: Ball, platform_list: list[Platform]):
        pyxel.cls(col=pyxel.COLOR_GREEN)
        pyxel.circ(x=ball.x, y=ball.y, r=ball.radius, col=pyxel.COLOR_BROWN)

        for platform in platform_list:
            pyxel.rect(x=platform.x, y=platform.y, w=platform.width, h=platform.height, col=platform.quirk.value)

    def lost_screen(self):
        ...
    
    def paused_screen(self):
        ...

class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view
        

    def update(self):
        match self._model.game_state:
            case GameState.START:
                pyxel.mouse(True)
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self._model.play_game()
                
                if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                    pyxel.quit()

            case GameState.PLAYING:
                pyxel.mouse(False)
                self._model.height_update()
                self._model.manage_platform()
                self._model.auto_screen()
        
                if pyxel.btn(pyxel.KEY_D):
                    self._model.push_right()
                
                if pyxel.btn(pyxel.KEY_A):
                    self._model.push_left()

                if pyxel.btn(pyxel.KEY_P):
                    self._model.pause_game()

                if self._model.check_collision():
                    if platform := self._model.check_collision():
                        self._model.quirk_release(platform.quirk)



            case GameState.PAUSE:
                pyxel.quit()

            case GameState.END:
                pyxel.cls(col=pyxel.COLOR_RED)
                pyxel.text(50, 50, "GAME OVER", col=pyxel.COLOR_WHITE)
                

            
    def draw(self):
        match self._model.game_state:
            case GameState.START:
                self._view.start_screen(pyxel.mouse_x, pyxel.mouse_y)
                

            case GameState.PLAYING:
                self._view.playing_screen(self._model.ball, self._model.platform_list)

            case GameState.PAUSE:
                ...

            case GameState.END:
                ...

            

        