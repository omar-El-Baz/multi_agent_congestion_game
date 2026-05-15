# scripts/run_experiments.py
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.environment import NetworkGraph
from src.agents import Agent
from src.simulation import CongestionSimulation
from src.optimizer import SocialOptimumSolver

# Set up Seaborn for professional, academic styling
sns.set_theme(style="whitegrid")

def setup_braess_network():
    net = NetworkGraph()
    net.add_edge('S', 'A', a=0.01, b=0.0)
    net.add_edge('S', 'B', a=0.0, b=45.0)
    net.add_edge('A', 'B', a=0.0, b=0.0)
    net.add_edge('A', 'D', a=0.0, b=45.0)
    net.add_edge('B', 'D', a=0.01, b=0.0)
    return net

def run_scaling_experiment():
    agent_counts = [500, 1000, 2000, 3000, 4000]
    nash_costs = []
    optimal_costs = []

    print("Running scaling experiments...")
    for count in agent_counts:
        print(f"Testing with {count} agents...")
        net_nash = setup_braess_network()
        net_opt = setup_braess_network()
        
        agents_nash = [Agent(i, 'S', 'D') for i in range(count)]
        agents_opt = [Agent(i, 'S', 'D') for i in range(count)]

        # Run Nash Simulation
        sim = CongestionSimulation(net_nash, agents_nash)
        sim.run(max_epochs=10) # Limit epochs for faster experiment runs
        
        # Calculate Nash average cost
        nash_total = sum(edge.current_load * edge.get_cost() for edge in net_nash.edges.values())
        nash_costs.append(nash_total / count)

        # Run Social Optimum
        optimizer = SocialOptimumSolver(net_opt, agents_opt)
        _, opt_avg = optimizer.solve_marginal_cost_assignment()
        optimal_costs.append(opt_avg)

    return agent_counts, nash_costs, optimal_costs

def plot_results(agent_counts, nash_costs, optimal_costs):
    # Plot 1: Line Chart of Average Cost vs Number of Players
    plt.figure(figsize=(10, 6))
    plt.plot(agent_counts, nash_costs, label='Selfish Routing (Nash Equilibrium)', marker='o', color='#e74c3c', linewidth=2)
    plt.plot(agent_counts, optimal_costs, label='Coordinated Routing (Social Optimum)', marker='s', color='#2ecc71', linewidth=2)
    
    plt.title("Average Latency vs. Number of Players in Braess's Paradox", fontsize=14, pad=15)
    plt.xlabel("Number of Players", fontsize=12)
    plt.ylabel("Average Cost (Latency)", fontsize=12)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('docs/scaling_experiment.png', dpi=300)
    print("Saved scaling plot to docs/scaling_experiment.png")

    # Plot 2: Bar Chart showing the Price of Anarchy at 4000 agents
    plt.figure(figsize=(8, 6))
    labels = ['Selfish (Nash)', 'Coordinated (Optimum)']
    values = [nash_costs[-1], optimal_costs[-1]]
    colors = ['#e74c3c', '#2ecc71']

    bars = plt.bar(labels, values, color=colors, width=0.5)
    plt.title("Efficiency Comparison (4000 Players)", fontsize=14, pad=15)
    plt.ylabel("Average Cost", fontsize=12)
    
    # Add exact values on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval:.2f}", ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('docs/efficiency_comparison.png', dpi=300)
    print("Saved efficiency bar chart to docs/efficiency_comparison.png")

if __name__ == "__main__":
    counts, nash, opt = run_scaling_experiment()
    plot_results(counts, nash, opt)