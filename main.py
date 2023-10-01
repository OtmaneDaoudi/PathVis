import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, OptionProperty, ObjectProperty
from typing import List, Set,Dict
from kivy.vector import Vector
from itertools import chain
from kivy.clock import Clock

import Algorithms.A_star

class Cell(Widget):
    color_ = ListProperty([1, 1, 1, 1])

    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.y = y
        self.g_score = float("inf")
        self.heuristic = None # evaluated when visualization is invoked

    def paint_green(self):
        self.color_ = 102/255, 245/255, 66/255, 1

    def paint_black(self):
        self.color_ = [0, 0, 0, 1]

    def paint_red(self):
        self.color_ = [222/255, 43/255, 11/255, 1]

    def paint_white(self):
        self.color_ = [1, 1, 1, 1]

    def paint_yellow(self):
        self.color_ = [1, 1, 0, 1]

class ControlPanel(Widget):
    grid = ObjectProperty(None)

    def mark_start(self):
        self.grid.clickType = "Start"

    def mark_wall(self):
        self.grid.clickType = "Wall"

    def mark_end(self):
        self.grid.clickType = "End"

    def run_search(self):
        if not self.grid.start_cell or not self.grid.end_cell: return None
        target_node = (self.grid.end_cell.x, self.grid.end_cell.y) 
        # remove wall nodes
        for wall_node in self.grid.wall:
            self.grid.graph.pop(wall_node, None)
        
        for k, v in self.grid.graph.items():
            # remove edges tqrgeting wall nodes
            for wall_node in self.grid.wall:
                if wall_node in v:
                    v.remove(wall_node)
            
            # calculate node heuristic
            k.heuristic = Vector(k.x, k.y).distance(target_node)

        # run search
        algorithm = Algorithms.A_star.A_Star(self.grid.graph)
        algorithm.aStartAlgo(self.grid.start_cell, self.grid.end_cell)
class Grid(GridLayout):
    cells: List[List[Cell]] = ListProperty()
    clickType = OptionProperty("Start", options = ["Start", "Wall", "End"])
    
    ROWS = 20
    COLS = 40

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = Grid.ROWS
        self.cols = Grid.COLS

        self.start_cell: Cell = None
        self.end_cell: Cell = None
        self.wall: Set[Cell] = set()
        # graph representation for the grid
        self.graph: Dict[Cell, List[Cell]] = dict() 

        for row_ in reversed(range(self.rows)):
            row_items = []
            for col_ in range(self.cols):
                cell = Cell(col_, row_)
                row_items.append(cell)
                self.add_widget(cell)
            self.cells.append(row_items)
            
        # populate graph
        for row in range(Grid.ROWS):
            for col in range(Grid.COLS):
                neighbors = []
                # up
                if row > 0:
                    neighbors.append(self.cells[row - 1][col])
                # down
                if row < Grid.ROWS - 1:
                    neighbors.append(self.cells[row + 1][col])
                # left
                if col > 0:
                    neighbors.append(self.cells[row][col - 1])
                # right
                if col < Grid.COLS - 1:
                    neighbors.append(self.cells[row][col + 1])
                self.graph[self.cells[row][col]] = neighbors  

    def cell_at(self, x, y):
        for cell in chain.from_iterable(self.cells):
            if cell.collide_point(x, y):
                return cell
            
    def on_touch_down(self, touch):
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