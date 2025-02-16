import tkinter as tk
from math import ceil

from Grid import Grid
from main import MIN_WIDTH, MAX_WIDTH, MIN_HEIGHT, MAX_HEIGHT

# Konstanter
BORDER_OFFSET_PX = 0
LOWER_BUTTON_PX = 50
MINIMAL_ZOOM = 0.1
MIN_ZOOM_FOR_BORDER = 2
STEPS = [1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 8, 16, 50]
SPEEDS = [2000, 1000, 500, 250, 100, 50, 20, 10, 10, 10, 10, 10, 10]


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
    root : Tk Tkinters rotfönster"""

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

        self.root = tk.Tk()  # Skapar ett fönster
        self.root.geometry("400x400")

        # Variabler kopplade till inputfälten i inställningsrutan
        self.width = tk.IntVar()
        self.width.set(10)
        self.height = tk.IntVar()
        self.height.set(10)
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

        self.width_label = tk.Label(self.settings_frame, text='Bredd: ')
        self.height_label = tk.Label(self.settings_frame, text='Höjd: ')
        self.torus_box = tk.Checkbutton(self.settings_frame, text='Torus', variable=self.torus)
        self.width_label.grid(column=0, row=2)
        self.height_label.grid(column=0, row=3)
        self.torus_box.grid(column=0, row=4)

        self.width_entry = tk.Entry(self.settings_frame, textvariable=self.width, validate="all",
                                    validatecommand=(self.root.register(validate_num), "%P"))
        self.height_entry = tk.Entry(self.settings_frame, textvariable=self.height, validate="all",
                                     validatecommand=(self.root.register(validate_num), "%P"))
        self.width_entry.grid(row=2, column=1)
        self.height_entry.grid(row=3, column=1)

        self.build_button = tk.Button(self.settings_frame, text="Bygg!", command=self.__show_grid)
        self.build_button.grid(row=5, column=0, columnspan=2)

        self.settings_frame.pack()

    def __build_grid(self):
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
        width, height = self.width.get(), self.height.get()
        if not (MIN_WIDTH <= width <= MAX_WIDTH and MIN_HEIGHT <= height <= MAX_HEIGHT):
            self.grid_label.config(text=f"Spelbrädet måste ligga i intervallen:\nBredd: {MIN_WIDTH} -> {MAX_WIDTH}\nHöjd: {MIN_HEIGHT} -> {MAX_HEIGHT}")
            return

        self.settings_frame.destroy()

        self.update_canvas_size()
        self.zoom_level = self.min_zoom

        self.root.bind("<Configure>", self.__resize)
        self.life_canvas.bind("<MouseWheel>", self.__scroll)
        self.life_canvas.bind("<B1-Motion>", self.__mouse_move)
        self.life_canvas.bind('<ButtonPress-1>', self.__canvas_click)
        self.grid = Grid(width, height, self.torus.get())
        self.life_canvas.grid(row=0, column=0, columnspan=4)

        self.life_frame.pack()

    # https://stackoverflow.com/questions/61712329/tkinter-track-window-resize-specifically
    def __resize(self, event):
        if self.root.winfo_width() != event.width or self.root.winfo_height() != event.height:
            self.update_canvas_size()
            self.__calculate_zoom(0, 0, 0)

    def update_setting_buttons(self):
        steps = STEPS[self.speed]
        speed = SPEEDS[self.speed]
        frequency = steps / speed * 1000
        self.speed_label.config(text=f"{frequency} gen/s")
        self.pause_button.config(text="⏸" * self.running or "⏵")

    def __calculate_zoom(self, delta, x, y):
        # zooma fungerar
        # https://stackoverflow.com/questions/38281745/calculating-view-offset-for-zooming-in-at-the-position-of-the-mouse-cursor
        x_offset_prem = x - (self.zoom_level + delta) / self.zoom_level * (x - self.grid_offset[0])  # - 0.01*event.x
        y_offset_prem = y - (self.zoom_level + delta) / self.zoom_level * (y - self.grid_offset[1])

        x_offset = round(max(min(x_offset_prem, 0), -self.zoom_level * self.width.get() - self.canvas_width))
        y_offset = round(max(min(y_offset_prem, 0), -self.zoom_level * self.height.get() - self.canvas_height))

        self.grid_offset = (x_offset, y_offset)
        self.zoom_level = max(self.zoom_level + delta, self.min_zoom)
        self.render_frame()

        for x, y in self.revive_cells_queue:
            self.__change_cell(x, y)

    def __change_cell(self, cell_x, cell_y, alive=True):
        fill_color = "white" if alive else "black"
        x = cell_x * self.zoom_level + BORDER_OFFSET_PX + self.grid_offset[0]
        y = cell_y * self.zoom_level + BORDER_OFFSET_PX + self.grid_offset[1]
        #print(self.zoom_level)
        self.life_canvas.create_rectangle(x, y, x + self.zoom_level, y + self.zoom_level, fill=fill_color, width=1 if self.zoom_level >= MIN_ZOOM_FOR_BORDER else 0)

    def __event_coords_to_cell_coords(self, event):
        x = int((event.x - self.grid_offset[0] - BORDER_OFFSET_PX) // self.zoom_level)
        y = int((event.y - self.grid_offset[1] - BORDER_OFFSET_PX) // self.zoom_level)
        return x, y

    def __slower(self):
        self.speed -= 1
        self.speed = max(self.speed, 0)
        self.update_setting_buttons()

    def __faster(self):
        self.speed += 1
        self.speed = min(self.speed, len(SPEEDS) - 1)
        self.update_setting_buttons()

    def __step_press(self):
        self.running = False
        self.simulate_step()
        self.render_frame()
        self.update_setting_buttons()

    def __pause(self):
        self.running = not self.running
        self.update_setting_buttons()

    def __scroll(self, event):
        if event.delta > 0:
            self.__calculate_zoom(1, event.x, event.y)
        elif event.delta < 0:
            self.__calculate_zoom(-1, event.x, event.y)

    def __canvas_click(self, event):
        print(f"klick på {event.x}, {event.y}")
        x, y = self.__event_coords_to_cell_coords(event)
        self.last_clicked = (x, y)
        if 0 <= x < self.width.get() and 0 <= y < self.height.get():
            if self.grid.grid[x][y] in self.grid.alive_set and (x, y) in self.kill_cells_queue or self.grid.grid[x][
                y] not in self.grid.alive_set and (x, y) not in self.revive_cells_queue:
                self.__change_cell(x, y, True)
                self.revive_cells_queue.add((x, y))
                self.kill_cells_queue.discard((x, y))
                print(f"Add {x}, {y}")
            else:
                self.__change_cell(x, y, False)
                self.kill_cells_queue.add((x, y))
                self.revive_cells_queue.discard((x, y))
                print(f"Kill {x}, {y}")

    def __mouse_move(self, event):
        x, y = self.__event_coords_to_cell_coords(event)
        if 0 <= x < self.width.get() and 0 <= y < self.height.get() and (x, y) != self.last_clicked:
            self.last_clicked = None
            self.__change_cell(x, y, True)
            self.revive_cells_queue.add((x, y))

    def update_canvas_size(self):
        max_width = self.root.winfo_width() * 0.9
        max_height = self.root.winfo_height() * 0.9 - LOWER_BUTTON_PX

        self.canvas_width = round(max_width) + BORDER_OFFSET_PX * 2
        self.canvas_height = round(max_height) + BORDER_OFFSET_PX * 2
        self.min_zoom = max(min(self.canvas_width / self.width.get(), self.canvas_height / self.height.get()), MINIMAL_ZOOM)
        self.life_canvas.config(width=self.canvas_width, height=self.canvas_height)

    def render_frame(self):
        self.life_canvas.delete("all")
        #print("render")
        for cell in self.grid.alive_set:
            self.__change_cell(cell.pos_x, cell.pos_y)
            #print(cell.pos_x, cell.pos_y)
        # self.root.update()

    def simulate_step(self):
        #print(f"Add: {self.revive_cells_queue}")
        self.grid.add_alive_cells(self.revive_cells_queue)
        self.revive_cells_queue.clear()
        #print(f"kill: {self.kill_cells_queue}")
        self.grid.kill_cells(self.kill_cells_queue)
        self.kill_cells_queue.clear()

        self.grid.simulate_step(self.current_generation + 1)
        self.current_generation += 1

    def __update(self):
        if self.running:
            self.simulate_step()
            displayed_frames_modifier = self.current_generation % 2 if STEPS[self.speed] > 1 else 0
            if self.current_generation % (STEPS[self.speed] - displayed_frames_modifier) == 0:
                self.render_frame()

        self.root.after(SPEEDS[self.speed], self.__update)

    def start_game_loop(self):
        self.__update()

    def start_ui(self):
        self.root.mainloop()


if __name__ == "__main__":
    import main_GUI
