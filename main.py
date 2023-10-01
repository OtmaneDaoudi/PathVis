import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, OptionProperty, ObjectProperty
from typing import List, Set

class Cell(Widget):
    color_ = ListProperty([1, 1, 1, 1])

    def paint_green(self):
        self.color_ = 102/255, 245/255, 66/255, 1

    def paint_black(self):
        self.color_ = [0, 0, 0, 1]

    def paint_red(self):
        self.color_ = [222/255, 43/255, 11/255, 1]

    def paint_white(self):
        self.color_ = [1, 1, 1, 1]

class ControlPanel(Widget):
    grid = ObjectProperty(None)

    def mark_start(self):
        self.grid.clickType = "Start"

    def mark_wall(self):
        self.grid.clickType = "Wall"

    def mark_end(self):
        self.grid.clickType = "End"

    def run_search(self):
        # build the graph
        
        # run the algorithm on the graph (with visualizations)
        # paint resulting path
        pass

class Grid(GridLayout):
    cells: List[Cell] = ListProperty()
    clickType = OptionProperty("Start", options = ["Start", "Wall", "End"])
    
    start_cell: Cell = None
    end_cell: Cell = None
    wall: Set[Cell] = set()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(40 * 20):
            cell = Cell()
            self.cells.append(cell)
            self.add_widget(cell)

    def cell_at(self, x, y):
        for cell in self.cells:
            if cell.collide_point(x, y):
                return cell
            
    def on_touch_down(self, touch):
        print(len(self.wall))
        if touch.y >= self.y:
            target_cell = self.cell_at(*touch.pos)
            if target_cell:
                if self.clickType == "Start":
                    if self.start_cell:
                        self.start_cell.paint_white()
                    self.start_cell = target_cell
                    # remove cell from wall
                    self.wall.discard(self.start_cell)
                    target_cell.paint_green()
                elif self.clickType == "End":
                    if self.end_cell:
                        self.end_cell.paint_white()
                    self.end_cell = target_cell
                    target_cell.paint_red()
                    self.wall.discard(self.end_cell)
                
    def on_touch_move(self, touch):
        if touch.y >= self.y:
            if self.clickType == "Wall":
                target_cell = self.cell_at(*touch.pos)
                if target_cell and target_cell not in [self.start_cell, self.end_cell]:
                    self.wall.add(target_cell)
                    target_cell.paint_black()
class PathVisUi(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class PathVis(App):
    def build(self):
        return PathVisUi()

if __name__ == "__main__":
    PathVis().run()