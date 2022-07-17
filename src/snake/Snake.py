from pygame.math import Vector2

class Snake:
    def __init__(self, hidden=8) -> None:
        self.body = [Vector2(5, 8), Vector2(4, 8), Vector2(3, 8)]
        self.direction = 'r'
        self.change_direction(self.direction)
        self.hidden = hidden
        
    def change_direction(self, direction) -> None:
        if direction == 'r' and not self.direction == 'l':
            self.direction = 'r'
        elif direction == 'l' and not self.direction == 'r':
            self.direction = 'l'
        elif direction == 'u' and not self.direction == 'd':
            self.direction = 'u'
        elif direction == 'd' and not self.direction == 'u':
            self.direction = 'd'

    def eat_food(self, food):
        if food.pos == self.body[0]:
            return True 
        return False
    
    def add_body(self):
        tail = self.body[-1]
        
        if tail.x == self.body[-2].x:
            if tail.y < self.body[-2].y:
                self.body.append(Vector2(tail.x, tail.y-1))
            else:
                self.body.append(Vector2(tail.x, tail.y+1))
        elif tail.y == self.body[-2].y:
            if tail.x < self.body[-2].x:
                self.body.append(Vector2(tail.x-1, tail.y))
            else:
                self.body.append(Vector2(tail.x+1, tail.y))
    
    def exist_in_tail(self, pos):
        if pos in self.body[1:]:
            return True
        return False