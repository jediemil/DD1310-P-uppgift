from threading import get_ident

from Cell import Cell

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y, width, height) for y in range(height)] for x in range(width)]
        self.alive_set = set()
        self.generation = -1

    def add_alive_cells(self, coord_set):
        for x, y in coord_set:
            print(x, y)
            cell = self.grid[x][y]
            print(cell.pos_x, cell.pos_y)
            self.alive_set.add(cell)
            cell.is_alive = True
            cell.change_to = True

    def simulate_step(self, generation):
        next_alive_cells = self.alive_set.copy()

        for cell in self.alive_set:
            alive_neighbors = cell.check_alive_neighbors(self.grid, generation) - 1
            if alive_neighbors != 2 and alive_neighbors != 3:
                cell.kill(generation)
                next_alive_cells.remove(cell)

            revive_cells = cell.ping_dead_neighbors(self.grid, generation)
            for revive_cell in revive_cells:
                revive_cell.revive(generation)
                next_alive_cells.add(revive_cell)

        self.alive_set = next_alive_cells
        print(f"Alive: {generation}")
        for cell in self.alive_set:
            print(cell)
        print()
        self.generation = generation # debug
        print(len(self.alive_set)) # debug

    def __str__(self):
        """grid_list = [["░░ " for _ in range(self.height)] for _ in range(self.width)]
        for cell in self.alive_set:
            x = cell.pos_x
            y = cell.pos_y
            grid_list[x][y] = "██ "

        str_rows = []
        for row in grid_list:
            str_rows.append("".join(row))
        return "\n".join(str_rows)"""
        string = ""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[x][y].check_alive(self.generation):
                    string += "██ "
                else:
                    string += "░░ "
            string += "\n"
        return string

