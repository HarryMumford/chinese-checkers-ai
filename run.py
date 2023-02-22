
import copy
import random
import views
import domain
from enum import Enum


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


class Cell:
    neighbour_states: NeighbourStates
    state: domain.State = domain.State.EMPTY

    def __init__(self, state: domain.State) -> None:
        self.state = state
        self.neighbour_states = NeighbourStates()
    
    def __str__(self) -> str:
        return '{0}'.format(self.state.value)


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


class Coord:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Movement():
    def __init__(self, board) -> None:
        self.board: Board = board

    def move(self, coord: Coord, direction: Direction) -> Coord:
        selected: Cell = self.board.get_cell(coord.x, coord.y)
        if selected.state != domain.State.OCCUPIED:
            raise Exception("unable to move: this cell is not occupied")
        new_x = coord.x
        new_y = coord.y
        if direction == Direction.NW:
            new_x -= 1
            new_y -= 1
        elif direction == Direction.NE:
            new_y -= 1
        elif direction == Direction.E:
            new_x += 1
        elif direction == Direction.W:
            new_x -= 1
        elif direction == Direction.SW:
            new_y += 1
        elif direction == Direction.SE:
            new_x += 1
            new_y += 1
        else:
            raise Exception("direction not supported")
        self.board.update_cell(coord.x, coord.y, domain.State.SELECTED)
        self.board.save_state()
        self.board.update_cell(coord.x, coord.y, domain.State.EMPTY)
        new_cell: Cell = self.board.get_cell(new_x, new_y)
        if new_cell != domain.State.EMPTY:
            raise Exception("unable to move: destination is not empty")
        self.board.update_cell(new_x, new_y, domain.State.SELECTED)
        self.board.save_state()
        self.board.update_cell(new_x, new_y, domain.State.OCCUPIED)
        self.board.save_state()
        return Coord(new_x, new_y)


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

    def get_cell(self, x: int, y: int) -> Cell:
        if self._pending_changes == True:
            return copy.deepcopy(self._pending_state.cells[y][x])
        return copy.deepcopy(self.history[-1].cells[y][x])
    
    def get_cells(self) -> list:
        if self._pending_changes == True:
            return copy.deepcopy(self._pending_state.cells)
        return copy.deepcopy(self.history[-1].cells)

    def update_cell(self, x: int, y: int, state: domain.State) -> None:
        if x < 0 or y < 0:
            raise Exception("failed to update: x and y must be positive")
        if self._pending_state.cells[y][x] == None:
            raise Exception(
                "failed to update: coordinates do not specify a cell")
        if self._pending_changes == False:
            self._pending_state = copy.deepcopy(self.history[-1])
        self._pending_state.cells[y][x].state = state
        self._update_neighbours(x, y)
        self._pending_changes = True

    def save_state(self) -> None:
        if self._pending_changes == True:
            self.history.append(self._pending_state)
        self._pending_changes = False

    def _update_neighbours(self, x: int, y: int) -> None:
        current_state_cells = self._pending_state.cells
        cell: Cell = current_state_cells[y][x]
        # look north
        if y > 0:
            nw_neighbour: Cell = current_state_cells[y - 1][x - 1]
            if nw_neighbour != None:
                nw_neighbour.neighbour_states.SE = cell.state
                cell.neighbour_states.NW = nw_neighbour.state

            if x < len(current_state_cells[y]):
                ne_neighbour: Cell = current_state_cells[y - 1][x]
                if ne_neighbour != None:
                    ne_neighbour.neighbour_states.SW = cell.state
                    cell.neighbour_states.NE = ne_neighbour.state

        # look west
        if x > 0:
            w_neighbour: Cell = current_state_cells[y][x - 1]
            if w_neighbour != None:
                w_neighbour.neighbour_states.E = cell.state
                cell.neighbour_states.W = w_neighbour.state

        # look east
        if x < len(current_state_cells[y]):
            e_neighbour: Cell = current_state_cells[y][x + 1]
            if e_neighbour != None:
                e_neighbour.neighbour_states.W = cell.state
                cell.neighbour_states.E = e_neighbour.state

        # look south
        if y < len(current_state_cells):
            sw_neighbour: Cell = current_state_cells[y - 1][x]
            if sw_neighbour != None:
                sw_neighbour.neighbour_states.NE = cell.state
                cell.neighbour_states.SW = sw_neighbour.state
            if x < len(current_state_cells):
                se_neighbour: Cell = current_state_cells[y - 1][x - 1]
                if se_neighbour != None:
                    se_neighbour.neighbour_states.NW = cell.state
                    cell.neighbour_states.SE = se_neighbour.state


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
        board.update_cell(coord.x, coord.y, domain.State.OCCUPIED)

    board.save_state()
    
    direction = random.choice(list(Direction))
    print(direction.name)
    movable: list = []
    for row in board.get_cells():
        for c in row:
            cell: Cell = c
            if cell == None:
                continue
            if cell.state != domain.State.OCCUPIED:
                continue
            print(cell.neighbour_states.__dict__.keys())
            
    

    
    animator = views.Animation(board.history, True)
    animator.run(0.5)


run()
