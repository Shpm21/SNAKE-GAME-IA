import pygame
from food.Food import Food
from snake.Snake import Snake
from a_algorithm.Algorithm import A_STAR
from node.Node import Node
from a_algorithm.Algorithm import BFS
from a_algorithm.Algorithm import DFS

CELL = 20
N_OF_CELL = 20
SIZE = CELL * N_OF_CELL
class Game:
    def __init__(self) -> None:
        self.map = self.generate_map()
        self.window = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption("Snake Game")
        self.fps = pygame.time.Clock()
        self.food = Food()
        self.snake = Snake()
        self.score = 0 
        #self.algorithm = A_STAR()
        self.algorithm = BFS()
        #self.algorithm = DFS()
        self.inicio = (int(self.snake.body[0].x),int(self.snake.body[0].y))
        self.objetivo = (int(self.food.pos.x),int(self.food.pos.y))
        self.window.fill(pygame.Color(255, 255, 255))
        self.end = False
              
    def keep_moving(self):
        x = self.snake.body[0].x
        y = self.snake.body[0].y

        if self.snake.body[1].x == x:
            if self.snake.body[1].y < y:
                y = y + 1
            else:
                y = y - 1
        elif self.snake.body[1].y == y:
            if self.snake.body[1].x < x:
                x = x + 1
            else:
                x = x - 1
        return x, y
    
    def draw(self, element, color, border=False):
        x = int(element.x * CELL)
        y = int(element.y * CELL)
        body_rect = pygame.Rect(x, y, CELL, CELL)
        pygame.draw.rect(self.window, color, body_rect)
        if border:
            pygame.draw.rect(self.window, (CELL, CELL, CELL+1), body_rect, 3)
            
    def draw_snake(self):
        self.draw(self.snake.body[0], color=(90, 255, 90), border=True)
            
        for body in self.snake.body[1:]:
            self.draw(body, color=(0, 255, 0))
        
    def draw_cell(self):
        for i in range(N_OF_CELL):
            for j in range(N_OF_CELL):
                self.draw(pygame.Rect(i, j, CELL, CELL), pygame.Color(0, 0, 0), border=True)
        
    def draw_food(self):
        self.draw(pygame.Rect(self.food.pos.x, self.food.pos.y, CELL, CELL), pygame.Color(255, 0, 0))    
        
    def draw_elements(self):
        self.draw_cell() 
        self.draw_snake()
        self.draw_food()
        
    def respawn_food(self):
        self.food.spawn()
        
    def add_snake_body(self):
        self.snake.add_body()
        
    def snake_eat_food(self) -> bool:
        return (self.snake.eat_food(self.food))
    
    def game_over(self):
        if self.snake.body[0].x < 0 or self.snake.body[0].y > N_OF_CELL:
            self.end = True
        elif self.snake.body[0].y < 2 or self.snake.body[0].y > N_OF_CELL:
            self.end = True
        elif self.snake.exist_in_tail(self.snake.body[0]):
            self.end = True
            
    def __run__(self) -> None:
        while not self.end:
            path = self.algorithm.evaluate_path(self.map, self.inicio, self.objetivo, self.snake)
            if path is None:
                x, y = self.keep_moving()
            else:
                x = path.position[0]
                y = path.position[1]
            
            for i in range(len(self.snake.body)-1, 0, -1):
                self.snake.body[i].x = self.snake.body[i-1].x
                self.snake.body[i].y = self.snake.body[i-1].y

            self.snake.body[0].x = x
            self.snake.body[0].y = y
            
            self.window.fill(pygame.Color(255, 255, 255))
            
            self.draw_elements()
            
            if self.snake_eat_food():
                self.score += 1
                self.respawn_food()
                while self.food.pos in self.snake.body[1:]:
                    self.respawn_food()
                
                self.add_snake_body()
                
            self.game_over()
            pygame.display.flip()
            self.fps.tick(24)
            
            self.inicio = (int(self.snake.body[0].x),int(self.snake.body[0].y))
            self.objetivo = (int(self.food.pos.x),int(self.food.pos.y))
        print(f'Puntaje Obtenido: {self.score}')  
        
    def generate_map(self) -> list:
        map = []
        for i in range(N_OF_CELL):
            aux = []
            for j in range(N_OF_CELL):
                aux.append(Node((i, j)))
            map.append(aux)
        return map