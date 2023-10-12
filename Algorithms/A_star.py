from typing import List, Dict
from main import Cell
from kivy.clock import Clock
from kivy.vector import Vector

Graph = Dict[Cell, List[Cell]]

class A_Star:
    def __init__(self, graph: Graph, start_cell: Cell, end_cell: Cell):
        self.graph = graph
        self.start_cell = start_cell
        self.end_cell = end_cell
        # calculate heuristics
        self.heuristics = {cell : Vector(cell.center).distance(self.end_cell.center) for cell in self.graph.keys()}
        self.g_scores = {cell: float("inf") for cell in self.graph.keys()}

    def __neighbors(self, cell: Cell) -> List[Cell]:
        return self.graph[cell]
    
    def __cost(self, cell1: Cell, cell2: Cell) -> int:
        # we use uniform costs, may be suceptible to future change
        return 1
    
    def __resolve_path(self, cameFrom: Dict[Cell, Cell | None], current: Cell) -> List[int]:
        """ Reconstructs resulting path """
        total_path = [current]
        while current in cameFrom.keys():
            current = cameFrom[current]
            total_path.append(current)
        return total_path

    def run(self) -> None | List[Cell]:
        opened = [self.start_cell]
        cameFrom = {}
        
        self.g_scores[self.start_cell] = 0
        
        f_score = {}
        f_score[self.start_cell] = self.heuristics[self.start_cell]

        delay = 0.3

        while opened:
            current_node = opened.pop(0)
            if current_node == self.end_cell:
                return self.__resolve_path(cameFrom, self.end_cell), delay
                        
            for child in self.__neighbors(current_node):
                tentative_score = self.g_scores[current_node] + 1
                if tentative_score < self.g_scores[child]:
                    cameFrom[child] = current_node
                    self.g_scores[child] = tentative_score
                    f_score[child] = tentative_score + self.heuristics[child]
                    
                    if child not in opened:
                        opened.append(child)
                        if child != self.start_cell and child != self.end_cell:
                            Clock.schedule_once(child.paint_yellow, delay)
                            delay += 0.005
                        opened.sort(key = lambda entry : f_score[entry])
        return None