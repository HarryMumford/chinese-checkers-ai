
import copy
import random
import views
import domain
from enum import Enum
import unittest


class Direction(Enum):
    NE = 0
    E = 1
    SE = 2
    SW = 3
    W = 4
    NW = 5


class NeighbourStates:
    NE: domain.State = domain.State.EMPTY
    E: domain.State = domain.State.EMPTY
    SE: domain.State = domain.State.EMPTY
    SW: domain.State = domain.State.EMPTY
    W: domain.State = domain.State.EMPTY
    NW: domain.State = domain.State.EMPTY


class Coord:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return '[{0}, {1}]'.format(self.x, self.y)


class Cell:
    moves: list
    state: domain.State = domain.State.EMPTY

    def __init__(self, state: domain.State) -> None:
        self.state = state
        self.moves = []
    
    def add_move(self, move: Coord) -> None:
        for m in self.moves:
            if move.x == m.x and move.y == m.y:
                return
        self.moves.append(move)

    def delete_move(self, move: Coord) -> None:
        for m in self.moves:
            if move.x == m.x and move.y == m.y:
                self.moves.remove(m)
                return

    def __str__(self) -> str:
        moves = ""
        for m in self.moves:
            moves += '[{0}, {1}] '.format(m.x, m.y)
        return 'moves: {0}\nstate: {1}'.format(moves, self.state)


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


class Movement():
    def __init__(self, board) -> None:
        self.board: Board = board

    def move(self, start: Coord, dest: Coord):
        selected: Cell = self.board.get_cell(start)
        if selected.state != domain.State.OCCUPIED:
            raise Exception("unable to move: this cell is not occupied")
    
        self.board.update_cell(start, domain.State.SELECTED)
        self.board.save_state()
        self.board.update_cell(start, domain.State.EMPTY)
        dest_cell: Cell = self.board.get_cell(dest)
        if dest_cell.state != domain.State.EMPTY:
            raise Exception("unable to move: destination is not empty")
        self.board.update_cell(dest, domain.State.SELECTED)
        self.board.save_state()
        self.board.update_cell(dest, domain.State.OCCUPIED)
        self.board.inc_turn()
        self.board.save_state()

class BoardState:
    cells: list
    turn: int

    def __init__(self, cells, turn: int) -> None:
        self.cells = cells
        self.turn = turn

    def __str__(self) -> str:
        frame_str = "turn: " + str(self.turn)
        return frame_str


class Board():
    history = []
    _pending_state: BoardState
    _pending_changes: bool

    def __init__(self, initial_cells) -> None:
        i = 0
        for row in initial_cells:
            max_length = 17
            if len(row) != max_length:
                raise Exception("Row " + str(i) + " is " + str(len(row)) +
                                " in length. All rows must be " + str(max_length) + " elements long")
            i += 1
        self._pending_state = BoardState(initial_cells, 0)
        self._pending_changes = True
        self.save_state()
        
    def inc_turn(self) -> None:
        self._pending_state.turn += 1

    def get_cell(self, coord: Coord) -> Cell:
        if self._pending_changes == True:
            return copy.deepcopy(self._pending_state.cells[coord.y][coord.x])
        return copy.deepcopy(self.history[-1].cells[coord.y][coord.x])

    def get_cells(self) -> list:
        if self._pending_changes == True:
            return copy.deepcopy(self._pending_state.cells)
        return copy.deepcopy(self.history[-1].cells)

    def update_cell(self, coord: Coord, state: domain.State) -> None:
        if coord.x < 0 or coord.y < 0:
            raise Exception("failed to update: x and y must be positive")
        if self._pending_state.cells[coord.y][coord.x] == None:
            raise Exception(
                "failed to update: coordinates do not specify a cell")
        if self._pending_changes == False:
            self._pending_state = copy.deepcopy(self.history[-1])
        self._pending_state.cells[coord.y][coord.x].state = state
        if state == domain.State.OCCUPIED or state == domain.State.EMPTY:
            self._update_moves(coord)
        self._pending_changes = True

    def save_state(self) -> None:
        if self._pending_changes == True:
            self.history.append(self._pending_state)
        self._pending_changes = False

    def _update_moves(self, coord: Coord) -> None:
        current_state_cells = self._pending_state.cells
        cell: Cell = current_state_cells[coord.y][coord.x]
        if cell.state == domain.State.EMPTY:
            cell.moves.clear()
            
        affected_cells_coords = [
            Coord(coord.x - 1, coord.y - 1),    # nw
            Coord(coord.x, coord.y-1),          # ne
            Coord(coord.x-1, coord.y),          # w
            Coord(coord.x+1, coord.y),          # e
            Coord(coord.x, coord.y+1),          # sw
            Coord(coord.x+1, coord.y+1)         # se
        ]
        
        for c in affected_cells_coords:
            affected_cell: Cell = current_state_cells[c.y][c.x]
            
            if affected_cell == None:
                continue
            
            if cell.state == domain.State.OCCUPIED:
                if affected_cell.state == domain.State.EMPTY:
                    cell.add_move(Coord(c.x, c.y))
                if affected_cell.state == domain.State.OCCUPIED:
                    affected_cell.delete_move(coord)
            
            if cell.state == domain.State.EMPTY and affected_cell.state == domain.State.OCCUPIED:
                affected_cell.add_move(Coord(coord.x, coord.y))

               
class Player:
    starting_coords: list

    def __init__(self, starting_coords) -> None:
        self.starting_coords = starting_coords


def run():
    initial_cells = [
        [None, None, None, None, Cell(
            domain.State.EMPTY), None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), Cell(domain.State.EMPTY), None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), Cell(domain.State.EMPTY), None, None, None, None, None, None, None, None, None],
        [Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), None, None, None, None],
        [None, Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), None, None, None, None],
        [None, None, Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), None, None, None, None],
        [None, None, None, Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), None, None, None, None],
        [None, None, None, None, Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), None, None, None, None],
        [None, None, None, None, Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), None, None, None],
        [None, None, None, None, Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), None, None],
        [None, None, None, None, Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), None],
        [None, None, None, None, Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(
            domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(domain.State.EMPTY)],
        [None, None, None, None, None, None, None, None, None, Cell(domain.State.EMPTY), Cell(domain.State.EMPTY), Cell(
         domain.State.EMPTY), Cell(domain.State.EMPTY), None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, Cell(domain.State.EMPTY), Cell(
         domain.State.EMPTY), Cell(domain.State.EMPTY), None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, Cell(
         domain.State.EMPTY), Cell(domain.State.EMPTY), None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, Cell(
            domain.State.EMPTY), None, None, None, None],
    ]

    board = Board(copy.deepcopy(initial_cells))
    movement = Movement(board)
    p1 = Player([
        Coord(4, 0),
        Coord(4, 1),
        Coord(5, 1),
        Coord(4, 2),
        Coord(5, 2),
        Coord(6, 2),
        Coord(4, 3),
        Coord(5, 3),
        Coord(6, 3),
        Coord(7, 3),
    ])

    for coord in p1.starting_coords:
        board.update_cell(coord, domain.State.OCCUPIED)
    board.save_state()
        
    i = 0
    while i < 100:
        movable: list = []
        y = 0
        for r in board.get_cells():
            x = 0
            for c in r:
                c: Cell
                if c != None and c.state == domain.State.OCCUPIED:
                    if len(c.moves) > 0:
                        movable.append(Coord(x, y)) 
                x += 1
            y += 1
        selected_coord: Coord = random.choice(movable)
        selected_cell: Cell =  board.get_cell(selected_coord)
        dest: Coord = random.choice(selected_cell.moves)
        movement.move(selected_coord, dest)
        i += 1

             
    animator = views.Animation(board.history, False)
    animator.run(0.1)

run()

