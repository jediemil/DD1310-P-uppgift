from Cell import Cell


class Grid:
    """
    En klass som sköter spelbrädet i game of life. Den innehåller ett tvådimensionellt grid av celler och hjälpmetoder för
    att köra simulationen.

    Attribut:
    width : int
    height : int
    grid : list[list[Cell]]
    alive_set : set[tuple[int, int]]
    torus : bool
    """

    def __init__(self, width, height, torus):
        """Konstruktormetoden för Grid. Skapar spelbrädet och fyller det med döda celler.
        :param width: Bredden på brädet i antal celler
        :type width: int
        :param height: Höjden på brädet i antal celler
        :type height: int
        :param torus: Om true beter sig spelbrädet som en torus
        :type torus: bool"""

        self.width = width
        self.height = height

        # Sätter globala konstanter för alla instanser av Cell
        Cell.grid_width = width
        Cell.grid_height = height
        Cell.torus = torus

        # Generera en matris av Celler med hjälp av list comprehension
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]

        self.alive_set = set()
        self.torus = torus

    def add_alive_cells(self, coord_set):
        """Ändrar cellerna i coord_set till levande celler på spelbrädet.
        :param coord_set: Ett set med koordineter till celler som ska återupplivas.
        :type coord_set: set[tuple[int, int]]"""

        for x, y in coord_set:
            cell = self.grid[x][y]
            self.alive_set.add(cell)
            cell.queue_to_change = False
            cell.is_alive = True

    def kill_cells(self, coord_set):
        """Ändrar cellerna i coord_set till döda celler på spelbrädet.
        :param coord_set: Ett set med koordineter till celler som ska dödas.
        :type coord_set: set[tuple[int, int]]"""

        for x, y in coord_set:
            cell = self.grid[x][y]
            self.alive_set.discard(cell)
            cell.queue_to_change = False
            cell.is_alive = False

    def simulate_step(self, generation):
        """Simulerar ett steg av Game of Life. Metoden går genom alla levande celler och byter sedan ut
        alive_set mot de celler som lever nästa generation
        :param generation: Generationen som det här steget gäller
        :type generation: int"""

        next_alive_cells = self.alive_set.copy()  # Antar att alla celler överlever

        for cell in self.alive_set:
            # Ber alla levande celler att räkna antal levande grannar (-1 eftersom att den räknar med sig själv)
            alive_neighbors = cell.check_alive_neighbors(self.grid, generation) - 1
            if alive_neighbors != 2 and alive_neighbors != 3:  # Enligt reglerna till Game of Life
                # Dödar cellen och tar bort den från mängden av levande celler
                cell.kill(generation)
                next_alive_cells.remove(cell)

            # Ber alla levande celler att be alla sina döda grannar räkna om de ska pånyttfödas denna generation
            revive_cells = cell.ping_dead_neighbors(self.grid, generation)
            # Varje cell returnerar en mängd med de celler som ska pånyttfödas
            for revive_cell in revive_cells:
                revive_cell.revive(generation)
                next_alive_cells.add(revive_cell)

        self.alive_set = next_alive_cells

    def __str__(self):
        """Konverterar spelbrädet till en användarvänlig sträng för utskrift. Metoden undviker att loopa genom hela spelbrädet.
        :returns: En textrepresentation av spelbrädet
        :rtype: str"""

        # Skapa en lista fylld med tomma listor
        rows = [[] for _ in range(self.height)]

        # Lägg in levande cellers x-koordinat i de tomma listorna för varje motsvarande y-koordinat
        for cell in self.alive_set:
            rows[cell.pos_y].append(cell.pos_x)

        # Skapar en lista som ska innehålla varje rad av utskriften
        str_rows = []

        for row in rows:
            # Sortera cellerna i listan enligt x-koordinat
            row.sort()

            if row:
                str_row = "░░ " * row[0] + "██ "  # Första delen av raden -> tom plats till första cellen
                for i, x in enumerate(row[1:]):  # Loopa genom resterande celler på raden
                    str_row += "░░ " * (row[i + 1] - row[i] - 1) + "██ "  # Tom plats till nästa cell

                str_row += "░░ " * (self.width - row[-1] - 1)  # Tom plats till slutet på brädet
            else:
                str_row = "░░ " * self.width  # Om raden är tom printas hela raden som tom

            str_rows.append(str_row)

        return "\n".join(str_rows)  # Lägger ihop hela listan till en lång sträng med "\n" mellan varje listelement
