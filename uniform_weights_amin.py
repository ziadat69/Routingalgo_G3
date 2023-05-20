import time
from algorithm.generic_sr import GenericSR
from algorithm.segment_routing.equal_split_shortest_path import EqualSplitShortestPath

class UniformWeights(GenericSR):
    def __init__(self, nodes: list, links: list, demands: list, weights: dict = None, waypoints: dict = None, **kwargs):
        super().__init__(nodes, links, demands, weights, waypoints)

        self.__nodes = nodes  # [i, ...]
        self.__links = links  # [(i,j,c), ...]
        self.__demands = demands  # {idx: (s,t,d), ...}
        self.__waypoints = waypoints

    def compute_link_utilization(self, weights):
        """Compute link utilization based on the capacity-aware weights"""
        link_utilization = {}
        for link, weight in weights.items():
            capacity = self.__get_link_capacity(link)
            utilization = weight / capacity
            link_utilization[link] = utilization
        return link_utilization

    def __get_link_capacity(self, link):
        """Get the capacity of a link"""
        for i, j, c in self.__links:
            if (i, j) == link:
                return c
        return 0

    def compute_capacity_aware_weights(self, link_utilization):
        """Compute capacity-aware weights based on link utilization"""
        demand_weights = {}
        for link, utilization in link_utilization.items():
            demand_weights[link] = 1 / (1 - utilization)
        return demand_weights

    def solve(self) -> dict:
        """Set capacity-aware weights and use shortest path algorithm"""

        # add random waypoint for each demand
        t = time.process_time()
        pt_start = time.process_time()  # count process time (e.g. sleep excluded)

        # Compute link utilization based on the capacity-aware weights
        link_utilization = self.compute_link_utilization(self.__weights)

        # Compute capacity-aware weights based on link utilization
        demand_weights = self.compute_capacity_aware_weights(link_utilization)

        # Solve the routing problem with capacity-aware weights
        post_processing = EqualSplitShortestPath(nodes=self.__nodes, links=self.__links, demands=self.__demands,
                                                 split=True, weights=demand_weights, waypoints=self.__waypoints)
        solution = post_processing.solve()

        pt_duration = time.process_time() - pt_start
        exe_time = time.process_time() - t

        # Update execution time
        solution["execution_time"] = exe_time
        solution["process_time"] = pt_duration

        return solution

    def get_name(self):
        """Returns name of algorithm"""
        return "uniform_weights"

