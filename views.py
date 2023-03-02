from time import sleep
import os
import domain

class Animation():
    frames = []
    debug: bool

    def __init__(self, game_history, debug: bool) -> None:
        self.state_history = game_history 
        self.debug = debug
        for board_state in game_history:
            frame_str = "turn: " + str(board_state.turn) + "\n"
            i = 0
            for line in board_state.cells:
                j = 0
                while j < (len(board_state.cells) - i):
                    frame_str += "  "
                    j += 1
                for cell in line:
                    if cell == None:
                        if debug == True:
                            frame_str += ".   "
                        else:
                            frame_str += "    "
                    else:
                        if cell.state == domain.State.EMPTY:
                            frame_str += "○   "
                        if cell.state == domain.State.OCCUPIED:
                            frame_str += "●   "
                        if cell.state == domain.State.SELECTED:
                            frame_str += "◎   "
                frame_str += "\n"
                i += 1
            self.frames.append(frame_str)
    
    def print_last(self) -> None:
        print(self.frames[-1])
            
    def run(self, frame_rate: float) -> None:
        if self.debug == False:
            os.system('clear')
        for f in self.frames:
            print(f)
            sleep(frame_rate)
            if self.debug == False:
                os.system('clear')
