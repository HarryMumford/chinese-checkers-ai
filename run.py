
import copy
import random
import views
import domain
from enum import Enum

class Cell:
    neighbours = []
    state: domain.State = domain.State.EMPTY
    x: int = 0
    y: int = 0

    def __init__(self, x: int, y: int, state: domain.State) -> None:
        self.x: int = x
        self.y: int = y
        self.state = state

    def __str__(self) -> str:
        return '[{0}, {1}] state: {2}'.format(self.x, self.y, self.state)

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

south_starting_position = [
    Cell(0, 16, domain.State.OCCUPIED),
    Cell(0, 15, domain.State.OCCUPIED),
    Cell(1, 15, domain.State.OCCUPIED),
    Cell(0, 14, domain.State.OCCUPIED),
    Cell(1, 14, domain.State.OCCUPIED),
    Cell(2, 14, domain.State.OCCUPIED),
    Cell(0, 13, domain.State.OCCUPIED),
    Cell(1, 13, domain.State.OCCUPIED),
    Cell(2, 13, domain.State.OCCUPIED),
    Cell(3, 13, domain.State.OCCUPIED),
]

class Movement():
    def __init__(self, board) -> None:
        self.board = board

    # def move(self, coord: Coord, direction: Direction) -> Coord: 
    #     if coord.x >= self.board.width or coord.y >= self.board.height:
    #         return None
        
    #     adjacent_coord = self._get_adjacent_coord(coord, direction)
    #     if self.board.get_state(adjacent_coord) == 0:
    #         return None
        
    #     if self.board.get_state(adjacent_coord) == 1:
    #         self.board.move(coord, adjacent_coord, True)
    #         return adjacent_coord
    
    # def jump(self, coord: Coord, direction: Direction) -> Coord: 
    #     adjacent_coord = self._get_adjacent_coord(coord, direction)
        
    #     s = self.board.get_state(adjacent_coord)
       
        
    #     if self.board.get_state(adjacent_coord) == 2:
    #         jump_dest = self._get_adjacent_coord(adjacent_coord, direction)
    #         print(jump_dest)
    #         if self.board.get_state(jump_dest) == 1:
    #             self.board.move(coord, jump_dest, False)
    #             return jump_dest
            
    #     return None
                 
    # def _get_adjacent_coord(self, coord: Coord, direction: Direction) -> Coord:
    #     if direction == Direction.E:
    #         new_coord = Coord(coord.x+1, coord.y)
    #     if direction == Direction.SE:
    #         if coord.y % 2 == 0:
    #             new_coord = Coord(coord.x, coord.y+1)
    #         else:
    #             new_coord = Coord(coord.x+1, coord.y+1)
    #     if direction == Direction.SW:
    #         if coord.y % 2 == 0:
    #             new_coord = Coord(coord.x-1, coord.y+1)
    #         else:
    #             new_coord = Coord(coord.x, coord.y+1)
    #     if direction == Direction.W:
    #         new_coord = Coord(coord.x-1, coord.y)
    #     if direction == Direction.NW:
    #         if coord.y % 2 == 0:
    #             new_coord = Coord(coord.x-1, coord.y-1)
    #         else:
    #             new_coord = Coord(coord.x, coord.y-1)
    #     if direction == Direction.NE:
    #         if coord.y % 2 == 0:
    #             new_coord = Coord(coord.x, coord.y-1)
    #         else:
    #             new_coord = Coord(coord.x+1, coord.y-1)
    #     return new_coord
    
class BoardState:
    cells = [[]]
    turn: int
    
    def __init__(self, state, turn: int) -> None:
        self.cells = state
        self.turn = turn

    def __str__(self) -> str:
            frame_str = "turn: " + str(self.turn)
            return frame_str
    

class Board():
    history = []
    _pending_state: BoardState
    _pending_changes: bool

    def __init__(self, initial_cells) -> None:
        self._pending_state = BoardState(initial_cells, 0)
        self._pending_changes = True
        self.save_state()
        
    def update_cells(self, cells) -> None:
        if self._pending_changes == False:
            self._pending_state = copy.deepcopy(self.history[-1])
        for cell in cells:
            self._pending_state.cells[cell.y][cell.x].state = cell.state
        self._pending_changes = True
        
    def update_cell(self, cell: Cell) -> None:
        if self._pending_changes == False:
            self._pending_state = copy.deepcopy(self.history[-1])
        self._pending_state.cells[cell.y][cell.x].state = cell.state
        self._pending_changes = True
       
    def save_state(self) -> None:
        if self._pending_changes == True:
            self.history.append(self._pending_state)
        self._pending_changes = False
        
    def _update_neighbours(self, cell: Cell) -> None:
        cell.neighbours
            
class Player:
    def __init__(self, starting_coords) -> None:
        self.starting_coords = starting_coords

def run():
    row_lengths = [1, 2, 3, 4, 13, 12, 11, 10, 9, 10, 11, 12, 13, 4, 3, 2, 1]
    initial_cells = []
    y = 0
    for l in row_lengths:
        x = 0
        row = []
        while x < l:
            row.append(Cell(x, y, domain.State.EMPTY))
            x += 1
        initial_cells.append(row)
        y += 1
        

    p1 = Player(south_starting_position)
    board = Board(copy.deepcopy(initial_cells))
    # movement = Movement(board)

    board.update_cells(p1.starting_coords)
    board.save_state()
    animator = views.Animation(board.history)
    animator.run(1)
    # directions = []
    # for d in Direction:
    #     directions.append(d)
        
    # coords = board.get_coords_with_state(2)
    # while board.get_current_turn() <= 10:
    #     start = random.choice(coords)
    #     dest = movement.move(start, random.choice([Direction.NE, Direction.NW]))
            
    # animator = Animation(board.history)
    # animator.run()
           
run()
