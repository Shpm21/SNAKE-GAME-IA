from random import randrange
from pygame.math import Vector2

class Food:
    def __init__(self) -> None:
        self.pos = Vector2(0, 0)
        self.spawn()
        
    def spawn(self) -> None:
        x = randrange(1, 19)
        y = randrange(2, 19)
        self.pos = Vector2(x, y)
