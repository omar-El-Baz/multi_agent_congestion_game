# scripts/generate_topology.py
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path

def generate_network_topology():
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / 'docs'
    docs_dir.mkdir(exist_ok=True) # Creates the folder if it somehow gets deleted

    plt.figure(figsize=(8, 6))
    G = nx.DiGraph()

    # Add nodes S (Source), A, B, and D (Destination)
    G.add_nodes_from(['S', 'A', 'B', 'D'])

    # Define positions to create the classic Diamond shape
    pos = {
        'S': (0, 0.5), 
        'A': (1, 1), 
        'B': (1, 0), 
        'D': (2, 0.5)
    }

    # Add directed edges
    edges = [('S', 'A'), ('S', 'B'), ('A', 'B'), ('A', 'D'), ('B', 'D')]
    G.add_edges_from(edges)

    # 1. Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=2500, node_color='#ecf0f1', edgecolors='#2c3e50', linewidths=2)
    
    # 2. Draw edges with arrows
    nx.draw_networkx_edges(G, pos, edgelist=edges, arrowstyle='-|>', arrowsize=25, 
                           node_size=2500, edge_color='#34495e', width=2)

    # 3. Draw node labels (S, A, B, D)
    nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold', font_family='sans-serif', font_color='#2c3e50')

    # 4. Define and draw edge labels
    edge_labels = {
        ('S', 'A'): 'C(x) = 0.01x',
        ('S', 'B'): 'C(x) = 45',
        ('A', 'B'): 'C(x) = 0',
        ('A', 'D'): 'C(x) = 45',
        ('B', 'D'): 'C(x) = 0.01x'
    }

    # Use a white bounding box so the text is readable over the lines
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=13, 
                                 font_weight='bold', label_pos=0.5,
                                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=2))

    # Formatting
    plt.title("Braess's Paradox Network Topology", fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    # Save directly to the docs folder using pathlib
    save_path = docs_dir / 'network_topology.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Network topology successfully saved to {save_path}")
    plt.show()

if __name__ == "__main__":
    generate_network_topology()