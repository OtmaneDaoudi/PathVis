import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.graphics import Canvas, Rectangle, Color
from kivy.uix.label import Label
from kivy.properties import ListProperty, OptionProperty, ObjectProperty
from typing import List
from kivy.vector import Vector

class Cell(Widget):
    color_ = ListProperty([1, 1, 1, 1])
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_start(self):
        self.color_ = [0, .5, 0, 1]

    def set_wall(self):
        self.color_ = [0, 0, 0, 1]

    def set_end(self):
        self.color_ = [222/255, 43/255, 11/255, 1]

class ControlPanel(Widget):
    grid = ObjectProperty(None)

    def mark_start(self):
        self.grid.clickType = "Start"

    def mark_wall(self):
        self.grid.clickType = "Wall"

    def mark_end(self):
        self.grid.clickType = "End"

class Grid(GridLayout):
    cells: List[Cell] = ListProperty()
    clickType = OptionProperty("Start", options = ["Start", "Wall", "End"])
    
    start_cell, end_cell = None, None
    wall = []

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
        if touch.y >= self.y:
            target_cell = self.cell_at(*touch.pos)
            if target_cell:
                if self.clickType == "Start":
                    target_cell.set_start()
                elif self.clickType == "End":
                    target_cell.set_end()
                
    def on_touch_move(self, touch):
        if touch.y >= self.y:
            if self.clickType == "Wall":
                target_cell = self.cell_at(*touch.pos)
                if target_cell:
                    target_cell.set_wall()
class PathVisUi(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class PathVis(App):
    def build(self):
        return PathVisUi()

if __name__ == "__main__":
    PathVis().run()