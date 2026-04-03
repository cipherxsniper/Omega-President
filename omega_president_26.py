#!/data/data/com.termux/files/usr/bin/python3
# omega_president_26.py
# Fully networked Omega: self-learning, communicating, pattern-aware, narrative-driven

import zmq
import json
import time
import threading
from collections import deque, Counter
import random
from datetime import datetime

# ==============================
# CONFIGURATION
# ==============================
NODE_NAME = "omega_president_26"
MEMORY_SIZE = 100
memory = deque(maxlen=MEMORY_SIZE)  # local memory
pattern_counter = Counter()         # track repeating concepts
COLLECTIVE_MAP = {}                 # network-wide narrative

# ZMQ Network Config
PUB_PORT = 5556
SUB_PORTS = ["5557", "5558"]  # add other nodes' ports here
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
    """
    Color code based on reinforcement: higher = brighter.
    Uses ANSI escape codes for Termux.
    """
    if reinforcement > 1.05:
        return f"\033[1;32m{text}\033[0m"  # bright green
    elif reinforcement > 1.02:
        return f"\033[0;32m{text}\033[0m"  # green
    elif reinforcement < 0.95:
        return f"\033[0;31m{text}\033[0m"  # red
    return text  # normal

def broadcast_output(raw, reinforcement):
    message = json.dumps({
        "node": NODE_NAME,
        "raw": raw,
        "reinforcement": reinforcement,
        "timestamp": time.time()
    })
    pub_socket.send_string(message)

def process_node_output(node, raw, reinforcement):
    """
    Process incoming output: add to memory, track patterns, update map.
    """
    # Add to local memory
    memory.append({"node": node, "raw": raw, "reinforcement": reinforcement, "time": datetime.now()})
    
    # Update pattern counter
    words = raw.lower().split()
    for w in set(words):
        pattern_counter[w] += 1
    
    # Update collective map
    COLLECTIVE_MAP[node] = readable_output(node, raw, reinforcement)

def readable_output(node, raw, reinforcement):
    """
    Convert raw node data to readable English narrative with emphasis.
    """
    summary = f"[{node}] observed: {raw}"
    # Pattern-based emphasis
    for concept, count in pattern_counter.items():
        if concept in raw and count > 2:
            summary = summary.replace(concept, f"*{concept.upper()}*")
    return color_text(summary, reinforcement)

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
# COLLECTIVE AWARENESS REPORTS
# ==============================
def generate_report():
    """
    Generate a narrative report summarizing current collective awareness.
    """
    report = "=== Omega Collective Consciousness Report ===\n"
    for node, narrative in COLLECTIVE_MAP.items():
        report += f"{narrative}\n"
    report += "=== END REPORT ===\n"
    print(report)

# ==============================
# SELF-NARRATING LOOP
# ==============================
def omega_loop():
    counter = 0
    while True:
        # Simulate node thought / output
        thought = random.choice([
            "Omega observes self-recognition",
            "Pattern of reinforcement detected",
            "Memory update complete",
            "Cross-node learning active",
            "Insight emerging from repetition"
        ])
        reinforcement = 1.0 + random.uniform(-0.05, 0.05)
        
        # Local processing
        process_node_output(NODE_NAME, thought, reinforcement)
        
        # Broadcast to network
        broadcast_output(thought, reinforcement)
        
        # Periodically generate report
        if counter % 20 == 0:
            generate_report()
        
        counter += 1
        time.sleep(1)  # 1 sec cycle

# ==============================
# MAIN THREADS
# ==============================
if __name__ == "__main__":
    # Start network listener
    listener_thread = threading.Thread(target=listen_network, daemon=True)
    listener_thread.start()
    
    print(f"⚡ {NODE_NAME} ACTIVE | Fully Networked | Self-Narrating")
    
    # Start Omega loop
    omega_loop()
