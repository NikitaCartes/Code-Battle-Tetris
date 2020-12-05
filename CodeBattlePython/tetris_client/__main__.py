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


#logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)

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

def count_full_lines(current_board: list) -> int:
    full_lines = 0
    for y in range(17, -1, -1):
        is_row_empty = True
        is_row_has_empty = False
        for x in range(0, 18):
            if (x, y) in current_board:
                is_row_empty = False
            else:
                is_row_has_empty = True
                break
        if not is_row_has_empty:
            full_lines += 1
        if is_row_empty:
            break
    return full_lines

def count_fullness(current_board: list) -> int:
    fullness = 1
    for y in range(17, -1, -1):
        is_row_empty = True
        for x in range(0, 18):
            if (x, y) in current_board:
                fullness += 1*pow(20, y)
                is_row_empty = False
        if is_row_empty:
            break
    return fullness

def get_min_max_x(figure_coors: list, current_board: list):
    collision = False
    collision_points = []
    new_board = current_board.copy()
    for pnt in figure_coors:
        if (pnt[0]+1, pnt[1]) in figure_coors:
            continue
        else:
            collision_points.append((pnt[0], pnt[1]))
    delta = 1
    lowest_point = max(figure_coors, key=lambda t: t[0])[0]
    while collision == False:
        shifted_points = [(pnt[0]+delta, pnt[1]) for pnt in collision_points]
        for pnt in shifted_points:
            if (pnt[0], pnt[1]) in current_board:
                collision = True
                for pnt_temp in figure_coors:
                    new_board.append( (pnt_temp[0]+delta-1, pnt_temp[1]))
        delta += 1
        if lowest_point + delta > 17:
            for pnt_temp in figure_coors:
                new_board.append( (pnt_temp[0]+delta-1, pnt_temp[1]))
            break
    max_delta = delta

    collision = False
    collision_points = []
    new_board = current_board.copy()
    for pnt in figure_coors:
        if (pnt[0]-1, pnt[1]) in figure_coors:
            continue
        else:
            collision_points.append((pnt[0], pnt[1]))
    delta = 1
    lowest_point = min(figure_coors, key=lambda t: t[0])[0]
    while collision == False:
        shifted_points = [(pnt[0]-delta, pnt[1]) for pnt in collision_points]
        for pnt in shifted_points:
            if (pnt[0], pnt[1]) in current_board:
                collision = True
                for pnt_temp in figure_coors:
                    new_board.append( (pnt_temp[0]-delta+1, pnt_temp[1]))
        delta += 1
        if lowest_point - delta < 1:
            for pnt_temp in figure_coors:
                new_board.append( (pnt_temp[0]-delta+1, pnt_temp[1]))
            break
    min_delta = -delta

    return min_delta, max_delta
    

def find_best_action(gcb: Board):
    board_list = board_to_list(gcb)
    best_score = 100000
    best_delta = 0
    best_rotate = 0
    best_fullness = 0
    min_delta, max_delta = (0, 0)
    for rotate in range(0, 4):
        figure = [(temp._x, 17 - temp._y) for temp in gcb.predict_figure_points_after_rotation(rotation=rotate)]
        min_delta, max_delta = get_min_max_x(figure, board_list)
        for delta in range(min_delta, max_delta):
            board = table_after_fall([(temp[0]+delta, temp[1]) for temp in figure], board_list)
            min_y = min([y_coord[1] for y_coord in board])
            full_lines = count_full_lines(board)
            #temp = 0
            #if full_lines < 3:
            #    temp = full_lines * 4
            #else:
            #    temp = full_lines * (-4)
            score = (find_empty(board) + 20)*15 + (18 - min_y - full_lines*3)
            if score < best_score:
                best_score = score
                best_delta = delta
                best_rotate = rotate
            elif score == best_score:
                fullness = count_fullness(board)
                if fullness >= best_fullness:     
                    best_score = score
                    best_delta = delta
                    best_rotate = rotate
                    best_fullness = fullness
    print("Score: ", best_score)
    print("Fullness: ", best_fullness)
    print(min_delta, max_delta)
    return best_delta, best_rotate


def turn(gcb: Board) -> TetrisAction:
    start_time = datetime.now()
    delta, rotate = find_best_action(gcb)
    #print("empty: ", find_empty(board_to_list(gcb)))
    
    action = [TetrisAction.ACT]*rotate
    
    if delta < 0:
        action.extend([TetrisAction.LEFT] * (-delta))
    else:
        action.extend([TetrisAction.RIGHT] * delta)
    action.append(TetrisAction.DOWN)
    end_time = datetime.now()
    print("Time: ", (end_time - start_time).total_seconds() * 1000)
    print("===========================================================")
    return action


def main(uri: Text):
    """
    uri: url for codebattle game
    """
    gcb = GameClient(uri)
    gcb.run(turn)


if __name__ == "__main__":
    uri = "http://codebattle2020.westeurope.cloudapp.azure.com/codenjoy-contest/board/player/ughx7b2ws78dix93nqvf?code=940325171272210979&gameName=tetris#"
    main(uri)
