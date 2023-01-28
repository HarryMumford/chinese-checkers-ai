from enum import Enum
from time import sleep
import copy
import os
import random

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Direction(Enum):
    NE = 0
    E = 1
    SE = 2
    SW = 3
    W = 4
    NW = 5

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

    def move(self, coord: Coord, direction: Direction) -> Coord: 
        if coord.x >= self.board.width or coord.y >= self.board.height:
            return None
        
        adjacent_coord = self._get_adjacent_coord(coord, direction)
        if self.board.get_state(adjacent_coord) == 0:
            return None
        
        if self.board.get_state(adjacent_coord) == 1:
            self.board.move(coord, adjacent_coord, True)
            return adjacent_coord
    
    def jump(self, coord: Coord, direction: Direction) -> Coord: 
        adjacent_coord = self._get_adjacent_coord(coord, direction)
        
        s = self.board.get_state(adjacent_coord)
       
        
        if self.board.get_state(adjacent_coord) == 2:
            jump_dest = self._get_adjacent_coord(adjacent_coord, direction)
            print(jump_dest)
            if self.board.get_state(jump_dest) == 1:
                self.board.move(coord, jump_dest, False)
                return jump_dest
            
        return None
                 
    def _get_adjacent_coord(self, coord: Coord, direction: Direction) -> Coord:
        if direction == Direction.E:
            new_coord = Coord(coord.x+1, coord.y)
        if direction == Direction.SE:
            if coord.y % 2 == 0:
                new_coord = Coord(coord.x, coord.y+1)
            else:
                new_coord = Coord(coord.x+1, coord.y+1)
        if direction == Direction.SW:
            if coord.y % 2 == 0:
                new_coord = Coord(coord.x-1, coord.y+1)
            else:
                new_coord = Coord(coord.x, coord.y+1)
        if direction == Direction.W:
            new_coord = Coord(coord.x-1, coord.y)
        if direction == Direction.NW:
            if coord.y % 2 == 0:
                new_coord = Coord(coord.x-1, coord.y-1)
            else:
                new_coord = Coord(coord.x, coord.y-1)
        if direction == Direction.NE:
            if coord.y % 2 == 0:
                new_coord = Coord(coord.x, coord.y-1)
            else:
                new_coord = Coord(coord.x+1, coord.y-1)
        return new_coord
    
class BoardState:
    state = [[]]
    turn: int
    
    def __init__(self, state, turn: int) -> None:
        self.state = state
        self.turn = turn

    def __str__(self) -> str:
            frame_str = "turn: " + str(self.turn) + "\n"
            for line in self.state:
                count = 0
                if count % 2 != 0:
                    frame_str += "  "
                for pixel in line:
                    if pixel == 0:
                        frame_str += "    "
                    if pixel == 1:
                        frame_str += "○   "
                    if pixel == 2:
                        frame_str += "●   "
                    if pixel == 3:
                        frame_str += "◎   "
                if count % 2 == 0:
                    frame_str += "  "
                frame_str += "\n"
                count += 1
                return frame_str
    

class Board():
    history = []

    def __init__(self, initial_state) -> None:
        self.width = len(initial_state[0])
        self.height = len(initial_state)
        self.history.append(BoardState(copy.deepcopy(initial_state), 0))
        
    def populate_all(self, coords) -> None:
        current_state = self._get_all_states()
        for coord in coords:
            current_state.state[coord.y][coord.x] = 2
        self.history.append(current_state)
    
    def move(self, old_coord: Coord, new_coord: Coord, end_turn: bool) -> None:
        current_state = self._get_all_states()
        current_state.state[old_coord.y][old_coord.x] = 3
        self.history.append(current_state)
        current_state = self._get_all_states()
        current_state.state[old_coord.y][old_coord.x] = 1
        current_state.state[new_coord.y][new_coord.x] = 3
        self.history.append(current_state)
        if end_turn:
            current_state = self._get_all_states()
            current_state.state[new_coord.y][new_coord.x] = 2
            current_state.turn += 1
            self.history.append(current_state)
        
    def get_coords_with_state(self, state: int):
        coords = []
        y = 0
        for row in self._get_all_states().state:
            x = 0
            for s in row:
                if s == state:
                    coords.append(Coord(x, y))
                x += 1
            y += 1
               
        return coords
    
    def get_current_turn(self) -> int:
        return self.history[-1].turn
        
    def get_state(self, coord: Coord) -> int:
        if coord.x > self.width - 1 or coord.y > self.height - 1:
            return 0
        return self._get_all_states().state[coord.y][coord.x]
            
    def _get_all_states(self) -> BoardState: 
        return BoardState(copy.deepcopy(self.history[-1].state), self.history[-1].turn)

class Player:
    def __init__(self, starting_coords) -> None:
        self.starting_coords = starting_coords


class Animation():
    frames = []

    def __init__(self, state_history) -> None:
        self.state_history = state_history 
        for state in state_history:
            frame_str = "turn: " + str(state.turn) + "\n"
            count = 0
            for line in state.state:
                if count % 2 != 0:
                    frame_str += "  "
                for pixel in line:
                    if pixel == 0:
                        frame_str += "    "
                    if pixel == 1:
                        frame_str += "○   "
                    if pixel == 2:
                        frame_str += "●   "
                    if pixel == 3:
                        frame_str += "◎   "
                if count % 2 == 0:
                    frame_str += "  "
                frame_str += "\n"
                count += 1
            self.frames.append(frame_str)
            
    def run(self) -> None:
        sleep(1)
        os.system('clear')
        for f in self.frames:
            print(f)
            sleep(0.7)
            os.system('clear')

def run():
    initial_state = [
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # 0
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # 1
        [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # 2
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],  # 3
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 4
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 5
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 6
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 7
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 8
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],  # 9
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 10
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],  # 11
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 12
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],  # 13
        [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # 14
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],  # 15
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # 16
    ]
    
    p1 = Player(Position.SOUTH)
    board = Board(copy.deepcopy(initial_state))
    movement = Movement(board)

    board.populate_all(p1.starting_coords)
    directions = []
    for d in Direction:
        directions.append(d)
        
    coords = board.get_coords_with_state(2)
    while board.get_current_turn() <= 10:
        start = random.choice(coords)
        dest = movement.move(start, random.choice([Direction.NE, Direction.NW]))
            
    animator = Animation(board.history)
    animator.run()

def jumped(coord: Coord, new_coord: Coord) -> bool:
   if abs(coord.x - new_coord.x) == 2 or abs(coord.y - new_coord.y) == 2:
       return True
           
run()
