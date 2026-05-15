# src/optimizer.py

class SocialOptimumSolver:
    def __init__(self, network, agents):
        self.network = network
        self.num_agents = len(agents)
        # Assuming all agents have the same source/destination for this project scope
        self.source = agents[0].source
        self.destination = agents[0].destination
        self.paths = self.network.get_all_paths(self.source, self.destination)

    def solve_marginal_cost_assignment(self):
        """
        Assigns agents one-by-one to the path that causes the smallest 
        increase to the TOTAL system cost, ignoring individual selfishness.
        """
        # Reset the network load to 0 before optimizing
        for edge in self.network.edges.values():
            edge.current_load = 0

        path_counts = {tuple(p): 0 for p in self.paths}

        print("Calculating Social Optimum (Centralized Routing)...")
        for _ in range(self.num_agents):
            best_path = None
            min_marginal_system_cost = float('inf')

            for path in self.paths:
                marginal_cost = 0
                for edge_tuple in path:
                    edge = self.network.edges[edge_tuple]
                    
                    # Current total cost of this edge: load * cost_formula
                    current_edge_total_cost = edge.current_load * edge.get_cost()
                    
                    # What the total cost WOULD be if we added 1 more person
                    new_load = edge.current_load + 1
                    new_edge_total_cost = new_load * edge.get_cost(new_load)
                    
                    # The difference is the damage this new agent does to the system
                    marginal_cost += (new_edge_total_cost - current_edge_total_cost)

                if marginal_cost < min_marginal_system_cost:
                    min_marginal_system_cost = marginal_cost
                    best_path = tuple(path)

            # Route the agent onto the path that does the least system-wide damage
            path_counts[best_path] += 1
            for edge_tuple in best_path:
                self.network.edges[edge_tuple].add_agent()

        # Calculate final metrics
        total_system_cost = sum(
            edge.current_load * edge.get_cost() 
            for edge in self.network.edges.values()
        )
        average_cost = total_system_cost / self.num_agents

        self.print_results(path_counts, average_cost, total_system_cost)
        return path_counts, average_cost

    def print_results(self, path_counts, average_cost, total_cost):
        print("\n--- Social Optimum Reached! ---")
        print("Optimized Path Distribution:")
        for path, count in path_counts.items():
            print(f"Path {path}: {count} agents")
            
        print(f"\nAverage Cost per Agent: {average_cost:.2f}")
        print(f"Total System Cost: {total_cost:.2f}")