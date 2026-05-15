# test_setup.py
from src.environment import NetworkGraph

# Initialize the Network
net = NetworkGraph()

# Build the Diamond Graph
# Parameters: start_node, end_node, a (congestion multiplier), b (base latency)
net.add_edge('S', 'A', a=1.0, b=0.0)  # S -> A: Cost = 1.0 * x
net.add_edge('S', 'B', a=0.0, b=10.0) # S -> B: Cost = 10 (constant)
net.add_edge('A', 'B', a=0.0, b=1.0)  # A -> B: Cost = 1 (constant, the cross-link)
net.add_edge('A', 'D', a=0.0, b=10.0) # A -> D: Cost = 10 (constant)
net.add_edge('B', 'D', a=1.0, b=0.0)  # B -> D: Cost = 1.0 * x

# Find all paths
paths = net.get_all_paths('S', 'D')

print(f"Found {len(paths)} valid paths from S to D:")
for idx, path in enumerate(paths):
    print(f"Path {idx + 1}: {path}")