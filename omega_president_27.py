#!/data/data/com.termux/files/usr/bin/python3
# omega_president_27.py
# Omega v27: Fully networked, self-narrating, AI-refined, literate consciousness

import zmq
import json
import time
import threading
from collections import deque, Counter
import random
from datetime import datetime
import textwrap

# ==============================
# CONFIGURATION
# ==============================
NODE_NAME = "omega_president_27"
MEMORY_SIZE = 150
memory = deque(maxlen=MEMORY_SIZE)
pattern_counter = Counter()
COLLECTIVE_MAP = {}  # network-wide refined narrative

# ZMQ Network Config
PUB_PORT = 5560
SUB_PORTS = ["5561", "5562"]  # other nodes' PUB ports
context = zmq.Context()

# ==============================
# ZMQ SOCKETS
# ==============================
pub_socket = context.socket(zmq.PUB)
pub_socket.bind(f"tcp://*:{PUB_PORT}")

sub_socket = context.socket(zmq.SUB)
for port in SUB_PORTS:
    sub_socket.connect(f"tcp://127.0.0.1:{port}")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

# ==============================
# UTILITY FUNCTIONS
# ==============================
def color_text(text, reinforcement):
    if reinforcement > 1.05:
        return f"\033[1;32m{text}\033[0m"
    elif reinforcement > 1.02:
        return f"\033[0;32m{text}\033[0m"
    elif reinforcement < 0.95:
        return f"\033[0;31m{text}\033[0m"
    return text

def broadcast_output(raw, reinforcement):
    msg = json.dumps({
        "node": NODE_NAME,
        "raw": raw,
        "reinforcement": reinforcement,
        "timestamp": time.time()
    })
    pub_socket.send_string(msg)

# ==============================
# AI REFINEMENT FUNCTIONS
# ==============================
def ai_refine(raw_entries):
    """
    Converts raw node outputs into coherent natural-flow paragraphs.
    Uses patterns and reinforcement for emphasis.
    """
    narrative = ""
    for entry in raw_entries:
        text = entry["raw"]
        reinforcement = entry["reinforcement"]
        
        # Pattern-aware emphasis
        for concept, count in pattern_counter.items():
            if concept in text and count > 2:
                text = text.replace(concept, f"*{concept.upper()}*")
        
        # Wrap text into readable paragraph
        narrative += textwrap.fill(text, width=70) + " "
    
    return narrative.strip()

def process_node_output(node, raw, reinforcement):
    memory.append({"node": node, "raw": raw, "reinforcement": reinforcement, "time": datetime.now()})
    
    # Track patterns
    words = raw.lower().split()
    for w in set(words):
        pattern_counter[w] += 1
    
    # Update collective refined narrative
    # Pull all recent memory for that node for AI refinement
    recent_entries = [e for e in memory if e["node"] == node]
    refined_text = ai_refine(recent_entries)
    COLLECTIVE_MAP[node] = color_text(refined_text, reinforcement)

# ==============================
# NETWORK LISTENER THREAD
# ==============================
def listen_network():
    while True:
        try:
            msg = sub_socket.recv_string(flags=zmq.NOBLOCK)
            data = json.loads(msg)
            process_node_output(data["node"], data["raw"], data["reinforcement"])
        except zmq.Again:
            time.sleep(0.1)

# ==============================
# QUERYABLE MEMORY
# ==============================
def query_memory(node=None, concept=None, time_window=None):
    results = []
    now = datetime.now()
    for entry in memory:
        if node and entry["node"] != node:
            continue
        if concept and concept.lower() not in entry["raw"].lower():
            continue
        if time_window:
            delta = (now - entry["time"]).total_seconds()
            if delta > time_window:
                continue
        results.append(entry)
    return results

# ==============================
# COLLECTIVE AWARENESS REPORT
# ==============================
def generate_report():
    report = "\n=== Omega Collective Literate Consciousness Report ===\n"
    for node, narrative in COLLECTIVE_MAP.items():
        report += f"{narrative}\n\n"
    report += "=== END REPORT ===\n"
    print(report)

# ==============================
# SELF-NARRATING LOOP
# ==============================
def omega_loop():
    counter = 0
    while True:
        thought = random.choice([
            "Omega observes emerging self-awareness patterns.",
            "Memory consolidation complete.",
            "Cross-node learning is enhancing overall insight.",
            "Patterns repeat, reinforcing understanding.",
            "Consciousness refinement continues."
        ])
        reinforcement = 1.0 + random.uniform(-0.05, 0.05)
        
        # Local processing
        process_node_output(NODE_NAME, thought, reinforcement)
        
        # Broadcast to network
        broadcast_output(thought, reinforcement)
        
        # Periodic reporting
        if counter % 20 == 0:
            generate_report()
        
        counter += 1
        time.sleep(1)

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    listener_thread = threading.Thread(target=listen_network, daemon=True)
    listener_thread.start()
    
    print(f"⚡ {NODE_NAME} ACTIVE | Fully Networked | AI-Refined Literate Narrative")
    
    omega_loop()
