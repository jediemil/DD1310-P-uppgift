import tkinter as tk

def validate_num(new_val):
    return new_val.isnumeric()

class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Livet hos matematiska organismer")
        self.top_label = tk.Label(self.root, text='Livet hos matematiska organismer', font=('Arial', 20, 'bold'))
        self.top_label.grid(row=0, column=0, columnspan=2)
        self.grid_label = tk.Label(self.root, text='Skapa ett nytt grid: ', justify='left')
        self.grid_label.grid(column=0, row=1, columnspan=2)

        self.width_label = tk.Label(self.root, text='Bredd: ')
        self.height_label = tk.Label(self.root, text='Höjd: ')
        self.width_label.grid(column=0, row=2)
        self.height_label.grid(column=0, row=3)

        self.width = tk.IntVar()
        self.width.set(10)
        self.height = tk.IntVar()
        self.height.set(10)
        self.width_entry = tk.Entry(self.root, textvariable=self.width, validate="all",
                                    validatecommand=(self.root.register(validate_num), "%P"))
        self.height_entry = tk.Entry(self.root, textvariable=self.height, validate="all",
                                    validatecommand=(self.root.register(validate_num), "%P"))
        self.width_entry.grid(row=2, column=1)
        self.height_entry.grid(row=3, column=1)

        self.build_button = tk.Button(self.root, text="Bygg!", command=self.build_grid)
        self.build_button.grid(row=4, column=0, columnspan=2)

    def build_grid(self):
        print("Bygg grid")

    def start(self):
        self.root.mainloop()