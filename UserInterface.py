import tkinter as tk

def validate_num(new_val):
    return new_val.isnumeric()

class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.settings_frame = tk.Frame(self.root)
        self.life_frame = tk.Frame(self.root)
        self.life_canvas = tk.Canvas(self.life_frame, bg="black", bd=0, relief="flat")
        self.life_canvas.bind('<Button>', self.__canvas_click)
        self.zoom_level = 10

        self.root.title("Livet hos matematiska organismer")
        self.top_label = tk.Label(self.root, text='Livet hos matematiska organismer', font=('Arial', 20, 'bold'))
        self.top_label.pack()
        self.grid_label = tk.Label(self.settings_frame, text='Skapa ett nytt grid: ', justify='left')
        self.grid_label.grid(column=0, row=1, columnspan=2)

        self.width_label = tk.Label(self.settings_frame, text='Bredd: ')
        self.height_label = tk.Label(self.settings_frame, text='Höjd: ')
        self.width_label.grid(column=0, row=2)
        self.height_label.grid(column=0, row=3)

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
        self.build_button.grid(row=4, column=0, columnspan=2)

        self.settings_frame.pack()

    def build_grid(self):
        print("Bygg grid")
        self.settings_frame.destroy()
        self.life_canvas.config(width=self.width.get()*self.zoom_level, height=self.height.get()*self.zoom_level)
        self.life_canvas.pack()
        self.life_frame.pack()

    def render_frame(self, alive_set):
        self.life_canvas.config(bg="black")
        for cell in alive_set:
            self.__add_cell(cell.pos_x, cell.pos_y)
            print(cell.pos_x, cell.pos_y)

        self.root.update()

    def __add_cell(self, x, y):
        self.life_canvas.create_rectangle(x*self.zoom_level, y*self.zoom_level, (x+1)*self.zoom_level-1, (y+1)*self.zoom_level-1, fill='white')

    def __canvas_click(self, event):
        print(f"klick på {event.x}, {event.y}")

    def start(self):
        self.root.mainloop()
        #self.root.update()

if __name__ == "__main__":
    import main_GUI