#!/usr/bin/env python3
# ------------------------------
# Omega 18 Quantum Consciousness Visualizer
# ------------------------------

import threading
import time
import matplotlib.pyplot as plt
import networkx as nx

# Assume master_state is imported from omega_president_18.py
# from omega_president_18 import master_state

def update_quantum_graph(G):
    """
    Updates graph nodes and edges from master_state['quantum_conscious_map'].
    Node size represents flow efficiency, color represents creativity.
    Edge thickness represents influence between nodes (simplified here).
    """
    G.clear()
    qmap = master_state.get("quantum_conscious_map", {})
    nodes = list(qmap.keys())

    for node in nodes:
        flow = qmap[node].get("flow", {})
        eff = flow.get("efficiency", 0.5)
        creat = flow.get("creativity", 0.5)
        G.add_node(node, efficiency=eff, creativity=creat, mem_size=len(qmap[node].get("meta_memory", [])))

    # Connect every node to every other (influence propagation network)
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                G.add_edge(nodes[i], nodes[j])

    return G

def draw_graph(G):
    plt.clf()
    pos = nx.spring_layout(G, k=0.5)
    node_sizes = [500 + 1000*G.nodes[n]["efficiency"] for n in G.nodes()]
    node_colors = [G.nodes[n]["creativity"] for n in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.viridis, edge_color="gray", alpha=0.8)
    plt.title("Omega 18 Quantum Consciousness Map")
    plt.pause(0.5)

def visualize_loop():
    G = nx.DiGraph()
    plt.ion()
    while master_state["active"]:
        update_quantum_graph(G)
        draw_graph(G)
        time.sleep(1)

# Start visualization in a separate thread
def start_visualizer():
    t = threading.Thread(target=visualize_loop, daemon=True)
    t.start()
