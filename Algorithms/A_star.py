from typing import Tuple, List, Dict
from contextlib import suppress
from main import Cell
from kivy.clock import Clock

Graph = Dict[Cell, List[Cell]]

class A_Star:
    def __init__(self, graph: Graph):
        self.graph = graph

    def __neighbors(self, cell: Cell) -> List[Cell]:
        return self.graph[cell]
    
    def childs(self, cell: Cell) -> List[Cell]:
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

    def __g(self, cell: Cell) -> float:
        """ Returns the cost of the optimal path from start to node """
        return cell.g_score
    
    def __h(self, cell: Cell) -> float:
        """ Returns the estimated cose from node to goal """
        return cell.heuristic

    def __f(self, cell: Cell) -> float:
        """ The evaluation fucntion f = g + h """
        return self.__g(cell) + self.__h(cell)

    def aStartAlgo(self, start_node: Cell, target_node: Cell) -> None | List[Cell]:
        opened = [start_node]
        cameFrom = {}
        
        start_node.g_score = 0
        
        f_score = {}
        f_score[start_node] = start_node.heuristic

        delay = 0.3

        while opened:
            current_node = opened.pop(0)
            if current_node == target_node:
                return self.__resolve_path(cameFrom, target_node), delay
                        
            for child in self.__neighbors(current_node):
                tentative_score = current_node.g_score + 1
                if tentative_score < child.g_score:
                    cameFrom[child] = current_node
                    child.g_score = tentative_score
                    f_score[child] = tentative_score + child.heuristic
                    
                    if child not in opened:
                        opened.append(child)
                        if child != start_node and child != target_node:
                            Clock.schedule_once(child.paint_yellow, delay)
                            Cell.Scheduled_paints += 1
                            delay += 0.005
                        opened.sort(key = lambda entry : f_score[entry])
        return None