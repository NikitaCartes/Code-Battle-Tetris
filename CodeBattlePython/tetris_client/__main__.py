from sys import path

#path.append(r'/home/AstralRomance/code_battle/Code-Battle-Tetris/CodeBattlePython/')

from tetris_client import GameClient
import random
import logging
from typing import Text
from tetris_client import TetrisAction
from tetris_client import Board
from tetris_client import Element
from tetris_client import Point

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)

index = 0
# Number of deleted rows
score_counter = 0
# Current round
round_counter = 1
# Flag to check line refresh
is_refreshed = False


def is_line_refreshed(board_state):
    global is_refreshed, score_counter, round_counter
    if score_counter >= 20:
        round_counter += 1
        score_counter = 0
    print('*******\n')
    print(is_refreshed, score_counter)

    if round_counter == 1:
        if (board_state.get_element_at(Point(17, 17)).get_char() != '.'):
            is_refreshed = True
        if (board_state.get_element_at(Point(17, 17)).get_char() == '.') and (is_refreshed == True):
            score_counter += 2
            is_refreshed = False
            
    

def turn(gcb: Board) -> TetrisAction:
    # this function must return list actions from TetrisAction: tetris_client/internals/tetris_action.py
    #     LEFT = 'left'
    #     RIGHT = 'right'
    #     DOWN = 'down'
    #     ACT = 'act'
    #     ACT_2 = 'act(2)'
    #     ACT_3 = 'act(3),'
    #     ACT_0_0 = 'act(0,0)'
    # change return below to your code (right now its returns random aciton):
    # код ниже является примером и сэмплом для демонстрации - после подстановки корректного URI к своей игре
    # запустите клиент и посмотрите как отображаются изменения в UI игры и что приходит как ответ от API
    # elem = gcb.get_current_figure_type()
    #print(gcb.get_future_figures())
    #print(gcb.get_current_figure_point())
    #print(gcb.get_current_figure_type())
    #print(gcb.find_element(elem))
    # predict_figure_points_after_rotation - предсказывает положение фигуры после вращения
    #print('rotate prediction: ', gcb.predict_figure_points_after_rotation(rotation=3))
    
    #actions = [x for x in TetrisAction if x.value != "act(0,0)"]
    
    # return [TetrisAction.LEFT] - example how to send only one action, list with 1 element
    
    # ROUND 1
    global index
    global round_counter
    is_line_refreshed(gcb)
    if round_counter == 1:
        index = (index + 2) % 18
        action = [TetrisAction.LEFT] * 10
        action.extend([TetrisAction.RIGHT]*index)
        action.append(TetrisAction.DOWN)
        return action
    else:
        index = (index + 2) % 18
        action = [TetrisAction.LEFT] * 10
        action.extend([TetrisAction.RIGHT]*index)
        action.append(TetrisAction.DOWN)
        return action
    # это те действия, которые выполнятся на игровом сервере в качестве вашего хода


def main(uri: Text):
    """
    uri: url for codebattle game
    """
    gcb = GameClient(uri)
    gcb.run(turn)


if __name__ == "__main__":
    # в uri переменную необходимо поместить url с игрой для своего пользователя
    # put your game url in the 'uri' path 1-to-1 as you get in UI
    uri = "http://codebattle2020.westeurope.cloudapp.azure.com/codenjoy-contest/board/player/ughx7b2ws78dix93nqvf?code=940325171272210979&gameName=tetris"
    main(uri)
