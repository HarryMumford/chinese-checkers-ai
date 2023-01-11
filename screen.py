from enum import Enum

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
    

class Player:
    def __init__(self, starting_coords) -> None:
        self.starting_coords = starting_coords

pixel_map = [
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

def move(coord: Coord, direction: Direction):
    if get_state(coord) == 2:
        depopulate(coord)
        if direction == Direction.NE:
            populate(Coord(coord.x, coord.y-1))
            
def get_state(coord: Coord):
    return pixel_map[coord.y][coord.x]
        
def populate_player(player: Player):
    for coord in player.starting_coords:
        populate(coord)
        
def depopulate(coord: Coord):
    if pixel_map[coord.y][coord.x] == 2:
        pixel_map[coord.y][coord.x] = 1

def populate(coord: Coord):
    pixel_map[coord.y][coord.x] = 2

def render(screen_map=pixel_map):
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

populate_player(Player(Position.SOUTH))
render()
move(Coord(4, 13), Direction.NE)
render()
