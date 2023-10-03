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
    
    def __resolve_path(self, cameFrom: Dict[Cell, Cell | None], target_node: Cell) -> List[int]:
        """ Reconstructs resulting path """
        path = []
        curr = target_node
        while curr:
            path.append(curr)
            curr = cameFrom[curr]
        return path 

    def __g(self, cell: Cell) -> float:
        """ Returns the cost of the optimal path from start to node """
        return cell.g_score
    
    def __h(self, cell: Cell) -> float:
        """ Returns the estimated cose from node to goal """
        return cell.heuristic

    def __f(self, cell: Cell) -> float:
        """ The evaluation fucntion f = g + h """
        return self.__g(cell) + self.__h(cell)

    # def aStartAlgo(self, start_node: Cell, target_node: Cell) -> None | List[Cell]:
    #     opened, closed = [(start_node, start_node.heuristic, None)], []
    #     current_node = None
    #     start_node.g_score = 0
    #     cameFrom = {start_node: None}
    #     delay = 0.06
    #     itr = 300
    #     while itr and opened:
    #         itr -= 1
    #         if not opened:
    #             return None
    #         current_node = opened.pop(0)
    #         closed.append(current_node)
    #         if current_node[0] == target_node:
    #             return
    #             # return self.__resolve_path(cameFrom, target_node)
    #         for child in self.__neighbors(current_node[0]):
    #             if child != start_node and child != target_node:
    #                 Clock.schedule_once(child.paint_yellow, 0.2 + delay)
    #                 delay += 0.005
    #             # update child's g_score
    #             new_g_score = self.__g(current_node[0]) + self.__cost(current_node[0], child)
    #             if new_g_score < self.__g(child):
    #                 cameFrom[child] = current_node[0]
    #                 child.g_score = new_g_score
    #             child_entry = (child, self.__f(child), current_node[0])
    #             # check if the child already in opened or closed with lower evaluation
    #             temp = opened + closed
    #             filtered_temp = list(filter(
    #                 lambda entry: entry[0] == child_entry[0] and child_entry[1] <= entry[1], temp))
    #             if filtered_temp:
    #                 for node in filtered_temp:
    #                     with suppress(ValueError):
    #                         opened.remove(node)
    #                     with suppress(ValueError):
    #                         closed.remove(node)
    #             # add child entry to opened
    #             opened.append(child_entry)
            
    #         # sort opened
    #         opened.sort(key=lambda entry: entry[1])
            
    #         print(f'opnd : {len(opened)} | clsd : {len(closed)}')
    #     print("done")
    #     return None

    def aStartAlgo(self, start_node: Cell, target_node: Cell) -> None | List[Cell]:
        opened = [start_node]
        cameFrom = {}
        
        start_node.g_score = 0
        
        f_score = {}
        f_score[start_node] = start_node.heuristic

        delay = 0.06

        while opened:
            current_node = opened.pop(0)
            if current_node == target_node:
                return
                        
            for child in self.__neighbors(current_node):
                tentative_score = current_node.g_score + 1
                if tentative_score < child.g_score:
                    cameFrom[child] = current_node
                    child.g_score = tentative_score
                    f_score[child] = tentative_score + child.heuristic
                    
                    if child not in opened:
                        opened.append(child)
                        if child != start_node and child != target_node:
                            Clock.schedule_once(child.paint_yellow, 0.2 + delay)
                            delay += 0.005
                        opened.sort(key = lambda entry : f_score[entry])
        return None