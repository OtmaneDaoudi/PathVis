from typing import Tuple, List, Dict
from contextlib import suppress
from main import Cell

Graph = Dict[Cell, List[Cell]]

class A_Star:
    def __init__(self, graph: Graph):
        self.graph = graph

    def __neighbors(self, cell: Cell) -> List[Cell]:
        return self.graph[cell]
    
    def __cost(self, cell1: Cell, cell2: Cell) -> int:
        # we use uniform costs, may be suceptible to future change
        return 1
    
    def __resolve_path(self, cameFrom: Dict[Cell, Cell | None], target_node: Cell) -> List[int]:
        """ Reconstructs resulting path """
        path = []
        curr = target_node
        while curr:
            path.append(curr)
            curr = cameFrom[curr]
        print(len(path))
        return path 

    def __g(self, cell: Cell) -> int:
        """ Returns the cost of the optimal path from start to node """
        return cell.g_score
    
    def __h(self, cell: Cell) -> int:
        """ Returns the estimated cose from node to goal """
        return cell.heuristic

    def __f(self, cell: Cell) -> int:
        """ The evaluation fucntion f = g + h """
        return self.__g(cell) + self.__h(cell)

    def aStartAlgo(self, start_node: Cell, target_node: Cell) -> None | List[Cell]:
        opened, closed = [(start_node, start_node.heuristic, None)], []
        current_node = None
        start_node.g_score = 0
        cameFrom = {start_node: None}

        while 1:
            if not opened:
                return None
            current_node = opened.pop(0)
            closed.append(current_node)
            if current_node[0] == target_node:
                return self.__resolve_path(cameFrom, target_node)
            for child in self.__neighbors(current_node[0]):
                # update child's g_score
                new_g_score = self.__g(current_node[0]) + self.__cost(current_node[0], child)
                if new_g_score < self.__g(child):
                    child.g_score = new_g_score
                    cameFrom[child] = current_node[0]
                child_entry = (child, self.__f(child), current_node[0])
                # check if the child already in opened or closed with lower evaluation
                temp = opened + closed
                filtered_temp = list(filter(
                    lambda entry: entry[0] == child_entry[0] and child_entry[1] <= entry[1], temp))
                if filtered_temp:
                    with suppress(ValueError):
                        opened.remove(filtered_temp[0])
                    with suppress(ValueError):
                        closed.remove(filtered_temp[0])
                # add child entry to opened
                opened.append(child_entry)
                child.paint_yellow()
                # sort opened
                opened.sort(key=lambda entry: entry[1])