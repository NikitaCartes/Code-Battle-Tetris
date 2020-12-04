from sys import path

path.append(r'/home/nikita/Code-Battle-Tetris/CodeBattlePython/')

from tetris_client import GameClient
import random
import logging
from typing import Text
from tetris_client import TetrisAction
from tetris_client import Board
from tetris_client import Element
from tetris_client import Point

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)

k = 1

def get_first_empty_for_O(gcb: Board, y) -> int:
    x = 0
    while (x < 17) and ((gcb.get_element_at(Point(x, y)).get_char() != ".") or (gcb.get_element_at(Point(x+1, y)).get_char() != ".")):
        x +=1
    return x

def get_first_empty_for_I(gcb: Board, y) -> int:
    x = 0
    while (x < 18) and (gcb.get_element_at(Point(x, y)).get_char() != "."):
        x +=1
    return x    

def turn(gcb: Board) -> TetrisAction:
    action = [TetrisAction.LEFT] * 10
    y = 17
    x = 0
    global k
    if gcb.get_current_figure_type() == "I":
        x = 18
        while x == 18:
            x = get_first_empty_for_I(gcb, y)
            y = y - 1
    elif gcb.get_current_figure_type() == "O":
        x = 17
        while x == 17:
            x = get_first_empty_for_O(gcb, y)
            y = y - 1
    elif gcb.get_current_figure_type() == "J":
        if k % 2 == 0:
            action.append(TetrisAction.ACT_2)
        action.append(TetrisAction.LEFT)
        k += 1

    action.extend([TetrisAction.RIGHT]*x)
    action.append(TetrisAction.DOWN)
    return action


def main(uri: Text):
    """
    uri: url for codebattle game
    """
    gcb = GameClient(uri)
    gcb.run(turn)

if __name__ == "__main__":
    uri = "http://codebattle2020.westeurope.cloudapp.azure.com/codenjoy-contest/board/player/f2ifat9xda9sy6qaktq2?code=3385983798808468512&gameName=tetriss"
    main(uri)
