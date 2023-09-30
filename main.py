import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

class PathVisUi(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
class PathVis(App):
    def build(self):
        return PathVisUi()

if __name__ == "__main__":
    PathVis().run()