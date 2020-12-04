from tetris_client import Board, Element, Point


def table_after_fall(figure_coors: list, current_board: list) -> list:
    collision = False
    collision_points = []
    new_board = current_board.copy()
    for pnt in figure_coors:
        if (pnt[0], pnt[1]+1) in figure_coors:
            continue
        else:
            collision_points.append((pnt[0], pnt[1]))
    delta = 1
    lowest_point = max(figure_coors, key=lambda t: t[1])[1]
    while collision == False:
        shifted_points = [(pnt[0], pnt[1]+delta) for pnt in collision_points]
        for pnt in shifted_points:
            if (pnt[0], pnt[1]) in current_board:
                collision = True
                for pnt_temp in figure_coors:
                    new_board.append( (pnt_temp[0], pnt_temp[1]+delta-1))
        delta += 1
        if lowest_point + delta > 17:
            for pnt_temp in figure_coors:
                new_board.append( (pnt_temp[0], pnt_temp[1]+delta-1))
            break

    return new_board
