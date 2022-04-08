from Game import Game
from Ball import Ball
from Size import Size

import random


class GameService:
    pass

    @staticmethod
    def start_game(game: Game):
        for i in range(5):
            key = random.choice(game.get_empty_cell())
            game.area[key] = Ball(Size.big, random.choice(game.color))

        for i in range(3):
            key = random.choice(game.get_empty_cell())
            game.area[key] = Ball(Size.small, random.choice(game.color))

        GameService.rework_graph(game)

    @staticmethod
    def choose_cell(game: Game, cell: tuple):
        if GameService.is_big_ball(game, cell[0], cell[1]):
            game.choosing_cell = cell

    @staticmethod
    def end_move(game: Game):
        for key in game.area.keys():
            if GameService.is_small_ball(game, key[0], key[1]):
                game.area.get(key).size = Size.big
                GameService.delete_balls(game, key)
        for i in range(3):
            if len(game.get_empty_cell()) == 0:
                break
            key = random.choice(game.get_empty_cell())
            game.area[key] = Ball(Size.small, random.choice(game.color))
        game.choosing_cell = None
        GameService.rework_graph(game)

    @staticmethod
    def is_big_ball(game: Game, row: int, col: int):
        return game.area.get((row, col)) is not None and game.area.get((row, col)).size == Size.big

    @staticmethod
    def is_small_ball(game: Game, row: int, col: int):
        return game.area.get((row, col)) is not None and game.area.get((row, col)).size == Size.small

    @staticmethod
    def move(game: Game, cell: tuple):
        if game.choosing_cell is None:
            GameService.choose_cell(game, cell)
        else:
            GameService.move_ball(game, game.choosing_cell, cell)

    @staticmethod
    def move_ball(game: Game, cell_start: tuple, cell_end: tuple):
        if GameService.can_move_ball(game, cell_start, cell_end):
            color = None
            if GameService.is_small_ball(game, cell_end[0], cell_end[1]):
                color = game.area.get(cell_end).color
            game.area[cell_end] = game.area.get(cell_start)
            game.area[cell_start] = None
            GameService.delete_balls(game, cell_end)
            if color is not None:
                key = random.choice(game.get_empty_cell())
                game.area[key] = Ball(Size.big, color)
                GameService.delete_balls(game, key)
            GameService.end_move(game)
        elif GameService.is_big_ball(game, cell_end[0], cell_end[1]):
            GameService.choose_cell(game, cell_end)

    @staticmethod
    def delete_balls(game: Game, cell: tuple):
        hor_balls = [cell]
        ver_balls = [cell]
        down_up_balls = [cell]
        up_down_balls = [cell]
        while True:
            end = False
            if GameService.search_line(game, hor_balls, 0, 0, -1):
                hor_balls.insert(0, (hor_balls[0][0], hor_balls[0][1] - 1))
                end = True
            if GameService.search_line(game, hor_balls, -1, 0, 1):
                hor_balls.append((hor_balls[-1][0], hor_balls[-1][1] + 1))
                end = True

            if GameService.search_line(game, ver_balls, 0, -1, 0):
                ver_balls.insert(0, (ver_balls[0][0] - 1, ver_balls[0][1]))
                end = True
            if GameService.search_line(game, ver_balls, -1, 1, 0):
                ver_balls.append((ver_balls[-1][0] + 1, ver_balls[-1][1]))
                end = True

            if GameService.search_line(game, down_up_balls, 0, 1, -1):
                down_up_balls.insert(0, (down_up_balls[0][0] + 1, down_up_balls[0][1] - 1))
                end = True
            if GameService.search_line(game, down_up_balls, -1, -1, 1):
                down_up_balls.append((down_up_balls[-1][0] - 1, down_up_balls[-1][1] + 1))
                end = True

            if GameService.search_line(game, down_up_balls, 0, 1, -1):
                down_up_balls.insert(0, (down_up_balls[0][0] + 1, down_up_balls[0][1] - 1))
                end = True
            if GameService.search_line(game, down_up_balls, -1, -1, 1):
                down_up_balls.append((down_up_balls[-1][0] - 1, down_up_balls[-1][1] + 1))
                end = True

            if GameService.search_line(game, up_down_balls, 0, -1, -1):
                up_down_balls.insert(0, (up_down_balls[0][0] - 1, up_down_balls[0][1] - 1))
                end = True
            if GameService.search_line(game, up_down_balls, -1, 1, 1):
                up_down_balls.append((up_down_balls[-1][0] + 1, up_down_balls[-1][1] + 1))
                end = True
            if not end:
                break
        deleted = False
        if GameService.delete_line(game, hor_balls):
            deleted = True
        if GameService.delete_line(game, ver_balls):
            deleted = True
        if GameService.delete_line(game, up_down_balls):
            deleted = True
        if GameService.delete_line(game, down_up_balls):
            deleted = True
        if deleted:
            game.points = game.points + 1

    @staticmethod
    def search_line(game: Game, balls, index: int, row: int, col: int):
        if 0 <= balls[index][1] + col < game.size and 0 <= balls[index][0] + row < game.size and \
                GameService.is_big_ball(game, balls[index][0] + row, balls[index][1] + col) and \
                game.area.get((balls[index][0] + row, balls[index][1] + col)).color == game.area.get(
            (balls[index][0], balls[index][1])).color:
            return True
        return False

    @staticmethod
    def delete_line(game: Game, balls):
        if len(balls) >= game.count_balls_line:
            for ball in balls:
                game.area[ball] = None
            game.points = game.points + len(balls) - 1
            return True

        return False

    @staticmethod
    def can_move_ball(game: Game, cell_start: tuple, cell_end: tuple):
        if GameService.is_big_ball(game, cell_end[0], cell_end[1]):
            return False
        return GameService.is_reachable(game, cell_start, cell_end)

    @staticmethod
    def is_reachable(game: Game, s: tuple, d: tuple):
        keys = game.area.keys()
        visited = dict()
        for i in keys:
            visited[i] = False

        # Создать очередь для BFS

        queue = [s]

        # Отметить исходный узел как посещенный и поставить его в очередь

        visited[s] = True

        while queue:

            # Удалить вершину из очереди

            n = queue.pop(0)

            # Если этот соседний узел является узлом назначения,

            # затем верните true

            if n == d:
                return True

            for i in game.graph.adj_lists[n]:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True

        return False

    @staticmethod
    def rework_graph(game: Game):
        for cell in game.area.keys():
            game.graph.adj_lists[cell] = []
            for adj in GameService.get_adj_cell(game, cell):
                if game.area.get(adj) is None or game.area.get(adj).size == Size.small:
                    game.graph.adj_lists[cell].append(adj)

    @staticmethod
    def is_game_over(game: Game):
        for key in GameService.get_big_ball_cell(game):
            for cell in game.area.keys():
                if GameService.is_big_ball(game, cell[0], cell[1]):
                    continue

                if GameService.can_move_ball(game, key, cell):
                    return False

        return True

    @staticmethod
    def get_adj_cell(game: Game, cell: tuple):
        cells = []
        if cell[0] - 1 >= 0:
            cells.append((cell[0] - 1, cell[1]))

        if cell[0] + 1 < game.size:
            cells.append((cell[0] + 1, cell[1]))

        if cell[1] - 1 >= 0:
            cells.append((cell[0], cell[1] - 1))

        if cell[1] + 1 < game.size:
            cells.append((cell[0], cell[1] + 1))

        return cells

    @staticmethod
    def get_big_ball_cell(game: Game):
        big_ball_cells = []
        for key in game.area.keys():
            if GameService.is_big_ball(game, key[0], key[1]):
                big_ball_cells.append(key)

        return big_ball_cells
