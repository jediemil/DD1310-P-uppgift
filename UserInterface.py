# Av Emil Reyier Hedin 2024-12-02. Senast ändrad 2025-02-20

import tkinter as tk

from Grid import Grid

# Konstanter för spelet
MIN_HEIGHT_GUI = 5
MAX_HEIGHT_GUI = 10000
MIN_WIDTH_GUI = 5
MAX_WIDTH_GUI = 10000
DEFAULT_WIDTH = 200
DEFAULT_HEIGHT = 100
STEPS =  [1,    1,    1,   1,   1,   1,  1,  1,  2,  4,  8,  16, 50]
SPEEDS = [2000, 1000, 500, 250, 100, 50, 20, 10, 10, 10, 10, 10, 10]

# Konstanter för GUI
BORDER_OFFSET_PX = 0
LOWER_BUTTON_PX = 50
CANVAS_SIZE = 0.95
MINIMAL_ZOOM = 0.1
MIN_ZOOM_FOR_CELL_BORDER = 2
ZOOM_FACTOR = 0.05
RELAXED_ZOOM = True  # Tillåter zoom att gå utanför spelbrädet, vilket skapar en mer intuitiv zoom-upplevelse


def validate_num(new_val):
    """Validatorfunktion som används för att godkänna vissa typer av inmatningar i textfälten.
    :param new_val: En sträng med värdet som ska valideras
    :type new_val: str
    :return: True om strängen är tom eller representerar ett tal, annars False
    :rtype: bool"""
    return new_val.isnumeric() or new_val == ""


class UserInterface:
    """En klass som sköter användargränssnittet och även kör själva spelet parallellt med gränssnittet.

    Attribut:
    canvas_width : int Höjden på canvasen i pixlar
    canvas_height : int Höjden på canvasen i pixlar
    grid : Grid Spelbrädet som sköter simulationen
    kill_cells_queue : set[tuple[int, int]] En mängd av celler som manuellt ska dödas nästa generation
    revive_cells_queue : set[tuple[int, int]] En mängd av celler som manuellt ska återupplivas nästa generation
    zoom_level : float Storleken på en cell i pixlar
    current_generation : int Den nuvarande generationen som simuleras
    running : bool True om simulationen kör, False om den är pausad
    speed : int Anger hastigheten på simulationen
    grid_offset : tuple[int, int] Ett offset som används för zoom-funktionen
    last_clicked : tuple[int, int] x och y koordinat på senaste cellen som blev klickad av spelaren
    width : IntVar Bredden på spelbrädet som användaren angav
    height : Höjden Bredden på spelbrädet som användaren angav
    torus : BooleanVar Anger om brädet ska bete sig som en torus
    min_zoom : float Den minsta storleken en cell får vara i pixlar
    root : Tk Tkinters rotfönster
    simulation_frame_renders : int Räknar hur många gånger spelloopen har ritat om spelbrädet"""

    def __init__(self):
        """Konstruktormetoden till UserInterface. Metoden initierar attributen och skapar inställningsrutan och spelrutan."""

        self.canvas_width = 0
        self.canvas_height = 0
        self.grid = None  # Grid sätts senare när användaren har angett en storlek
        self.kill_cells_queue = set()
        self.revive_cells_queue = set()
        self.zoom_level = 10
        self.current_generation = 0
        self.running = False
        self.speed = 0
        self.grid_offset = (0, 0)
        self.last_clicked = None
        self.min_zoom = 1
        self.simulation_frame_renders = 0

        self.root = tk.Tk()  # Skapar ett fönster
        self.root.geometry("400x400")

        # Variabler kopplade till inputfälten i inställningsrutan
        self.width = tk.IntVar()
        self.width.set(DEFAULT_WIDTH)
        self.height = tk.IntVar()
        self.height.set(DEFAULT_HEIGHT)
        self.torus = tk.BooleanVar()

        self.__build_settings()
        self.__build_grid()

    def __build_settings(self):
        """En privat metod som bygger upp hela inställningsrutan"""
        self.settings_frame = tk.Frame(self.root)

        # Texter
        self.root.title("Livet hos matematiska organismer")
        self.top_label = tk.Label(self.root, text='Livet hos matematiska organismer', font=('Arial', 20, 'bold'))
        self.top_label.pack()
        self.grid_label = tk.Label(self.settings_frame, text='Skapa ett nytt grid: ', justify='left')
        self.grid_label.grid(column=0, row=1, columnspan=2)

        # Etiketter
        self.width_label = tk.Label(self.settings_frame, text='Bredd: ')
        self.height_label = tk.Label(self.settings_frame, text='Höjd: ')
        self.width_label.grid(column=0, row=2)
        self.height_label.grid(column=0, row=3)

        # Inmatning
        # https://www.pythontutorial.net/tkinter/tkinter-validation/
        self.width_entry = tk.Entry(self.settings_frame, textvariable=self.width, validate="all",
                                    validatecommand=(self.root.register(validate_num), "%P"))
        self.height_entry = tk.Entry(self.settings_frame, textvariable=self.height, validate="all",
                                     validatecommand=(self.root.register(validate_num), "%P"))
        self.torus_box = tk.Checkbutton(self.settings_frame, text='Torus', variable=self.torus)
        self.width_entry.grid(row=2, column=1)
        self.height_entry.grid(row=3, column=1)
        self.torus_box.grid(column=0, row=4)

        # Byggknapp
        self.build_button = tk.Button(self.settings_frame, text="Bygg!", command=self.__show_grid)
        self.build_button.grid(row=5, column=0, columnspan=2)

        self.settings_frame.pack()

    def __build_grid(self):
        """En privat metod som bygger upp hela spelrutan"""
        self.life_frame = tk.Frame(self.root)
        self.life_canvas = tk.Canvas(self.life_frame, bg="black", bd=0, relief="flat")

        self.slower_button = tk.Button(self.life_frame, text="<", command=self.__slower)
        self.pause_button = tk.Button(self.life_frame, text="⏵", command=self.__pause)
        self.step_button = tk.Button(self.life_frame, text="Steg", command=self.__step_press)
        self.faster_button = tk.Button(self.life_frame, text=">", command=self.__faster)
        self.speed_label = tk.Label(self.life_frame, text="0.5 gen/s")
        self.slower_button.grid(row=1, column=0)
        self.pause_button.grid(row=1, column=1)
        self.step_button.grid(row=1, column=2)
        self.faster_button.grid(row=1, column=3)
        self.speed_label.grid(row=2, column=1, columnspan=2)

    def __show_grid(self):
        """Metoden läser och validerar användarens inmatning. Om inmatningen är giltig skapas ett Grid och
        spelrutan visas."""
        # Om inmatningen är tom kastas tk.TclError
        try:
            width, height = self.width.get(), self.height.get()
        except tk.TclError:
            width, height = 0, 0

        if not (MIN_WIDTH_GUI <= width <= MAX_WIDTH_GUI and MIN_HEIGHT_GUI <= height <= MAX_HEIGHT_GUI):
            # Om inmatningen är utanför min/max berättas det för användaren
            self.grid_label.config(
                text=f"Spelbrädet måste ligga i intervallen:\nBredd: {MIN_WIDTH_GUI} -> {MAX_WIDTH_GUI}\nHöjd: {MIN_HEIGHT_GUI} -> {MAX_HEIGHT_GUI}")
            return

        self.settings_frame.destroy()

        self.update_canvas_size()  # Sätter canvasen till rätt storlek baserat på fönsterstorleken
        self.zoom_level = self.min_zoom

        # Binder event
        self.root.bind("<Configure>", self.__resize)
        self.life_canvas.bind("<MouseWheel>", self.__scroll)
        self.life_canvas.bind("<B1-Motion>", self.__mouse_move)
        self.life_canvas.bind('<ButtonPress-1>', self.__canvas_click)

        self.grid = Grid(width, height, self.torus.get())
        self.life_canvas.grid(row=0, column=0, columnspan=4)

        self.life_frame.pack()

    def __get_visible_cells_set(self):
        """En metod som kombinerar alive_set, revive_cells_queue, och kill_cells_queue för att hitta
        de celler som ska synas just nu. De returneras i en mängd med de aktuella cellerna.
        :return: De celler som ska synas nu
        :rtype: set[Cell]"""
        # revive_cells_queue och kill_cells_queue är mängder med koordinater -> konvertera till mängder med celler
        revive_cells = {self.grid.grid[x][y] for x, y in self.revive_cells_queue}
        kill_cells = {self.grid.grid[x][y] for x, y in self.kill_cells_queue}

        # Ta reda på de synliga cellerna med mängdoperationer
        return (self.grid.alive_set | revive_cells) - kill_cells

    def update_setting_buttons(self):
        """Metoden uppdaterar knapparna och texten under spelbrädet för att motsvara spelets nuvarande status"""
        steps = STEPS[self.speed]
        speed = SPEEDS[self.speed]
        frequency = steps / speed * 1000
        self.speed_label.config(text=f"{frequency} gen/s")
        self.pause_button.config(text="⏸" * self.running or "⏵")  # Går också att skriva: "⏸" if self.running else "⏵"

    def update_canvas_size(self):
        """Metoden uppdaterar canvasen för att motsvara fönstrets storlek. En ny minsta zoom räknas ut också."""
        # Ny storlek
        max_width = self.root.winfo_width() * CANVAS_SIZE
        max_height = self.root.winfo_height() * CANVAS_SIZE - LOWER_BUTTON_PX
        self.canvas_width = round(max_width) + BORDER_OFFSET_PX * 2
        self.canvas_height = round(max_height) + BORDER_OFFSET_PX * 2
        self.life_canvas.config(width=self.canvas_width, height=self.canvas_height)

        # Ny zoom
        self.min_zoom = max(min(self.canvas_width / self.width.get(), self.canvas_height / self.height.get()), MINIMAL_ZOOM)

    def __calculate_zoom(self, delta, x, y):
        """Metoden ändrar på zoom_level och räknar ut nya offset baserat på delta och punkten som ska zoomas in på.
        :param delta: Skillnad i zoomnivå
        :type delta: float
        :param x: x-koordinat till punkten som ska zoomas in på
        :type x: int
        :param y: y-koordinat till punkten som ska zoomas in på
        :type y: int"""

        # Ny zoom
        new_zoom_level = self.zoom_level + delta

        # Ny offset
        # https://stackoverflow.com/questions/38281745/calculating-view-offset-for-zooming-in-at-the-position-of-the-mouse-cursor
        x_offset = x - new_zoom_level / self.zoom_level * (x - self.grid_offset[0])  # - 0.01*event.x
        y_offset = y - new_zoom_level / self.zoom_level * (y - self.grid_offset[1])

        x_offset_min = -new_zoom_level * (self.width.get() + 1) + self.canvas_width
        y_offset_min = -new_zoom_level * (self.height.get() + 1) + self.canvas_height

        if new_zoom_level <= self.min_zoom or not RELAXED_ZOOM:
            # Om man har zoomat ut till minsta zoomnivå ska spelbrädet snäppas tillbaka till ursprungsposition
            x_offset = round(min(max(x_offset, x_offset_min), 0))
            y_offset = round(min(max(y_offset, y_offset_min), 0))

        self.grid_offset = (x_offset, y_offset)
        self.zoom_level = max(new_zoom_level, self.min_zoom)

    def __change_cell(self, cell_x, cell_y, alive=True):
        """Metoden ritar ut en cell vid cell_x, cell_y på canvasen.
        :param cell_x: x-koordinat till cellen som ska ritas ut
        :type cell_x: int
        :param cell_y: y-koordinat till cellen som ska rits ut
        :type cell_y: int
        :param alive: True om cellen ska ritas levande, False om cellen ska ritas död. (Default True)
        :type alive: bool"""
        fill_color = "white" if alive else "black"
        border_pixel = 1 if self.zoom_level >= MIN_ZOOM_FOR_CELL_BORDER else 0

        x = cell_x * self.zoom_level + BORDER_OFFSET_PX + self.grid_offset[0]
        y = cell_y * self.zoom_level + BORDER_OFFSET_PX + self.grid_offset[1]
        self.life_canvas.create_rectangle(x, y, x + self.zoom_level, y + self.zoom_level, fill=fill_color, width=border_pixel)

    def __event_coords_to_cell_coords(self, event):
        """Metoden konverterar koordinater på canvasen till koordinater i spelbrädet.
        :param event: Tkinter event
        :type event: tkinter.Event
        :return: En punkt (x, y) på spelbrädet
        :rtype: tuple[int, int]"""
        x = int((event.x - self.grid_offset[0] - BORDER_OFFSET_PX) // self.zoom_level)
        y = int((event.y - self.grid_offset[1] - BORDER_OFFSET_PX) // self.zoom_level)
        return x, y

    def __resize(self, event):
        """Eventhanterare för "Configure" hos self.root. Kollar om fönstret har bytt storlek
        och uppdaterar canvasen utifrån det.
        :param event: tkinter configure event
        :type event: tk.Event"""
        # https://stackoverflow.com/questions/61712329/tkinter-track-window-resize-specifically
        if self.root.winfo_width() != event.width or self.root.winfo_height() != event.height:
            self.update_canvas_size()  # Uppdaterar canvasstorlek
            self.zoom_level = max(self.zoom_level, self.min_zoom)  # Tvingar zoom om rutan förstoras
            self.render_frame(self.__get_visible_cells_set())  # Ritar om spelbrädet

    def __slower(self):
        """Eventhanterare för "Click" på self.slower_button. Metoden sänker hastigheten och uppdaterar texten
        som anger hastigheten i gränssnittet."""
        self.speed -= 1
        self.speed = max(self.speed, 0)  # Se till att hastigheten inte kan gå under 0
        self.update_setting_buttons()

    def __faster(self):
        """Eventhanterare för "Click" på self.faster_button. Metoden höjer hastigheten och uppdaterar texten
        som anger hastigheten i gränssnittet."""
        self.speed += 1
        self.speed = min(self.speed, len(SPEEDS) - 1)  # Se till att hastigheten inte kan gå över maximala hastigheten
        self.update_setting_buttons()

    def __step_press(self):
        """Eventhanterare för "Click" på self.step_button. Metoden pausar simulationen och stegar en generation
        framåt. Texten på pausknappen uppdateras."""
        self.running = False
        self.simulate_step()
        self.render_frame(self.grid.alive_set)
        self.update_setting_buttons()

    def __pause(self):
        """Eventhanterare för "Click" på self.pause_button. Metoden växlar mellan att pausa och köra
        simulationen och uppdaterar texten på knappen."""
        self.running = not self.running
        self.update_setting_buttons()

    def __scroll(self, event):
        """Eventhanterare för "MouseWheel" på self.life_canvas. Metoden kollar vilket håll användaren
        scrollade, räknar ut en ny zoom, och ritar om spelplanen.
        :param event: Tkinter scroll-event
        :type event: tkinter.Event"""
        sgn_delta = 0
        if event.delta > 0:
            sgn_delta = 1
        elif event.delta < 0:
            sgn_delta = -1

        self.__calculate_zoom(sgn_delta * self.zoom_level * ZOOM_FACTOR, event.x, event.y)  # Procentuell ändring i zoom
        self.render_frame(self.__get_visible_cells_set())

    def __canvas_click(self, event):
        """Eventhanterare för "Click" på self.life_canvas. Metoden växlar mellan att manuellt döda och
        återuppliva cellen som klickas på.
        :param event: Tkinter klickevent
        :type event: tkinter.Event"""

        x, y = self.__event_coords_to_cell_coords(event)
        self.last_clicked = (x, y)  # Sparar den senaste klickade cellen för att mouse_move ska fungera ordentligt
        if 0 <= x < self.width.get() and 0 <= y < self.height.get():
            if self.grid.grid[x][y] in self.__get_visible_cells_set():
                # Om cellen är lever dödas den
                self.__change_cell(x, y, False)
                self.kill_cells_queue.add((x, y))
                self.revive_cells_queue.discard((x, y))
            else:
                # Om cellen är död återupplivas den
                self.__change_cell(x, y, True)
                self.revive_cells_queue.add((x, y))
                self.kill_cells_queue.discard((x, y))

    def __mouse_move(self, event):
        """Eventhanterare för "B1-Motion" på self.life_canvas. Metoden återupplivar alla celler
        som användaren drar musen över med Mouse-B1 intryckt.
        :param event: Tkinter move-event
        :type event: tkinter.Event"""

        x, y = self.__event_coords_to_cell_coords(event)
        # Den senaste cellen användaren klickade på ignoreras, eftersom att det kan vara användaren som råkar
        # röra lite på musen efter att ha dödat en cell.
        if 0 <= x < self.width.get() and 0 <= y < self.height.get() and (x, y) != self.last_clicked:
            # Om användaren drar musen över flera celler tillåts den senast klickade cellen att ändras
            self.last_clicked = None

            # Återuppliva cellen
            self.__change_cell(x, y, True)
            self.revive_cells_queue.add((x, y))
            self.kill_cells_queue.discard((x, y))

    def render_frame(self, cells):
        """Metoden tömmer spelbrädet och ritar sedan ut alla celler i cells.
        :param cells: En mängd med alla celler som ska ritas ut
        :type cells: set[Cell]"""
        self.life_canvas.delete("all")  # Tömmer canvasen
        for cell in cells:
            self.__change_cell(cell.pos_x, cell.pos_y)

    def simulate_step(self):
        """Metoden hanterar de celler som manuellt har dödats och återupplivats, och
        simulerar sedan en generation av Game of Life"""
        # Lägg till återupplivade celler
        self.grid.add_alive_cells(self.revive_cells_queue)
        self.revive_cells_queue.clear()

        # Radera dödade celler
        self.grid.kill_cells(self.kill_cells_queue)
        self.kill_cells_queue.clear()

        # Simulera en generation
        self.grid.simulate_step(self.current_generation + 1)
        self.current_generation += 1

    def __update(self):
        """Metoden sköter simulation och utritning av spelet i en asynkront rekursiv loop. Metoden
        simulerar en generation om spelet inte är pausat, och ritar ut spelbrädet om det ska ske denna generation.
        Efter det schemalägger den sig att köra igen om en viss tid baserat på spelets inställda hastighet."""
        if self.running:
            self.simulate_step()
            # Ritar ut spelbrädet om det ska ske denna generation. Om det hoppas 2 eller fler generationer per
            # utskrift genereras varannan frame en generation senare för att motverka att tidssymmetriska
            # former ser statiska ut
            displayed_frames_modifier = self.simulation_frame_renders % 2 if STEPS[self.speed] > 1 else 0
            if self.current_generation % (STEPS[self.speed] - displayed_frames_modifier) == 0:
                self.render_frame(self.grid.alive_set)
                self.simulation_frame_renders += 1

        # Schemalägger att köra denna metod igen
        self.root.after(SPEEDS[self.speed], self.__update)

    def start_game_loop(self):
        """Metoden startar spelloopen genom att anropa self.__update() för första gången.
        Att anropa den här metoden flera gånger kan orsaka konstiga buggar."""
        self.__update()

    def start_ui(self):
        """Startar huvudloopen i tkinter och öppnad därmed programfönstret.
        Denna metod är blockerande tills programfönstret stängs av användaren."""
        self.root.mainloop()


if __name__ == "__main__":
    # Om den här filen körs som huvudfil startar programmet som vanligt. (används för debug)
    ui = UserInterface()
    ui.start_game_loop()
    ui.start_ui()
