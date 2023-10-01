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
from kivy.properties import ListProperty

class Cell(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ControlPanel(Widget):
    pass

class Grid(GridLayout):
    cells = ListProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(40 * 20):
            cell = Cell()
            self.cells.append(cell)
            self.add_widget(cell)

class PathVisUi(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class PathVis(App):
    def build(self):
        return PathVisUi()

if __name__ == "__main__":
    PathVis().run()