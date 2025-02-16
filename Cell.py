# Av Emil Reyier Hedin 2024-11-21. Senast ändrad 2025-02-16

class Cell:
    """En klass som håller koll på en individuell cell i Game of Life.
    Cellen håller själv reda på om den lever eller inte utifrån nuvarande generation.
    För att kolla om cellen lever eller inte ska check_alive()-metoden användas.

    Attribut:
    queue_to_change : bool True om cellen ska byta levnadsstatus nästa generation
    is_alive : bool Cellens levnadsstatus
    last_simulated_generation : int Senaste generationen som cellen fick sin levnadsstatus bekräftad
    pos_x : int Cellens x-koordinat i spelbrädet
    pos_y : int Cellens y-koordinat i spelbrädet

    Globala attribut:
    torus : bool True om spelplanen ska bete sig som en torus
    grid_width : int Spelbrädets vidd
    grid_height : int Spelbrädets höjd"""

    # Globala attribut för Cell
    torus = None
    grid_width = None
    grid_height = None

    def __init__(self, x, y):
        """Konstruktorn till Cellklassen. Den skapar cellen och sätter värden på alla attribut.
        :param x: Cellens x-koordinat
        :type x: int
        :param y: Cellens y-koordinat
        :type y: int"""
        self.queue_to_change = False
        self.is_alive = False
        self.last_simulated_generation = -1
        self.pos_x = x
        self.pos_y = y

        # Används för att cellen inte ska försöka hitta celler utanför spelbrädet
        self.__top_min = max(0, y - 1)
        self.__bottom_max = min(self.grid_height - 1, y + 1)
        self.__left_min = max(0, x - 1)
        self.__right_max = min(self.grid_width - 1, x + 1)

    def kill(self, generation):
        """Säger åt cellen att presentera sig som död i framtida generationer.
        !VARNING! Ropas kill() på en redan död cell kommer den presentera sig som levande.
        :param generation: Nuvarande generation
        :type generation: int"""

        self.queue_to_change = True
        self.last_simulated_generation = generation
        # print(f"Kill {self.pos_x} {self.pos_y}")

    def revive(self, generation):
        """Säger åt cellen att presentera sig som levande i framtida generationer.
        !VARNING! Ropas revive() på en redan levande cell kommer den presentera sig som död.
        :param generation: Nuvarande generation
        :type generation: int"""

        self.queue_to_change = True
        self.last_simulated_generation = generation
        # print(f"Revive {self.pos_x} {self.pos_y}")

    def check_alive(self, generation):
        """Ber cellen att kolla om den lever eller inte, cellen svarar inte förrän
        en generation efter att den har dött eller återuppstått.
        :param generation: Nuvarande generation
        :type generation: int
        :return: True om cellen lever, False om cellen är död
        :rtype: bool"""

        if self.queue_to_change and generation != self.last_simulated_generation:
            self.queue_to_change = False
            self.is_alive = not self.is_alive

        return self.is_alive

    def check_alive_neighbors(self, grid, generation):
        """Räknar och returnerar antal levande celler i en 3x3 ruta med self i centrum.
        :param grid: En matris med alla celler
        :type grid: list[list[Cell]]
        :param generation: Nuvarande generation
        :type generation: int
        :returns: Antal levande grannar + cellen själv
        :rtype: int"""

        found_alive_neighbors = 0
        self.check_alive(generation)
        self.last_simulated_generation = generation

        for cell in self.__get_neighboring_cells(grid):
            if cell.check_alive(generation):
                found_alive_neighbors += 1
                # print(f"{self.pos_x},{self.pos_y} found {x}, {y}")

        return found_alive_neighbors

    def ping_dead_neighbors(self, grid, generation):
        """Alla döda celler runt self kommer att räkna sina levande grannar, och metoden avgör om den döda
        cellen ska återupplivas. Metoden returnerar sedan en mängd av koordinater på de celler som ska återupplivas.
        :param grid: En matris med alla celler
        :type grid: list[list[Cell]]
        :param generation: Nuvarande generation
        :type generation: int
        :returns: Celler som ska återupplivas
        :rtype: set[tuple[int, int]]"""

        revive_cells = set()
        for cell in self.__get_neighboring_cells(grid):
            # Ber cellen räkna sina grannar om den inte redan har gjort det den här generationen och är död
            if cell.last_simulated_generation != generation and not cell.check_alive(generation):
                neighbors = cell.check_alive_neighbors(grid, generation)
                if neighbors == 3:
                    # Om cellen har exakt 3 levande grannar ska den återupplivas
                    revive_cells.add(cell)

        return revive_cells

    def __get_neighboring_cells(self, grid):
        """En privat metod för att hitta alla omkringliggande celler till self. Här räknas self som
        en granne till self och kommer därför finnas med i returneringen
        :param grid: En matris med alla celler
        :type grid: list[list[Cell]]
        :returns: En mängd med alla grannceller
        :rtype: set[Cell]"""

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
        """Metoden konverterar cellens viktiga attribut till en sträng på ett lättläst sätt
        :returns: En strängrepresentation av cellens attribut
        :rtype: str"""
        return f"Cell: {self.pos_x}, {self.pos_y}, alive: {self.is_alive}, queue: {self.queue_to_change}, last_gen: {self.last_simulated_generation}"
