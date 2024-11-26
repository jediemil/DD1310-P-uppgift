from Cell import Cell


class Grid:
    def __init__(self, width, height, torus):
        self.width = width
        self.height = height
        Cell.grid_width = width
        Cell.grid_height = height
        Cell.torus = torus
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.alive_set = set()
        self.generation = 0
        self.torus = torus

    def add_alive_cells(self, coord_set):
        for x, y in coord_set:
            cell = self.grid[x][y]
            # print(cell.pos_x, cell.pos_y)
            self.alive_set.add(cell)
            cell.is_alive = True

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

    def __str__(self):
        rows = [[] for _ in range(self.height)]

        for cell in self.alive_set:
            rows[cell.pos_y].append(cell.pos_x)

        str_rows = []

        for row in rows:
            row.sort()
            # print(row)
            if row:
                str_row = "░░ " * row[0] + "██ "
                for i, x in enumerate(row[1:]):
                    str_row += "░░ " * (row[i + 1] - row[i] - 1) + "██ "

                str_row += "░░ " * (self.width - row[-1] - 1)
            else:
                str_row = "░░ " * self.width

            str_rows.append(str_row)

        return "\n".join(str_rows)
