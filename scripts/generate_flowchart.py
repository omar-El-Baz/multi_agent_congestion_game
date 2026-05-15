# scripts/generate_flowchart.py
from graphviz import Digraph
from pathlib import Path

def generate_simulation_flowchart():
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / 'docs'
    docs_dir.mkdir(exist_ok=True)

    # Initialize a directed graph
    dot = Digraph(comment='Best Response Dynamics Flowchart', format='png')
    
    # Global visual settings suitable for IEEE
    dot.attr(rankdir='TB', size='8,10', dpi='300')
    dot.attr('node', shape='box', style='filled, rounded', color='#34495e', 
             fillcolor='#ecf0f1', fontname='Helvetica', fontsize='12')
    dot.attr('edge', fontname='Helvetica', fontsize='11', color='#2c3e50')

    # Define Nodes
    dot.node('Start', 'Start Simulation\nInitialize all agents on Path 0', shape='ellipse', fillcolor='#d5f5e3')
    dot.node('Epoch', 'For epoch = 1 to max_epochs:')
    dot.node('Reset', 'strategies_changed = 0')
    dot.node('AgentLoop', 'For each agent in agents:')
    dot.node('Eval', 'Evaluate hypothetical cost C(x)\nfor all valid paths')
    dot.node('Decision', 'Is there a path with\nCost < Current Path Cost?', shape='diamond', fillcolor='#fcf3cf')
    dot.node('Switch', 'agent.update_path(best_path)\nstrategies_changed += 1')
    dot.node('NextAgent', 'Next Agent')
    dot.node('CheckEquilibrium', 'strategies_changed == 0?', shape='diamond', fillcolor='#fcf3cf')
    dot.node('End', 'Nash Equilibrium Reached\nSimulation Ends', shape='ellipse', fillcolor='#fadbd8')

    # Define Edges (Flow)
    dot.edge('Start', 'Epoch')
    dot.edge('Epoch', 'Reset')
    dot.edge('Reset', 'AgentLoop')
    dot.edge('AgentLoop', 'Eval')
    dot.edge('Eval', 'Decision')
    
    # Agent switching logic
    dot.edge('Decision', 'Switch', label=' Yes')
    dot.edge('Decision', 'NextAgent', label=' No')
    dot.edge('Switch', 'NextAgent')
    
    # Loops
    dot.edge('NextAgent', 'AgentLoop', label=' More agents')
    dot.edge('NextAgent', 'CheckEquilibrium', label=' All agents evaluated')
    
    # Equilibrium Check Logic
    dot.edge('CheckEquilibrium', 'End', label=' Yes (Stable State)')
    dot.edge('CheckEquilibrium', 'Epoch', label=' No (Next Epoch)')

    # Save directly to the docs folder using pathlib
    output_path = docs_dir / 'simulation_flowchart'
    dot.render(str(output_path), view=True, cleanup=True)
    print(f"Flowchart successfully saved to {output_path}.png")

if __name__ == "__main__":
    generate_simulation_flowchart()