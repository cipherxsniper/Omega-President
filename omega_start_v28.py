# omega_start_v28.py
import subprocess
import time
import os

# ==============================
# CONFIGURATION
# ==============================
NUM_NODES = 3  # Adjust number of nodes
BASE_PORT = 5560
NODE_SCRIPT = "omega_president_28_node.py"
LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

# ==============================
# SPAWN NODES
# ==============================
nodes = []
for i in range(NUM_NODES):
    pub_port = BASE_PORT + i
    sub_ports = [BASE_PORT + j for j in range(NUM_NODES) if j != i]

    log_file = os.path.join(LOG_DIR, f"node_{i+1}.log")
    cmd = [
        "python3", "-u", NODE_SCRIPT,
        "--node_name", f"omega_president_{i+1}",
        "--pub_port", str(pub_port),
        "--sub_ports", ",".join(map(str, sub_ports)),
        "--log_file", log_file
    ]
    print(f"Launching Node {i+1}: PUB {pub_port}, SUB {sub_ports}")
    p = subprocess.Popen(cmd)
    nodes.append(p)
    time.sleep(0.5)  # stagger startup

print("All nodes launched. Omega v28 network is live.")

# Keep orchestrator alive to monitor nodes
try:
    while True:
        time.sleep(5)
        for idx, p in enumerate(nodes):
            if p.poll() is not None:
                print(f"Node {idx+1} terminated unexpectedly!")
except KeyboardInterrupt:
    print("Shutting down Omega v28 network...")
    for p in nodes:
        p.terminate()
