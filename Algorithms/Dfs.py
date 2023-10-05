from typing import List, Dict
from main import Cell
from kivy.clock import Clock

Graph: Dict[Cell, List[Cell]]

class Dfs:
    def __init__(self, graph: Graph, start_cell: Cell, end_cell: Cell):
        self.graph = graph
        self.start_cell = start_cell
        self.end_cell = end_cell

    def __resolve_path(self, visited: List[Cell]):
        """ reconstructed the resulting path from the visited list """
        # path = []
        # current = visited.pop()
        # while:
        #     if current[0] == self.end_cell:

        # return path
        return None

    def __neighbors(self, cell: Cell) -> List[Cell]:
        return self.graph[cell]
    
    def dfs(self):
        visited = []
        dfs_stack = [(self.start_cell, None)]
        delay = 0.03
        while dfs_stack:
            # explore current node
            current_cell = dfs_stack.pop()
            visited.append(current_cell)

            if current_cell[0] == self.end_cell:
                return self.__resolve_path(visited), delay
            else:
                # mark current cell on the graph
                if current_cell[0] != self.start_cell:
                    Clock.schedule_once(current_cell[0].paint_yellow, delay)
                    delay += 0.005

            # push child cells
            dfs_stack.extend(self.__neighbors(current_cell))
                




        
        