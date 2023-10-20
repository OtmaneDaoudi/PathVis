from typing import List, Dict
from kivy.clock import Clock
from main import Cell
from Algorithms.A_star import Graph

Graph: Dict[Cell, List[Cell]]

class BFS:
    def __init__(self, graph: Graph, start_cell: Cell, end_cell: Cell):
        self.graph = graph
        self.start_cell = start_cell
        self.end_cell = end_cell

    def __resolve_path(self, visited: List[Cell]) -> List[Cell]:
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
    
    def run(self) -> None | Dict[Cell, Cell]:
        visited = {self.start_cell: None}
        bfs_queue = [self.start_cell]
        delay = 0.005
        while bfs_queue:
            # process current node
            cell = bfs_queue.pop(0)
            if cell == self.end_cell: return self.__resolve_path(visited), delay
            else:
                # mark current node on the graph as fully explored (blue)
                if cell != self.start_cell:
                    Clock.schedule_once(cell.paint_blue, delay)
                    delay += 0.001
            # enqueue child nodes
            neighbors = self.__neighbors(cell)
            for cell_ in neighbors:
                if cell_ not in visited:
                    visited[cell_] = cell
                    bfs_queue.append(cell_)
                    # mark current child as discovered (yellow)
                    if cell_ != self.start_cell and cell_ != self.end_cell:
                        Clock.schedule_once(cell_.paint_yellow, delay)
                        delay += 0.001
        return None