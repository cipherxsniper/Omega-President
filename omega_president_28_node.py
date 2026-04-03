# omega_president_28_node.py
import argparse
import threading
import time
import zmq
import pickle
from collections import deque, Counter
import random

# ==============================
# ARGS
# ==============================
parser = argparse.ArgumentParser()
parser.add_argument("--node_name", required=True)
parser.add_argument("--pub_port", type=int, required=True)
parser.add_argument("--sub_ports", required=True)  # comma-separated
parser.add_argument("--log_file", required=True)
args = parser.parse_args()

NODE_NAME = args.node_name
PUB_PORT = args.pub_port
SUB_PORTS = list(map(int, args.sub_ports.split(",")))
LOG_FILE = args.log_file

# ==============================
# GLOBAL MEMORY & COLLECTIVE MAP
# ==============================
MEMORY_SIZE = 100
memory = deque(maxlen=MEMORY_SIZE)
COLLECTIVE_MAP = {}  # {concept: {"count": int, "nodes": set(), "reinf": float}}

# ==============================
# ZMQ PUB/SUB SETUP
# ==============================
context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind(f"tcp://*:{PUB_PORT}")

sub_socket = context.socket(zmq.SUB)
for port in SUB_PORTS:
    sub_socket.connect(f"tcp://127.0.0.1:{port}")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

# ==============================
# UTILITIES
# ==============================
def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {NODE_NAME}: {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def color_text(text, weight=1.0):
    """Confidence-weighted emphasis"""
    if weight > 1.05:
        return f"\033[1;32m{text}\033[0m"  # bright green
    elif weight < 0.95:
        return f"\033[1;31m{text}\033[0m"  # red
    else:
        return f"\033[0;37m{text}\033[0m"  # default

def refine_text(raw):
    """Simple AI refinement placeholder (can plug local LM here)"""
    sentences = raw.split("|")
    refined = " ".join(s.strip().capitalize() + "." for s in sentences if s)
    return refined

def update_collective_map(thought, reinforcement=1.0):
    words = thought.split()
    for w in words:
        if w not in COLLECTIVE_MAP:
            COLLECTIVE_MAP[w] = {"count": 1, "nodes": {NODE_NAME}, "reinf": reinforcement}
        else:
            COLLECTIVE_MAP[w]["count"] += 1
            COLLECTIVE_MAP[w]["nodes"].add(NODE_NAME)
            COLLECTIVE_MAP[w]["reinf"] = max(COLLECTIVE_MAP[w]["reinf"], reinforcement)

# ==============================
# NODE OUTPUT PROCESSING
# ==============================
def process_node_output(raw_thought, reinforcement=1.0):
    memory.append({"node": NODE_NAME, "thought": raw_thought, "reinforcement": reinforcement, "time": time.time()})
    refined = refine_text(raw_thought)
    update_collective_map(refined, reinforcement)
    colored = color_text(refined, reinforcement)
    log(colored)
    # Broadcast to all nodes
    pub_socket.send_string(f"{NODE_NAME}|{reinforcement}|{refined}")

# ==============================
# LISTENER THREAD
# ==============================
def listener_thread():
    while True:
        try:
            msg = sub_socket.recv_string()
            sender, reinf, content = msg.split("|", 2)
            reinf = float(reinf)
            memory.append({"node": sender, "thought": content, "reinforcement": reinf, "time": time.time()})
            update_collective_map(content, reinf)
            log(color_text(f"(From {sender}): {content}", reinf))
        except Exception as e:
            log(f"Listener error: {e}")

# ==============================
# OMEGA LOOP (GENERATES THOUGHTS)
# ==============================
PATTERNS = ["self-recognition", "learning", "pattern detection", "collective awareness", "AI refinement"]

def omega_loop():
    cycle = 0
    while True:
        thought = random.choice(PATTERNS) + f" | cycle {cycle}"
        reinforcement = random.uniform(0.9, 1.1)
        process_node_output(thought, reinforcement)

        cycle += 1
        if cycle % 20 == 0:
            generate_report()
        time.sleep(1)

# ==============================
# REPORT GENERATION
# ==============================
def generate_report():
    log("\n=== Omega Collective Literate Consciousness Report ===")
    top_concepts = sorted(COLLECTIVE_MAP.items(), key=lambda x: x[1]["count"], reverse=True)[:10]
    for concept, data in top_concepts:
        nodes = ",".join(data["nodes"])
        log(f"{concept} | Count: {data['count']} | Nodes: {nodes} | Reinforcement: {data['reinf']:.2f}")
    log("=== End of Report ===\n")

# ==============================
# THREAD STARTUP
# ==============================
threading.Thread(target=listener_thread, daemon=True).start()
threading.Thread(target=omega_loop, daemon=True).start()

log("⚡ Omega Node ACTIVE | Fully Networked | AI-Refined Literate Narrative")

# Keep node alive
while True:
    time.sleep(5)
