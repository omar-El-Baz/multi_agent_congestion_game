# src/simulation.py

class CongestionSimulation:
    def __init__(self, network, agents):
        self.network = network
        self.agents = agents
        # Get all valid paths for the given source and destination
        self.paths = self.network.get_all_paths(agents[0].source, agents[0].destination)

    def run(self, max_epochs=100):
        print(f"Starting simulation with {len(self.agents)} agents...")
        convergence_history = []  # NEW: Track changes per epoch
        
        for agent in self.agents:
            agent.update_path(self.paths[0], self.network)

        for epoch in range(1, max_epochs + 1):
            strategies_changed = 0

            for agent in self.agents:
                best_path = agent.current_path
                min_cost = agent.evaluate_path_cost(best_path, self.network)

                for path in self.paths:
                    cost = agent.evaluate_path_cost(path, self.network)
                    if cost < min_cost:
                        min_cost = cost
                        best_path = path

                if best_path != agent.current_path:
                    agent.update_path(best_path, self.network)
                    strategies_changed += 1

            print(f"Epoch {epoch}: {strategies_changed} agents changed paths.")
            convergence_history.append(strategies_changed) # NEW: Store the data

            if strategies_changed == 0:
                print("\n--- Nash Equilibrium Reached! ---")
                self.print_results()
                break
                
        return convergence_history 
    
    def print_results(self):
        print("Final Path Distribution:")
        path_counts = {tuple(path): 0 for path in self.paths}
        for agent in self.agents:
            path_counts[tuple(agent.current_path)] += 1
        
        for path, count in path_counts.items():
            print(f"Path {path}: {count} agents")
            
        print("\nFinal Costs per Path:")
        for path, count in path_counts.items():
            if count > 0:
                # Grab a sample agent on this path to see what they are paying
                sample_agent = next(a for a in self.agents if tuple(a.current_path) == path)
                cost = sample_agent.evaluate_path_cost(list(path), self.network)
                print(f"Cost for Path {path}: {cost:.2f}")