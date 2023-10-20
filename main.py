import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, OptionProperty, ObjectProperty
from typing import List, Set,Dict
from itertools import chain
from kivy.clock import Clock

class Cell(Widget):
    color_ = ListProperty([1, 1, 1, 1])

    def paint_green(self):
        self.color_ = [102/255, 245/255, 66/255, 1]

    def paint_black(self):
        self.color_ = [0, 0, 0, 1]

    def paint_red(self):
        self.color_ = [222/255, 43/255, 11/255, 1]

    def paint_white(self):
        self.color_ = [1, 1, 1, 1]

    def paint_yellow(self, _ = None):
        self.color_ = [1, 1, 0, 1]

    def paint_blue(self, _ = None):
        self.color_ = [138/255, 43/255, 226/255, 1]

    def paint_pink(self, _ = None):
        self.color_ = [1, 0, 243/255, 1]

class ControlPanel(BoxLayout):
    grid = ObjectProperty(None)
    algorithm = OptionProperty("A*", options = ["A*", "Breadth-first", "Depth-first", "Greedy best-first"])  

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mark_start(self):
        self.grid.clickType = "Start"
        
    def mark_wall(self):
        self.grid.clickType = "Wall"

    def mark_end(self):
        self.grid.clickType = "End"

    def run_search(self):
        if not self.grid.start_cell or not self.grid.end_cell: return None

        # construct the graph based on the current grid's state
        graph = {cell: [child for child in self.grid.graph[cell] if child not in self.grid.wall] for cell in self.grid.graph.keys() if cell not in self.grid.wall}

        # run search
        search = None
        if self.algorithm == "A*":
            from Algorithms.A_star import A_Star
            search = A_Star(graph, self.grid.start_cell, self.grid.end_cell)
        elif self.algorithm == "Depth-first":
            from Algorithms.DFS import DFS
            search = DFS(graph, self.grid.start_cell, self.grid.end_cell)
        elif self.algorithm == "Breadth-first":
            from Algorithms.BFS import BFS
            search = BFS(graph, self.grid.start_cell, self.grid.end_cell)
        elif self.algorithm == "Greedy best-first":
            from Algorithms.GBFS import GBFS
            search = GBFS(graph, self.grid.start_cell, self.grid.end_cell)
        path, delay = search.run()
        
        # trace resulting path
        delay += 0.1
        for cell in path:
            if cell != self.grid.start_cell and cell != self.grid.end_cell:
                Clock.schedule_once(cell.paint_pink, delay)
                delay += 0.008

    def clear_grid(self):
        for row in range(self.grid.ROWS):
            for col in range(self.grid.COLS):
                self.grid.cells[row][col].paint_white()

        # remove wall cells
        self.grid.wall.clear()

        # remove start cell
        if self.grid.start_cell: 
            self.grid.start_cell = None

        # remove end cell
        if self.grid.end_cell:
            self.grid.end_cell = None

class Grid(GridLayout):
    cells: List[List[Cell]] = ListProperty()
    clickType = OptionProperty("Start", options = ["Start", "Wall", "End"])    

    ROWS = 30
    COLS = 50

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = Grid.ROWS
        self.cols = Grid.COLS

        self.start_cell: Cell = None
        self.end_cell: Cell = None
        self.wall: Set[Cell] = set()
        # static representation of the grid, mapping each node to it's neighbors (not considering start, end or wall nodes)
        self.graph: Dict[Cell, List[Cell]] = dict() 

        for _ in reversed(range(Grid.ROWS)):
            row_items = []
            for _ in range(Grid.COLS):
                cell = Cell()
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