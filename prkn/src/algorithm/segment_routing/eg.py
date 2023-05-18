import time
import networkx as nx

from algorithm.generic_sr import GenericSR
from algorithm.segment_routing.equal_split_shortest_path import EqualSplitShortestPath


class InverseCapacity(GenericSR):
    def __init__(self, nodes: list, links: list, demands: list, weights: dict = None, waypoints: dict = None, **kwargs):
        super().__init__(nodes, links, demands, weights, waypoints)

        self.nodes = nodes  # [i, ...]
        self.links = links  # [(i,j,c), ...]
        self.demands = demands  # {idx: (s,t,d), ...}
        self.weights = None
        self.waypoints = waypoints
        self.threshold = kwargs.get("threshold", 2.0)  # Maximale Link-Auslastungsschwelle

    def solve(self) -> dict:
        """Setzt Gewichte auf die inverse Kapazität und verwendet den kürzesten Pfad-Algorithmus"""

        # Füge für jede Anfrage einen zufälligen Wegpunkt hinzu
        t = time.process_time()
        pt_start = time.process_time()  # Prozesszeit zählen (z. B. Sleep ausgeschlossen)

        # Setze Link-Gewichte auf die inverse Kapazität, skaliert durch die maximale Kapazität
        max_c = max([c for _, _, c in self.links])
        self.weights = {(i, j): max_c / c for i, j, c in self.links}

        # Überprüfe die maximale Link-Auslastungsschwelle
        max_utilization = max([self.get_link_utilization(link) for link in self.links])
        print (max_utilization)
        if max_utilization > self.threshold:
            print(f"WARNING: Maximale Link-Auslastungsschwelle ({self.threshold * 100}%) überschritten!")
            # Berechne alternative Routen oder implementiere Notfallmaßnahmen
                 
            # Berechne alternative Routen
            alternative_routes = self.compute_alternative_routes()

            # Löse mit alternativen Routen
            solution = self.solve_with_alternative_routes(alternative_routes)
            
            # Füge Informationen über alternative Routen zur Lösung hinzu
            solution["alternative_routes"] = alternative_routes
            solution["max_normalized_link_utilization"] = max_utilization / (max_c / self.threshold)
        else:
            # Keine Notwendigkeit für alternative Routen, löse mit dem ursprünglichen Ansatz
            post_processing = EqualSplitShortestPath(nodes=self.nodes, links=self.links, demands=self.demands,
                                                     split=True, weights=self.weights, waypoints=self.waypoints)
            solution = post_processing.solve()

        pt_duration = time.process_time() - pt_start
        exe_time = time.process_time() - t

        # Aktualisiere Ausführungszeit
        solution["execution_time"] = exe_time
        solution["process_time"] = pt_duration
        return solution

    def get_name(self):
        return f"inverse_capacity"

    def get_link_utilization(self, link):
     i, j, c = link
     demands_to_j = [d for _, t, d in self.demands if t == j]
     f = sum(demands_to_j) if demands_to_j else 0
     max_c = max([c for _, _, c in self.links])
     return f / (max_c * self.threshold) if c != 0 else 0
   

    def compute_alternative_routes(self):

     alternative_routes = []

    # Hier könnte die Logik zur Berechnung der alternativen Routen eingefügt werden
    # basierend auf den vorhandenen Links, Nachfrageinformationen und bestimmten Kriterien oder Regeln

    # Beispiel: Füge eine alternative Route für jede Nachfrage hinzu, indem du den kürzesten Pfad umkehrst
     for demand in self.demands:
        s, t, _ = demand
        alternative_route = self.reverse_shortest_path(s, t)
        alternative_routes.append(alternative_route)

     return alternative_routes

    def reverse_shortest_path(self, source, target):
 
     shortest_path = self.get_shortest_path(source, target)
     reversed_path = shortest_path[::-1]  # Umkehrung der Reihenfolge der Links
     return reversed_path
    def solve_with_alternative_routes(self, alternative_routes):
     if alternative_routes:
        max_objective = 0
        max_objective_route = None

        for route in alternative_routes:
            # Kopie der Knoten, Links, Nachfragen und Gewichte erstellen
            nodes_copy = self.nodes.copy()
            links_copy = self.links.copy()
            demands_copy = self.demands.copy()
            weights_copy = self.weights.copy()

            # Löse das Problem mit der aktuellen alternativen Route
            post_processing = EqualSplitShortestPath(nodes=nodes_copy, links=links_copy, demands=demands_copy,
                                                     split=True, weights=weights_copy, waypoints=self.waypoints,
                                                     route=route)
            solution = post_processing.solve()

            # Berechnen Sie das Metrik für die aktuelle Route (z.B. Durchschnittliche Link-Auslastung)
            objective = self.compute_objective(solution)

            if objective > max_objective:
                max_objective = objective
                max_objective_route = route

        if max_objective > self.threshold:
            print(f"WARNING: Maximale Schwellenwert für das Metrik ({self.threshold}) überschritten!")
            # Implementieren Sie Notfallmaßnahmen oder weitere Logik für alternative Routen

        # Kopie der Knoten, Links, Nachfragen und Gewichte erstellen
        nodes_copy = self.nodes.copy()
        links_copy = self.links.copy()
        demands_copy = self.demands.copy()
        weights_copy = self.weights.copy()

        # Löse das Problem mit der Route mit dem maximalen Metrik
        post_processing = EqualSplitShortestPath(nodes=nodes_copy, links=links_copy, demands=demands_copy,
                                                 split=True, weights=weights_copy, waypoints=self.waypoints,
                                                 route=max_objective_route)
        solution = post_processing.solve()

        # Aktualisieren Sie die "objective" basierend auf dem maximalen Metrik
        objective = self.compute_objective(solution)
        solution["objective"] = objective

        return solution

     return None



    # Wenn keine alternativen Routen vorhanden sind, kann hier entsprechender Code hinzugefügt werden

    
    def get_shortest_path(self, source, target):
  
    # Verwendung des Dijkstra-Algorithmus, um den kürzesten Pfad zu berechnen
    # Hier ist ein Beispiel für die Verwendung der NetworkX-Bibliothek:

   

    # Erstellen Sie einen gerichteten Graphen basierend auf den vorhandenen Links und Gewichten
     graph = nx.DiGraph()
     for i, j, c in self.links:
        graph.add_edge(i, j, weight=self.weights[(i, j)])

    # Verwenden Sie den Dijkstra-Algorithmus, um den kürzesten Pfad zu berechnen
     shortest_path = nx.dijkstra_path(graph, source, target)

    # Geben Sie den kürzesten Pfad zurück
     return shortest_path
    def compute_normalized_utilization(self, solution):
     total_utilization = sum(self.get_link_utilization(link) for link in self.links)
     max_utilization = max(self.get_link_utilization(link) for link in self.links)
 
     if max_utilization > 0:
        normalized_utilization = total_utilization / max_utilization
     else:
        normalized_utilization = 0

     return normalized_utilization
    def compute_objective(self, solution):
     total_utilization = sum(self.get_link_utilization(link) for link in self.links)
     num_links = len(self.links)
     average_utilization = total_utilization / num_links
     return average_utilization

   


       
