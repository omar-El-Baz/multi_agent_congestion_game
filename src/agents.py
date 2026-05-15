# src/agents.py

class Agent:
    def __init__(self, agent_id: int, source: str, destination: str):
        self.agent_id = agent_id
        self.source = source
        self.destination = destination
        self.current_path = []  # List of edge tuples

    def evaluate_path_cost(self, path: list, network) -> float:
        """Calculates the hypothetical cost of a path."""
        total_cost = 0.0
        for edge_tuple in path:
            edge = network.edges[edge_tuple]
            is_on_edge = edge_tuple in self.current_path
            hypothetical_load = edge.current_load if is_on_edge else edge.current_load + 1
            total_cost += edge.get_cost(hypothetical_load)
        return total_cost

    def update_path(self, new_path: list, network):
        """Removes the agent from the old path and adds them to the new path."""
        # Remove load from the old edges
        for edge_tuple in self.current_path:
            network.edges[edge_tuple].remove_agent()
            
        # Add load to the new edges
        for edge_tuple in new_path:
            network.edges[edge_tuple].add_agent()
            
        self.current_path = new_path