import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class PathVisInterface(GridLayout):
    def __init__(self, dimension: int, **kwargs):
        super().__init__(**kwargs)
        self.cols = self.rows = dimension
        self.add_widget(Label(text = "hello"))

class PathVis(App):
    def build(self):
        return PathVisInterface(4)

if __name__ == "__main__":
    PathVis().run()