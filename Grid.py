from threading import get_ident

from Cell import Cell

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.alive_set = set()

    def add_alive_cells(self, coord_set):
        for x, y in coord_set:
            cell = self.grid[x][y]
            self.alive_set.add(cell)
            cell.is_alive = True

    def __str__(self):
        grid_list = [["░░ " for _ in range(self.height)] for _ in range(self.width)]
        for cell in self.alive_set:
            x = cell.pos_x
            y = cell.pos_y
            grid_list[x][y] = "██ "

        str_rows = []
        for row in grid_list:
            str_rows.append("".join(row))
        return "\n".join(str_rows)
