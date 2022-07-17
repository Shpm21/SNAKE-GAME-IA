from node.Node import Node
from collections import deque

def actions() -> list:
    return [
        lambda map, x, y: map[x-1][y],
        lambda map, x, y: map[x+1][y],
        lambda map, x, y: map[x][y-1],
        lambda map, x, y: map[x][y+1]
    ]

def restrictions() -> list:
    return [
        lambda n: n.position[0] > 0,
        lambda n: n.position[0] < 20-1,
        lambda n: n.position[1] > 0,
        lambda n: n.position[1] < 20-1
    ]
    
def inside_body(snake, node):
    for body in snake.body:
        if body.x == node.position[0] and body.y == node.position[1]:
            return True
    return False

def outside_boundary(node):
    if not 0 <= node.position[0] < 20:
        return True
    elif not 2 <= node.position[1] < 20:
        return True
    return False

class A_STAR:
    def __init__(self) -> None:
        self.actions = actions()
        self.restrictions = restrictions()
        
    def evaluate_path(self, map, node, goal, snake):
        init_node = Node(node)
        goal_node = Node(goal)  
        open_nodes = []
        close_nodes = []
        open_nodes.append(init_node)
        
        while len(open_nodes) > 0:
            i = 0
            for index, item in enumerate(open_nodes):
                if item.f < open_nodes[0].f:
                    i = index
            current = open_nodes.pop(i)
            
            if current == goal_node:
                if current.next is None:
                    return current
                while current.next.next is not None:
                    current = current.next
                return current
            
            close_nodes.append(current)
            
            successors = []
            for act, res in zip(self.actions, self.restrictions):
                if res(current):
                    successors.append(act(map, current.position[0], current.position[1]))

            for successor in successors:
                if inside_body(snake, successor) or outside_boundary(successor) or successor in close_nodes:
                    continue
                g = current.g + 1
                best = False
                
                if successor not in open_nodes:
                    successor.h = ((successor.position[0] - goal_node.position[0]) ** 2) + ((successor.position[1] - goal_node.position[1])**2)
                    open_nodes.append(successor)
                    best = True
                elif current.g < successor.g:
                    best = True
                
                if best:
                    successor.next = current
                    successor.g = g
                    successor.f = successor.g + successor.h
        return None
    
class BFS:
    def __init__(self) -> None:
        self.actions = actions()
        self.restrictions = restrictions()
        
    def evaluate_path(self, map, node, goal, snake):
        init_node = Node(node)
        goal_node = Node(goal)
        open_nodes = deque([])
        close_nodes = []
        open_nodes.append(init_node)
        
        while len(open_nodes) > 0:
            current = open_nodes.popleft()
            close_nodes.append(current)
            successors = []
            for act, res in zip(self.actions, self.restrictions):
                if res(current):
                    successors.append(act(map, current.position[0], current.position[1]))
                    
            for successor in successors:
                if inside_body(snake, successor) or outside_boundary(successor) or successor in close_nodes:
                    close_nodes.append(successor)
                    continue
                    
                if successor not in open_nodes and successor not in close_nodes:
                    successor.next = current
                    close_nodes.append(successor)
                    open_nodes.append(successor)
                    
                    if successor == goal_node:
                        if successor.next is None:
                            return successor
                        while successor.next.next is not None:
                            successor = successor.next
                        return successor
        return None
            
class DFS:
    def __init__(self) -> None:
        self.actions = actions()
        self.restrictions = restrictions()
        self.path = []
        self.open_nodes = []
        self.close_nodes = []
    
    def recursive_path(self, map, snake, goal_node, current):
        if current == goal_node:
            if current.next is None:
                return current
            while current.next.next is not None:
                current = current.next
            return current
        
        if current in self.close_nodes:
            return None

        self.close_nodes.append(current)
        
        successors = []
        for act, res in zip(self.actions, self.restrictions):
            if res(current):
                successors.append(act(map, current.position[0], current.position[1]))
                
        for successor in successors:
            if not inside_body(snake, successor) and not outside_boundary(successor) and successor not in self.close_nodes:
                successor.next = current
                path = self.recursive_path(map, snake, goal_node, successor)
                if path is not None:
                    return path
        return None
        
    def evaluate_path(self, map, node, goal, snake):
        if len(self.path) != 0:
            path = self.path.pop()
            
            if inside_body(snake, path):
                self.path = []
            else:
                return path
        
        init_node = Node(node)
        goal_node = Node(goal)
        
        self.open_nodes.append(init_node)
        
        return self.recursive_path(map, snake, goal_node, init_node)