class Cell:
    torus = None
    grid_width = None
    grid_height = None

    def __init__(self, x, y):
        self.queue_to_change = False
        self.is_alive = False
        self.last_simulated_generation = -1
        self.pos_x = x
        self.pos_y = y

        self.__top_min = max(0, y - 1)
        self.__bottom_max = min(self.grid_height - 1, y + 1)
        self.__left_min = max(0, x - 1)
        self.__right_max = min(self.grid_width - 1, x + 1)

    def check_alive(self, generation):
        if self.queue_to_change and generation != self.last_simulated_generation:
            self.queue_to_change = False
            self.is_alive = not self.is_alive

        return self.is_alive

    def kill(self, generation):
        self.queue_to_change = True
        self.last_simulated_generation = generation
        # print(f"Kill {self.pos_x} {self.pos_y}")

    def revive(self, generation):
        self.queue_to_change = True
        self.last_simulated_generation = generation
        # print(f"Revive {self.pos_x} {self.pos_y}")

    def check_alive_neighbors(self, grid, generation):
        found_alive_neighbors = 0
        self.check_alive(generation)
        self.last_simulated_generation = generation

        for cell in self.__get_neighboring_cells(grid):
            if cell.check_alive(generation):
                found_alive_neighbors += 1
                # print(f"{self.pos_x},{self.pos_y} found {x}, {y}")

        return found_alive_neighbors

    def ping_dead_neighbors(self, grid, generation):
        revive_cells = set()
        for cell in self.__get_neighboring_cells(grid):
            if cell.last_simulated_generation != generation and not cell.check_alive(generation):
                neighbors = cell.check_alive_neighbors(grid, generation)
                # print(f"{x}, {y} hittade {neighbors} (från {self.pos_x, self.pos_y})")

                if neighbors == 3:
                    revive_cells.add(cell)

        return revive_cells

    def __get_neighboring_cells(self, grid):
        cells = set()
        if self.torus:
            for x in range(self.pos_x - 1, self.pos_x + 2):
                for y in range(self.pos_y - 1, self.pos_y + 2):
                    cell = grid[x % self.grid_width][y % self.grid_height]
                    cells.add(cell)
        else:
            for x in range(self.__left_min, self.__right_max + 1):
                for y in range(self.__top_min, self.__bottom_max + 1):
                    cell = grid[x][y]
                    cells.add(cell)

        return cells

    def __str__(self):
        return f"Cell: {self.pos_x}, {self.pos_y}, alive: {self.is_alive}, queue: {self.queue_to_change}, last_gen: {self.last_simulated_generation}"
