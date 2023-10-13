from typing import List, Dict
from kivy.clock import Clock
from main import Cell
from Algorithms.A_star import Graph
from kivy.vector import Vector

Graph: Dict[Cell, List[Cell]]

class GBFS:
    def __init__(self, graph: Graph, start_cell: Cell, end_cell: Cell):
        self.graph = graph
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.heuristics = {cell : Vector(cell.center).distance(self.end_cell.center) for cell in self.graph.keys()}

    def __resolve_path(self, visited: List[Cell]):
        """ reconstructed the resulting path from the visited list """
        path = []
        curr = self.end_cell
        while curr:
            parent = visited[curr]
            path.append(curr)
            if parent:
                path.append(parent)
            curr = visited[curr]
        return path

    def __neighbors(self, cell: Cell) -> List[Cell]:
        return self.graph[cell]
    
    def run(self):
        gbfs_queue = [self.start_cell]
        visited = {self.start_cell: None}
        delay = 0.3
        while gbfs_queue:
            # explore current node
            current = gbfs_queue.pop(0)
            if current != self.start_cell:
                Clock.schedule_once(current.paint_blue, delay)
                delay += 0.001
            for child in self.__neighbors(current):
                if child not in visited:
                    visited[child] = current
                    if child == self.end_cell:
                        return self.__resolve_path(visited), delay
                    else:
                        gbfs_queue.append(child)
                        gbfs_queue.sort(key = lambda entry: self.heuristics[entry])

                        # mark child on the grid
                        Clock.schedule_once(child.paint_yellow, delay)
                        delay += 0.004
        return None

            