from sys import path

path.append(r'/home/nikita/Code-Battle-Tetris/CodeBattlePython/')

from tetris_client import Point
from tetris_client import Element
from tetris_client import Board
from tetris_client import TetrisAction
from typing import Text
import logging
import random
from tetris_client import GameClient
from datetime import datetime

from fall_an import table_after_fall, find_empty


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)

k = 1


def get_first_empty_for_O(gcb: Board, y) -> int:
    x = 0
    while (x < 17) and ((gcb.get_element_at(Point(x, y)).get_char() != ".") or (gcb.get_element_at(Point(x+1, y)).get_char() != ".")):
        x += 1
    return x


def get_first_empty_for_I(gcb: Board, y) -> int:
    x = 0
    while (x < 18) and (gcb.get_element_at(Point(x, y)).get_char() != "."):
        x += 1
    return x


def board_to_list(gcb: Board) -> list:
    list_of_dot = []
    for y in range(17, -1, -1):
        is_row_empty = True
        for x in range(0, 18):
            if gcb.get_element_at(Point(x, y)).get_char() != ".":
                list_of_dot.append((x, y))
                is_row_empty = False
        if is_row_empty:
            break
    if (8,0) in list_of_dot:
        list_of_dot.remove((8,0))
    
    if (8,1) in list_of_dot:
        list_of_dot.remove((8,1))
    
    if (9,0) in list_of_dot:
        list_of_dot.remove((9,0))
    
    if (9,1) in list_of_dot:
        list_of_dot.remove((9,1))

    return list_of_dot

def find_best_action(gcb: Board):
    figure = gcb.get_current_element()
    y = gcb.get_current_figure_point().get_y()
    best_score = 100000
    best_x=0
    best_rotate=0
    for x in range(0, 18):
        for rotate in range(0, 4):
            board = table_after_fall([(temp._x, 17 - temp._y) for temp in gcb.predict_figure_points_after_rotation(x, y, figure, rotate)], board_to_list(gcb))
            min_y = min([y_coord[1] for y_coord in board])
            score = (find_empty(board) + 1) * (18 - min_y)
            if score < best_score:
                best_score = score
                best_x = x
                best_rotate = rotate
    print(best_score)
    return best_x, best_rotate


def turn(gcb: Board) -> TetrisAction:
    start_time = datetime.now()
    x, rotate = find_best_action(gcb)
    #print("empty: ", find_empty(board_to_list(gcb)))
    action = []
    action.extend([TetrisAction.ACT]*rotate)
    action.extend([TetrisAction.LEFT] * 10)
    action.extend([TetrisAction.RIGHT] * x)
    action.append(TetrisAction.DOWN)
    end_time = datetime.now()
    print((end_time - start_time).total_seconds() * 1000)
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
