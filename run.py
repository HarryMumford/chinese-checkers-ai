from enum import Enum
from time import sleep

Direction = Enum('Direction', ['NE', 'E', 'SE', 'SW', 'W', 'NW'])

class Coord:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
    
    def __str__(self) -> str:
        return '[{0}, {1}]'.format(self.x, self.y)

class Position():
    SOUTH = [
        Coord(6, 16),
        Coord(6, 15),
        Coord(5, 15),
        Coord(7, 14),
        Coord(6, 14),
        Coord(5, 14),
        Coord(7, 13),
        Coord(6, 13),
        Coord(5, 13),
        Coord(4, 13),
    ]
    
class Movement():
    def __init__(self, board) -> None:
        self.board = board
    
    def move(self, coord: Coord, direction: Direction):
        if self.board.get(coord) == 2:
            self.board.set(coord, 1)
            if direction == Direction.NE:
                self.board.set(Coord(coord.x, coord.y-1), 2)
        
class StateTracker:
    history = []
    
    def update(self, state):
        self.history.append(state)
            
class Board():
    def __init__(self, state_tracker: StateTracker, initial) -> None:
        self.current = initial
        self.state_tracker = state_tracker
        state_tracker.update(initial)
        
    def set(self, coord: Coord, state):
        self.current[coord.y][coord.x] = state
        self.state_tracker.update(self.current)
        
    def get(self, coord: Coord) -> int:
        return self.current[coord.y][coord.x]
    
class Player:
    def __init__(self, starting_coords) -> None:
        self.starting_coords = starting_coords
        
initial_state = [
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], # 0
    [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], # 1
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0], # 2
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0], # 3
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 4
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], # 5
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], # 6
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], # 7
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], # 8
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], # 9
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], # 10
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], # 11
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 12
    [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0], # 13
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0], # 14
    [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], # 15
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], # 16
]

# def move(coord: Coord, direction: Direction):
#     if get_state(coord) == 2:
#         depopulate(coord)
#         if direction == Direction.NE:
#             populate(Coord(coord.x, coord.y-1))
            
# def get_state(coord: Coord):
#     return initial_state[coord.y][coord.x]
        
        
# def depopulate(coord: Coord):
#     if initial_state[coord.y][coord.x] == 2:
#         initial_state[coord.y][coord.x] = 1

# def populate(coord: Coord):
#     initial_state[coord.y][coord.x] = 2

def render(screen_map=initial_state):
    render_str = ""
    count = 0
    for line in screen_map:
        if count % 2 != 0:
            render_str += "  "
        for pixel in line:
            if pixel == 0:
                render_str += "    "
            if pixel == 1:
                render_str += "○   "
            if pixel == 2:
                render_str += "●   "
        render_str += "\n"
        count += 1
    print(render_str)
    
def run():
    p1 = Player(Position.SOUTH)
    state_tracker = StateTracker()
    board = Board(state_tracker, initial_state)
    movement = Movement(board)
    
    # populate initial
    for coord in p1.starting_coords:
        board.set(coord, 2)
        
    render()
        
    # make 1 move
    movement.move(Coord(4, 13), Direction.NE)
    
    render()
    
run()
    