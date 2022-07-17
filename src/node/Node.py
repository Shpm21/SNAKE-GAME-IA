class Node:
    def __init__(self, position =None) -> None:
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 1000000
        self.next = None
    
    def __eq__(self, other) -> bool:
        return self.position == other.position