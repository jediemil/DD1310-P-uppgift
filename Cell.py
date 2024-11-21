class Cell:
    def __init__(self, x, y):
        self.queue_to_change = False
        self.is_alive = False
        self.last_simulated_generation = 0
        self.pos_x = x
        self.pos_y = y
