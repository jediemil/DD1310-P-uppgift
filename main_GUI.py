from Cell import Cell
from UserInterface import UserInterface
from util import Settings

ui = UserInterface()
#ui.build()
Cell.grid_width = 10
Cell.grid_height = 10
ui.render_frame({Cell(2, 0),Cell(1, 1)})

ui.start()