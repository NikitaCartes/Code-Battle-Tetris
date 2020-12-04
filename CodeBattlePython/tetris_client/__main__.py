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

from fall_an import table_after_fall

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
    return list_of_dot

def find_best_action(gcb: Board):
    y=gcb.get_current_element
    for x in range(1, 17):
        for rotate in range(0, 4):
            table_after_fall([(temp._x, 17 - temp._y) for temp in gcb.predict_figure_points_after_rotation(x, y, figure, rotate)], board_to_list(gcb))

def turn(gcb: Board) -> TetrisAction:
    start_time = datetime.now()
    table_after_fall([(temp._x, 17 - temp._y) for temp in gcb.predict_figure_points_after_rotation()], board_to_list(gcb))
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
