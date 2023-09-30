from typing import Tuple, List, Dict
from contextlib import suppress


class Graph:
    # An edge is a tuple containg a target node and a cost
    Edge = Tuple[int, int]

    def __init__(self, adj_list: List[List[Edge]], heuristics: List[int]):
        self.graph: Dict[int, List[Graph.Edge]] = {
            index: successors for index, successors in enumerate(adj_list)
        }
        self.heuristics = heuristics
        self.g_scores = [float("inf") for _ in range(len(adj_list))]

    def neighbors(self, node: int) -> List[int]:
        return [edge[0] for edge in self.graph[node]]

    def heuristic(self):
        return self.heuristics

    def aStartAlgo(self, start_node: int, target_node: int) -> None | List[int]:
        # helper functions for the algorithm
        def __cost(node1: int, node2: int) -> int:
            cost = [edge[1] for edge in self.graph[node1] if edge[0] == node2]
            return cost[0]

        def __g(node: int) -> int:
            """ Returns the cost of the optimal path from start to node """
            return self.g_scores[node]

        def __h(node: int) -> int:
            """ Returns the estimated cose from node to goal """
            return self.heuristic()[node]

        def __f(node: int) -> int:
            """ The evaluation fucntion f = g + h """
            return __g(node) + __h(node)

        def __resolve_path(closed: List[int]) -> List[int]:
            curr = target_node
            res = []
            while 1:
                for entry in closed:
                    if entry[0] == curr:
                        res.insert(0, entry[0])
                        closed.remove(entry)
                        curr = entry[2]
                        break
                if curr == None:
                    return res

        opened, closed = [(start_node, __h(start_node), None)], []
        current_node = None
        self.g_scores[start_node] = 0
        # i = 2
        while 1:
            if not opened:
                return None
            current_node = opened.pop(0)
            closed.append(current_node)
            if current_node[0] == target_node:
                return __resolve_path(closed)
            for child in self.neighbors(current_node[0]):
                # update child's g_score
                new_g_score = __g(
                    current_node[0]) + __cost(current_node[0], child)
                if new_g_score < __g(child):
                    self.g_scores[child] = new_g_score
                child_entry = (child, __f(child), current_node[0])
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
                # sort opened
                opened.sort(key=lambda entry: entry[1])
            # debugging output to show the evolution of opened and closed alog the iterations
            # op = f'{opened}'
            # cl = f'{closed}'
            # print(f'{i:>2} : {op.ljust(40)} | {cl.ljust(40)}')
            # i += 1


if __name__ == '__main__':
    adj_list = [
        [(1, 3), (2, 4), (3, 2)],
        [(5, 7)],
        [(4, 2)],
        [(2, 1), (4, 1)],
        [(6, 4)],
        [(6, 4)],
        []
    ]

    heuristics = [9, 2, 2, 5, 3, 2, 0]
    graph = Graph(adj_list, heuristics)
    print(graph.aStartAlgo(0, 6))
