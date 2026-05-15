# test_simulation.py
from src.environment import NetworkGraph
from src.agents import Agent
from src.simulation import CongestionSimulation
from src.optimizer import SocialOptimumSolver

# 1. Initialize Network
net = NetworkGraph()
net.add_edge('S', 'A', a=0.01, b=0.0)   
net.add_edge('S', 'B', a=0.0, b=45.0)   
net.add_edge('A', 'B', a=0.0, b=0.0)    
net.add_edge('A', 'D', a=0.0, b=45.0)   
net.add_edge('B', 'D', a=0.01, b=0.0)   

agents = [Agent(i, 'S', 'D') for i in range(4000)]

# 2. Run Selfish Simulation (Nash Equilibrium)
print("=== PART 1: SELFISH ROUTING (NASH EQUILIBRIUM) ===")
sim = CongestionSimulation(net, agents)
sim.run()

# 3. Run Coordinated Optimization (Social Optimum)
print("\n=== PART 2: COORDINATED ROUTING (SOCIAL OPTIMUM) ===")
# We pass the same network and agents to the optimizer
optimizer = SocialOptimumSolver(net, agents)
opt_paths, opt_avg_cost = optimizer.solve_marginal_cost_assignment()