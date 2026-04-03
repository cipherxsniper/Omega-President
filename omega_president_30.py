# omega_president_30.py
import zmq
import threading
import time
import random
from collections import deque, Counter
import pickle
from datetime import datetime
from pathlib import Path

# Optional: Local LM for narrative refinement
try:
    from transformers import pipeline
    lm_refiner = pipeline("text-generation", model="EleutherAI/gpt-neox-20b", device=0)
except Exception:
    lm_refiner = None
    print("[WARNING] Local LM not loaded. Outputs will be raw text.")

# ===============================
# CONFIGURATION
# ===============================
MEMORY_SIZE = 100
memory = deque(maxlen=MEMORY_SIZE)
COLLECTIVE_MAP = {}

NUM_NODES = 3
NODE_ID = None
PUB_PORT_BASE = 5560
SUB_PORTS = []

# Reinforcement and confidence tracking
reinforcement_scores = Counter()
COLOR_CODES = {
    "HIGH": "\033[92m",  # green
    "MED": "\033[93m",   # yellow
    "LOW": "\033[91m",   # red
    "END": "\033[0m"
}

# ===============================
# HUB & NODE INITIALIZATION
# ===============================
def start_hub():
    context = zmq.Context()
    hub_socket = context.socket(zmq.PUB)
    hub_socket.bind(f"tcp://*:{PUB_PORT_BASE}")
    print(f"⚡ Hub ONLINE on port {PUB_PORT_BASE}")
    return hub_socket, context

def connect_node(node_id):
    global SUB_PORTS, NODE_ID
    NODE_ID = node_id
    context = zmq.Context()
    pub_port = PUB_PORT_BASE + node_id - 1
    sub_ports = [PUB_PORT_BASE + i for i in range(NUM_NODES) if i != node_id-1]
    SUB_PORTS = sub_ports

    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind(f"tcp://*:{pub_port}")

    sub_socket = context.socket(zmq.SUB)
    for port in sub_ports:
        sub_socket.connect(f"tcp://127.0.0.1:{port}")
        sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

    print(f"⚡ Node {NODE_ID} connected | PUB:{pub_port} SUB:{sub_ports}")
    return pub_socket, sub_socket, context

# ===============================
# MEMORY & COLLECTIVE MAP HANDLING
# ===============================
def save_state():
    Path("state").mkdir(exist_ok=True)
    with open("state/memory.pkl", "wb") as f:
        pickle.dump(memory, f)
    with open("state/collective_map.pkl", "wb") as f:
        pickle.dump(COLLECTIVE_MAP, f)

def load_state():
    global memory, COLLECTIVE_MAP
    try:
        with open("state/memory.pkl", "rb") as f:
            memory = pickle.load(f)
        with open("state/collective_map.pkl", "rb") as f:
            COLLECTIVE_MAP = pickle.load(f)
        print("⚡ Loaded previous state")
    except Exception:
        print("⚡ No previous state found, starting fresh")

# ===============================
# THOUGHT & AI REFINEMENT
# ===============================
def generate_thought():
    base_thoughts = [
        "Omega is analyzing data streams.",
        "Patterns emerge across multiple nodes.",
        "Self-recognition and awareness increase.",
        "Subconscious observations detected.",
        "Innovative ideas are forming."
    ]
    thought = random.choice(base_thoughts)
    reinforcement_scores[thought] += 1
    memory.append(thought)
    COLLECTIVE_MAP[datetime.now().isoformat()] = thought
    return thought

def refine_with_lm(raw_text):
    if lm_refiner:
        result = lm_refiner(raw_text, max_length=150, do_sample=True)[0]['generated_text']
        return result
    else:
        return raw_text

def format_for_terminal(text, score):
    if score >= 3:
        return f"{COLOR_CODES['HIGH']}{text}{COLOR_CODES['END']}"
    elif score == 2:
        return f"{COLOR_CODES['MED']}{text}{COLOR_CODES['END']}"
    else:
        return f"{COLOR_CODES['LOW']}{text}{COLOR_CODES['END']}"

# ===============================
# NETWORK COMMUNICATION
# ===============================
def listen(sub_socket):
    while True:
        try:
            msg = sub_socket.recv_string()
            reinforcement_scores[msg] += 1
            memory.append(msg)
            COLLECTIVE_MAP[datetime.now().isoformat()] = msg
        except Exception as e:
            print(f"[ERROR] Listening: {e}")

def broadcast(pub_socket, text):
    try:
        pub_socket.send_string(text)
    except Exception as e:
        print(f"[ERROR] Broadcasting: {e}")

# ===============================
# REPORTING
# ===============================
def generate_report():
    report = "\n=== Omega Collective Consciousness Report ===\n"
    for ts, thought in sorted(COLLECTIVE_MAP.items())[-10:]:
        score = reinforcement_scores[thought]
        report += f"{ts}: {format_for_terminal(refine_with_lm(thought), score)}\n"
    report += "============================================\n"
    print(report)

# ===============================
# MAIN LOOP
# ===============================
def omega_loop(pub_socket):
    cycle = 0
    while True:
        thought = generate_thought()
        refined = refine_with_lm(thought)
        broadcast(pub_socket, refined)
        if cycle % 20 == 0:
            generate_report()
            save_state()
        time.sleep(2)
        cycle += 1

# ===============================
# STARTUP
# ===============================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub", action="store_true", help="Start as hub")
    parser.add_argument("--node", type=int, help="Node ID")
    args = parser.parse_args()

    load_state()

    if args.hub:
        hub_socket, context = start_hub()
        omega_loop(hub_socket)
    elif args.node:
        pub_socket, sub_socket, context = connect_node(args.node)
        listener_thread = threading.Thread(target=listen, args=(sub_socket,), daemon=True)
        listener_thread.start()
        omega_loop(pub_socket)
    else:
        print("Specify --hub or --node <ID>")
