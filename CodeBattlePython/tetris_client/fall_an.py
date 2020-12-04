from functools import reduce

from tetris_client import Board, Element, Point


def table_after_fall(figure_coors: Element, current_board: list) -> list:
    print(current_board)
    if not current_board:
        return current_board
    collision = False
    collision_points = []
    new_board = current_board.copy()
    for pnt in figure_coors:
        if Point(pnt.get_x(), pnt.get_y()-1) in figure_coors:
            continue
        else:
            collision_points.append(Point(pnt.get_x(), pnt.get_y()))
    delta = 1
    while collision == False:
        shifted_points = [Point(pnt.get_x(), pnt.get_y()+delta) for pnt in collision_points]
        #print([i.get_y() for i in shifted_points])
        for pnt in shifted_points:
            if (pnt.get_x(), pnt.get_y()) in current_board:
                print(pnt.get_x(), pnt.get_y())
                collision = True
                for pnt_temp in figure_coors:
                    new_board.append((pnt_temp.get_x(), pnt_temp.get_y()+delta-1))
            else:
                break
        delta += 1
        if delta >=16:
            delta = 1
            break
    return new_board

def find_empty(current_board: list, current_bord_state: Board) -> int:
    if not current_board:
        return 0
    empty_counter = 0
    min_y = min([y_coord[1] for y_coord in current_board])
    for height in range(17-max_y):
        for width in range(18):
            if (width, height) not in current_board:
                for pnts in range(height, 18, 1):
                    if current_bord_state.get_element_at(Point(width, pnts)).get_char() != ".":
                        empty_counter += 1
                        break
    return empty_counter
