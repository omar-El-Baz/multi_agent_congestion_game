import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.environment import NetworkGraph
from src.agents import Agent
from src.simulation import CongestionSimulation
from src.optimizer import SocialOptimumSolver

sns.set_theme(style="whitegrid")

def setup_braess_network():
    """Network WITH the A->B cross-link (Resource Added)"""
    net = NetworkGraph()
    net.add_edge('S', 'A', a=0.01, b=0.0)
    net.add_edge('S', 'B', a=0.0, b=45.0)
    net.add_edge('A', 'B', a=0.0, b=0.0)  # The problematic resource
    net.add_edge('A', 'D', a=0.0, b=45.0)
    net.add_edge('B', 'D', a=0.01, b=0.0)
    return net

def setup_standard_network():
    """Network WITHOUT the A->B cross-link (Resource Removed)"""
    net = NetworkGraph()
    net.add_edge('S', 'A', a=0.01, b=0.0)
    net.add_edge('S', 'B', a=0.0, b=45.0)
    # Notice: 'A' to 'B' edge is missing here
    net.add_edge('A', 'D', a=0.0, b=45.0)
    net.add_edge('B', 'D', a=0.01, b=0.0)
    return net

def run_all_experiments():
    agent_counts = [500, 1000, 2000, 3000, 4000]
    
    # Data storage
    total_costs_braess_nash = []
    total_costs_braess_opt = []
    total_costs_standard_nash = []
    convergence_data_4000 = []

    print("Running comprehensive experiments...")
    for count in agent_counts:
        print(f"\n--- Testing with {count} agents ---")
        
        # 1. Braess Network (Selfish)
        net_braess = setup_braess_network()
        sim_braess = CongestionSimulation(net_braess, [Agent(i, 'S', 'D') for i in range(count)])
        history = sim_braess.run(max_epochs=15)
        
        if count == 4000:
            convergence_data_4000 = history # Save history for the convergence plot
            
        braess_total = sum(edge.current_load * edge.get_cost() for edge in net_braess.edges.values())
        total_costs_braess_nash.append(braess_total)

        # 2. Braess Network (Social Optimum)
        net_opt = setup_braess_network()
        optimizer = SocialOptimumSolver(net_opt, [Agent(i, 'S', 'D') for i in range(count)])
        optimizer.solve_marginal_cost_assignment()
        opt_total = sum(edge.current_load * edge.get_cost() for edge in net_opt.edges.values())
        total_costs_braess_opt.append(opt_total)

        # 3. Standard Network (Resource Removed - Selfish)
        net_standard = setup_standard_network()
        sim_standard = CongestionSimulation(net_standard, [Agent(i, 'S', 'D') for i in range(count)])
        sim_standard.run(max_epochs=15)
        standard_total = sum(edge.current_load * edge.get_cost() for edge in net_standard.edges.values())
        total_costs_standard_nash.append(standard_total)

    return agent_counts, total_costs_braess_nash, total_costs_braess_opt, total_costs_standard_nash, convergence_data_4000

def generate_plots(counts, braess_nash, braess_opt, standard_nash, convergence_history):
    # Plot 1: Total Cost vs Players (Fixes the Average Latency deviation)
    plt.figure(figsize=(10, 6))
    plt.plot(counts, braess_nash, label='Nash (With Cross-link)', marker='o', color='#e74c3c')
    plt.plot(counts, braess_opt, label='Social Optimum (With Cross-link)', marker='s', color='#2ecc71')
    plt.title("Total System Cost vs. Number of Players", fontsize=14)
    plt.xlabel("Number of Players", fontsize=12)
    plt.ylabel("Total System Cost", fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.savefig('docs/total_cost_scaling.png', dpi=300)

    # Plot 2: Adding/Removing Resources
    plt.figure(figsize=(10, 6))
    plt.plot(counts, braess_nash, label='With Cross-link (Braess)', marker='o', color='#e74c3c')
    plt.plot(counts, standard_nash, label='Without Cross-link (Standard)', marker='^', color='#3498db')
    plt.title("Impact of Removing a Resource on Selfish Routing", fontsize=14)
    plt.xlabel("Number of Players", fontsize=12)
    plt.ylabel("Total System Cost", fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.savefig('docs/resource_impact.png', dpi=300)

    # Plot 3: Convergence of Strategies
    plt.figure(figsize=(8, 5))
    epochs = range(1, len(convergence_history) + 1)
    plt.plot(epochs, convergence_history, marker='o', color='#9b59b6', linestyle='-')
    plt.title("Strategy Convergence over Time (4000 Players)", fontsize=14)
    plt.xlabel("Epoch", fontsize=12)
    plt.ylabel("Number of Agents Changing Paths", fontsize=12)
    plt.xticks(epochs)
    plt.tight_layout()
    plt.savefig('docs/strategy_convergence.png', dpi=300)

    print("\nAll plots successfully saved to docs/ directory!")

if __name__ == "__main__":
    results = run_all_experiments()
    generate_plots(*results)