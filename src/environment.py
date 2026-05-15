# src/environment.py

class Edge:
    def __init__(self, start_node: str, end_node: str, a: float, b: float):
        self.start_node = start_node
        self.end_node = end_node
        self.a = a  # Congestion multiplier
        self.b = b  # Base latency
        self.current_load = 0

    def get_cost(self, hypothetical_load: int = None) -> float:
        """Calculates cost: Cost = a * load + b"""
        load = hypothetical_load if hypothetical_load is not None else self.current_load
        return (self.a * load) + self.b

    def add_agent(self):
        self.current_load += 1

    def remove_agent(self):
        if self.current_load > 0:
            self.current_load -= 1

class NetworkGraph:
    def __init__(self):
        self.edges = {}          # Dictionary mapping (u, v) -> Edge object
        self.adjacency_list = {} # Dictionary mapping u -> [list of neighbors]

    def add_edge(self, u: str, v: str, a: float, b: float):
        self.edges[(u, v)] = Edge(u, v, a, b)
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        self.adjacency_list[u].append(v)

    def get_all_paths(self, source: str, destination: str) -> list:
        """Uses Depth First Search (DFS) to find all simple paths from S to D."""
        paths = []
        
        def dfs(current_node, current_path_nodes, current_path_edges):
            if current_node == destination:
                paths.append(list(current_path_edges))
                return
            
            if current_node in self.adjacency_list:
                for neighbor in self.adjacency_list[current_node]:
                    if neighbor not in current_path_nodes: # Prevent infinite loops/cycles
                        current_path_nodes.add(neighbor)
                        current_path_edges.append((current_node, neighbor))
                        
                        dfs(neighbor, current_path_nodes, current_path_edges)
                        
                        # Backtrack
                        current_path_edges.pop()
                        current_path_nodes.remove(neighbor)

        dfs(source, {source}, [])
        return paths