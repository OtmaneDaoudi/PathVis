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
    
    def bfs(self):
        visited = {}
        bfs_queue = [(self.start_cell, None)]
        delay = 0.03
        while bfs_queue:
            # explore current node
            cell, parent = bfs_queue.pop(0)
            if cell in visited: continue
            visited[cell] = parent
            if cell == self.end_cell: return self.__resolve_path(visited), delay
            else:
                # mark current cell on the graph
                if cell != self.start_cell:
                    Clock.schedule_once(cell.paint_yellow, delay)
                    delay += 0.005
            # enqueue child cells
            neighbors = self.__neighbors(cell)
            bfs_queue.extend([(cell_, cell) for cell_ in neighbors if cell_ not in visited])