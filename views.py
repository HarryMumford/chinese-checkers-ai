from time import sleep
import os
import domain

class Animation():
    frames = []

    def __init__(self, game_history) -> None:
        self.state_history = game_history 
        for action in game_history:
            frame_str = "turn: " + str(action.turn) + "\n"
            count = 0
            for line in action.cells:
                i = 0
                while i < 13 - len(line):
                    frame_str += "  "
                    i += 1
                for cell in line:
                    if cell.state == domain.State.EMPTY:
                        frame_str += "○   "
                    if cell.state == domain.State.OCCUPIED:
                        frame_str += "●   "
                    if cell.state == domain.State.SELECTED:
                        frame_str += "◎   "
                frame_str += "\n"
                count += 1
            self.frames.append(frame_str)
            
    def run(self, frame_rate: float) -> None:
        os.system('clear')
        for f in self.frames:
            print(f)
            sleep(frame_rate)
            os.system('clear')
