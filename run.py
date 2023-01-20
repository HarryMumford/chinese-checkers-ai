from enum import Enum
from time import sleep
import copy
import os

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

    def move(self, coord: Coord, direction: Direction) -> Coord: 
        if self.board.get(coord) == 2:
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
        
        self.board.move(coord, new_coord)
        return new_coord
             
class Board():
    history = []
    
    def __init__(self, initial_state) -> None:
        self.history.append(copy.deepcopy(initial_state))
        
    def populate_all(self, coords):
        current_state = self._get_current_state()
        for coord in coords:
            current_state[coord.y][coord.x] = 2
        self._update_history(current_state)
        
    def move(self, old_coord, new_coord):
        current_state = self._get_current_state()
        current_state[old_coord.y][old_coord.x] = 1
        current_state[new_coord.y][new_coord.x] = 2
        self._update_history(current_state)
                    
    def get(self, coord: Coord) -> int:
        current_state = self._get_current_state()
        return current_state[coord.y][coord.x]
    
    def _update_history(self, board_state):
        self.history.append(board_state)
        
    def _get_current_state(self):
        return copy.deepcopy(self.history[-1])


class Player:
    def __init__(self, starting_coords) -> None:
        self.starting_coords = starting_coords


class Animation():
    frames = []

    def __init__(self, state_history) -> None:
        for state in state_history:
            frame_str = ""
            count = 0
            for line in state:
                if count % 2 != 0:
                    frame_str += "  "
                for pixel in line:
                    if pixel == 0:
                        frame_str += "    "
                    if pixel == 1:
                        frame_str += "○   "
                    if pixel == 2:
                        frame_str += "●   "
                frame_str += "\n"
                count += 1
            self.frames.append(frame_str)
            
    def run(self) -> None:
        sleep(1)
        os.system('clear')
        for f in self.frames:
            print(f)
            sleep(0.5)
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

    
    dest = movement.move(Coord(4, 13), Direction.NW)
    dest = movement.move(dest, Direction.NW)
    dest = movement.move(dest, Direction.NW)
    dest = movement.move(dest, Direction.NE)
    dest = movement.move(dest, Direction.NE)
    dest = movement.move(dest, Direction.SE)
    dest = movement.move(dest, Direction.SE)
    dest = movement.move(dest, Direction.SW)
    dest = movement.move(dest, Direction.SW)
    dest = movement.move(dest, Direction.E)
    dest = movement.move(dest, Direction.W)
    

    animator = Animation(board.history)
    animator.run()
    
run()
