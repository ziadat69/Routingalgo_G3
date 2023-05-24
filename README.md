
# ZIADAT AHMAD ARBEIT IN PRKN DATEI
In meinem neuen Projekt habe ich einen Algorithmus entwickelt, der auf dem Konzept der inversen Kapazität basiert. Die Idee besteht darin, die Gewichte der Verbindungen in einem Netzwerk umzukehren, basierend auf ihrer Kapazität. Dadurch werden Links mit hoher Kapazität bevorzugt und erhalten niedrigere Gewichte für die Routenauswahl.
Der Algorithmus nutzt den kürzesten Pfad-Algorithmus, um optimale Routen für gegebene Nachfragepaare zu finden. Zusätzlich habe ich eine Funktion implementiert, um alternative Routen zu berechnen, indem der kürzeste Pfad umgekehrt wird.
Um die Link-Auslastung zu überwachen, habe ich eine Funktion entwickelt, die die Auslastung jedes Links basierend auf aktuellen Nachfrageinformationen berechnet. Ich habe auch eine maximale Link-Auslastungsschwelle definiert, um sicherzustellen, dass diese nicht überschritten wird.
Wenn die maximale Link-Auslastungsschwelle überschritten wird, ergreift der Algorithmus alternative Maßnahmen. Dies kann die Berechnung und Nutzung von alternativen Routen oder die Implementierung von Notfallmaßnahmen umfassen.
Für die Berechnung des kürzesten Pfads habe ich die NetworkX-Bibliothek und den Dijkstra-Algorithmus verwendet. Die Metriken, wie die Auslastung der Links und das Zielkriterium, werden berechnet, um die Leistung des Algorithmus zu bewerten.
Die Lösung des Algorithmus enthält Informationen über die berechneten Metriken, alternative Routen und Ausführungszeiten.
Insgesamt zielt mein Projekt darauf ab, die Kapazität der Links effizient zu nutzen und alternative Routen zu finden, um die Netzwerkleistung zu verbessern. Ich habe Maßnahmen implementiert, um die Link-Auslastung unter einer definierten Schwelle zu halten und gegebenenfalls Notfallmaßnahmen umzusetzen.
# ALI ALMAZAAL ARBEIT IN TE_SR_WAN_simulation-main
 In meinem neuen Projekt habe ich den Algorithmus DemandsFirstWaypoints weiter entwickelt.  

# BOUALI AMIN 
In meinem Projekt habe ich Uniform_weights und Demand_first_waypoint in dieser reihen folge sequenziert und analysiert.
Ziel war es die MLU zu verbessern, was geklappt hat , jedoch sehr auf kosten der Laufzeit.

Um mein Projekt zu replizieren, brauchen man nur das urspüngliche Repository TE_SR_WAN und ersetzt darin die main und sequential Klassen, mit den in dem Ordner Amin bereitgestellten Dateien.

Hier das ursprüngliche Repository, befolgt dabei die Anweisungen bezüglich der Installation.
https://github.com/tfenz/TE_SR_WAN_simulation
