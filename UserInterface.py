import time
import tkinter as tk
from threading import Thread
from Grid import Grid

BORDER_OFFSET_PX = 5
STEPS =  [1,    1,    1,   1,   1,   1,  1,  1,  2,  4,  8,  16, 50]
SPEEDS = [2000, 1000, 500, 250, 100, 50, 20, 10, 10, 10, 10, 10, 10]


def validate_num(new_val):
    return new_val.isnumeric()

class UserInterface:
    def __init__(self):
        self.canvas_width = 0
        self.canvas_height = 0
        self.grid = None
        self.kill_cells_queue = set()
        self.revive_cells_queue = set()
        self.zoom_level = 10
        self.border_pixels = 1
        self.current_generation = 0
        self.cell_width = self.zoom_level + self.border_pixels
        self.running = False
        self.speed = 0
        self.displayed_frames = 0
        self.grid_offset = (0, 0)

        self.__build_ui()

    def __build_ui(self):
        self.root = tk.Tk()
        self.settings_frame = tk.Frame(self.root)
        self.life_frame = tk.Frame(self.root)
        self.life_canvas = tk.Canvas(self.life_frame, bg="black", bd=0, relief="flat")
        self.life_canvas.bind('<Button>', self.__canvas_click)

        self.root.title("Livet hos matematiska organismer")
        self.top_label = tk.Label(self.root, text='Livet hos matematiska organismer', font=('Arial', 20, 'bold'))
        self.top_label.pack()
        self.grid_label = tk.Label(self.settings_frame, text='Skapa ett nytt grid: ', justify='left')
        self.grid_label.grid(column=0, row=1, columnspan=2)

        self.width_label = tk.Label(self.settings_frame, text='Bredd: ')
        self.height_label = tk.Label(self.settings_frame, text='Höjd: ')
        self.torus = tk.BooleanVar()
        self.torus_box = tk.Checkbutton(self.settings_frame, text='Torus', variable=self.torus)
        self.width_label.grid(column=0, row=2)
        self.height_label.grid(column=0, row=3)
        self.torus_box.grid(column=0, row=4)

        self.width = tk.IntVar()
        self.width.set(10)
        self.height = tk.IntVar()
        self.height.set(10)
        self.width_entry = tk.Entry(self.settings_frame, textvariable=self.width, validate="all",
                                    validatecommand=(self.root.register(validate_num), "%P"))
        self.height_entry = tk.Entry(self.settings_frame, textvariable=self.height, validate="all",
                                     validatecommand=(self.root.register(validate_num), "%P"))
        self.width_entry.grid(row=2, column=1)
        self.height_entry.grid(row=3, column=1)

        self.build_button = tk.Button(self.settings_frame, text="Bygg!", command=self.build_grid)
        self.build_button.grid(row=5, column=0, columnspan=2)

        self.slower_button = tk.Button(self.life_frame, text="<", command=self.__slower)
        self.pause_button = tk.Button(self.life_frame, text="paus", command=self.__pause)
        self.step_button = tk.Button(self.life_frame, text="Steg", command=self.__step_press)
        self.faster_button = tk.Button(self.life_frame, text=">", command=self.__faster)
        self.slower_button.grid(row=1, column=0)
        self.pause_button.grid(row=1, column=1)
        self.step_button.grid(row=1, column=2)
        self.faster_button.grid(row=1, column=3)

        self.settings_frame.pack()

    def start_ui(self):
        self.root.mainloop()

    def __slower(self):
        self.speed -= 1
        self.speed = max(self.speed, 1)

    def __faster(self):
        self.running = True
        self.speed += 1
        self.speed = min(self.speed, len(SPEEDS) - 1)

    def __step_press(self):
        self.running = False
        self.simulate_step()
        self.render_frame()

    def __pause(self):
        self.running = not self.running

    def __scroll(self, event):
        new_zoom = 0
        if self.zoom_level <= 50 and event.delta > 0:  # TODO: BYT UT 50 MOT EN BRA STORLEK BASERAT PÅ SKÄRMSTORLEK
            new_zoom = 1
        elif self.zoom_level > 1 and event.delta < 0:  # TODO: BYT UT 1 MOT EN BRA STORLEK BASERAT PÅ SKÄRMSTORLEK
            new_zoom = -1

        x_offset = -(event.x - new_zoom*self.grid_offset[0]*self.zoom_level)/self.zoom_level
        y_offset = -(event.y - new_zoom*self.grid_offset[1]*self.zoom_level)/self.zoom_level
        self.grid_offset = (x_offset, y_offset)
        self.zoom_level += new_zoom
        self.cell_width = self.zoom_level + self.border_pixels
        self.render_frame()
        for x, y in self.revive_cells_queue:
            self.__change_cell(x, y)

    def build_grid(self):
        print("Bygg grid")
        self.settings_frame.destroy()
        self.canvas_width = self.width.get()*self.cell_width + BORDER_OFFSET_PX*2
        self.canvas_height = self.height.get()*self.cell_width + BORDER_OFFSET_PX*2
        self.life_canvas.config(width=self.canvas_width, height=self.canvas_height)
        self.life_canvas.bind_all("<MouseWheel>", self.__scroll)
        self.life_canvas.bind_all("<Motion>", self.__mouse_move)
        self.grid = Grid(self.width.get(), self.height.get(), self.torus.get())
        self.life_canvas.grid(row=0, column=0, columnspan=4)
        self.life_frame.pack()
        #self.running = True

    def render_frame(self):
        self.life_canvas.delete("all")
        for cell in self.grid.alive_set:
            self.__change_cell(cell.pos_x, cell.pos_y)
            print(cell.pos_x, cell.pos_y)

        self.displayed_frames += 1
        #self.root.update()

    def __change_cell(self, cell_x, cell_y, alive=True):
        fill_color = "white" if alive else "black"
        x = cell_x * self.cell_width + BORDER_OFFSET_PX + self.grid_offset[0]
        y = cell_y * self.cell_width + BORDER_OFFSET_PX + self.grid_offset[1]
        #if 0 <= x <= self.canvas_width and 0 <= y <= self.canvas_height:
        self.life_canvas.create_rectangle(x, y, x + self.zoom_level, y + self.zoom_level, fill=fill_color)

    def __canvas_click(self, event):
        print(f"klick på {event.x}, {event.y}")
        x = (event.x - BORDER_OFFSET_PX) // self.cell_width
        y = (event.y - BORDER_OFFSET_PX) // self.cell_width
        if 0 <= x < self.width.get() and 0 <= y < self.height.get():
            if self.grid.grid[x][y] in self.grid.alive_set and (x, y) in self.kill_cells_queue or self.grid.grid[x][y] not in self.grid.alive_set and (x, y) not in self.revive_cells_queue:
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
        x = (event.x - BORDER_OFFSET_PX) // self.cell_width
        y = (event.y - BORDER_OFFSET_PX) // self.cell_width
        self.__change_cell(x, y, True)
        self.revive_cells_queue.add((x, y))

    def simulate_step(self):
        print(f"Add: {self.revive_cells_queue}")
        self.grid.add_alive_cells(self.revive_cells_queue)
        self.revive_cells_queue.clear()
        print(f"kill: {self.kill_cells_queue}")
        self.grid.kill_cells(self.kill_cells_queue)
        self.kill_cells_queue.clear()

        self.grid.simulate_step(self.current_generation + 1)
        self.current_generation += 1


    def __update(self):
        if self.running:
            self.simulate_step()
            displayed_frames_modifier = self.displayed_frames % 2 if STEPS[self.speed] > 1 else 0
            if self.current_generation % (STEPS[self.speed] - displayed_frames_modifier) == 0:
                self.render_frame()

        self.root.after(SPEEDS[self.speed], self.__update)

    def start(self):
        self.__update()



if __name__ == "__main__":
    import main_GUI