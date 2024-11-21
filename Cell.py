class Cell:
    def __init__(self, x, y, grid_width, grid_height):
        self.queue_to_change = False
        self.change_to = False # debug
        self.is_alive = False
        self.last_simulated_generation = -1
        self.pos_x = x
        self.pos_y = y

        self.__top_min = max(0, x - 1)
        self.__bottom_max = min(grid_height - 1, x + 1)
        self.__left_min = max(0, y - 1)
        self.__right_max = min(grid_width - 1, y + 1)

    def check_alive(self, generation):
        if self.queue_to_change and generation != self.last_simulated_generation:
            self.queue_to_change = False
            self.is_alive = self.change_to

        return self.is_alive

    def kill(self, generation):
        self.queue_to_change = True
        self.last_simulated_generation = generation
        self.change_to = False

    def revive(self, generation):
        self.queue_to_change = True
        self.last_simulated_generation = generation
        self.change_to = True

    def check_alive_neighbors(self, grid, generation):
        found_alive_neighbors = 0
        self.last_simulated_generation = generation
        for y in range(self.__left_min, self.__right_max + 1):
            for x in range(self.__top_min, self.__bottom_max + 1):
                if grid[x][y].is_alive: # if grid[x][y].check_alive(generation):
                    found_alive_neighbors += 1

        return found_alive_neighbors


    def ping_dead_neighbors(self, grid, generation):
        revive_cells = set()
        for x in range(self.__left_min, self.__right_max + 1):
            for y in range(self.__top_min, self.__bottom_max + 1):
                cell = grid[x][y]
                if cell.last_simulated_generation != generation and not cell.is_alive: # and not cell.check_alive(generation):
                    neighbors = self.check_alive_neighbors(grid, generation)
                    print(f"{x}, {y} hittade {neighbors} (från {self.pos_x, self.pos_y})")
                    if neighbors == 3:
                        revive_cells.add(cell)

        return revive_cells

