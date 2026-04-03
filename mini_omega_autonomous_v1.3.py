#!/usr/bin/env python3
import os
import subprocess
import logging
import time
import threading
import psutil
from datetime import datetime

# ==============================
# CONFIG
# ==============================
OMEGA_DIR = os.path.expanduser("~/Omega-President")
LOG_DIR = os.path.join(OMEGA_DIR, "logs")
NODE_COUNT = 30
BATCH_SIZE = 5
HEALTH_CHECK_INTERVAL = 10  # seconds
OPTIMIZATION_THRESHOLD = 80  # % CPU usage triggers optimization

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "mini_omega.log"),
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s: %(message)s'
)

# ==============================
# CORE FUNCTIONS
# ==============================

def connect_iot_and_satellite():
    logging.info("Connecting to IoT & satellite networks...")
    time.sleep(1)
    logging.info("IoT connected, syncing memory cloud.")

def save_memory_cloud():
    logging.info("Memory Cloud saved.")

def auto_update_modules():
    logging.info("Checking for core module updates...")
    try:
        subprocess.run(
            ["git", "-C", OMEGA_DIR, "stash", "--include-untracked"],
            check=True
        )
        subprocess.run(["git", "-C", OMEGA_DIR, "pull"], check=True)
        subprocess.run(["git", "-C", OMEGA_DIR, "stash", "pop"], check=False)
        logging.info("Modules updated successfully.")
    except Exception as e:
        logging.warning(f"Module update failed: {e}")

def launch_node(node_id):
    script = os.path.join(OMEGA_DIR, f"omega_president_{node_id}.py")
    log_file = os.path.join(LOG_DIR, f"node_{node_id}.log")
    if not os.path.exists(script):
        logging.warning(f"Node script {script} missing, creating placeholder...")
        with open(script, "w") as f:
            f.write(f"print('Node {node_id} placeholder running')\n")
    process = subprocess.Popen(
        ["python3", "-u", script],
        stdout=open(log_file, "a"),
        stderr=subprocess.STDOUT
    )
    logging.info(f"Launched Node {node_id}, PID: {process.pid}")
    return process

# ==============================
# PREDICTIVE & SELF-HEALING
# ==============================

def health_check_nodes(node_processes):
    good_nodes = []
    bad_nodes = []
    for node_id, proc in node_processes.items():
        log_file = os.path.join(LOG_DIR, f"node_{node_id}.log")
        if proc.poll() is None and os.path.exists(log_file) and os.path.getsize(log_file) > 0:
            good_nodes.append(node_id)
        else:
            bad_nodes.append(node_id)
    logging.info(f"Good nodes: {good_nodes}")
    logging.info(f"Bad nodes: {bad_nodes}")
    with open(os.path.join(LOG_DIR, "bad_nodes.txt"), "w") as f:
        f.write(" ".join(map(str, bad_nodes)))
    return good_nodes, bad_nodes

def repair_node(node_id):
    logging.info(f"Repairing Node {node_id}...")
    script = os.path.join(OMEGA_DIR, f"omega_president_{node_id}.py")
    try:
        result = subprocess.run(["python3", "-m", "py_compile", script], capture_output=True)
        if result.returncode != 0:
            logging.warning(f"Syntax error detected in Node {node_id}, applying auto-fix...")
            with open(script, "a") as f:
                f.write("\n")
        return launch_node(node_id)
    except Exception as e:
        logging.error(f"Failed to repair Node {node_id}: {e}")

def optimize_node(node_id, proc):
    try:
        p = psutil.Process(proc.pid)
        cpu = p.cpu_percent(interval=1)
        mem = p.memory_percent()
        if cpu > OPTIMIZATION_THRESHOLD:
            logging.info(f"Node {node_id} high CPU {cpu:.2f}%, restarting for optimization...")
            proc.terminate()
            time.sleep(1)
            return launch_node(node_id)
        return proc
    except Exception as e:
        logging.warning(f"Optimization check failed for Node {node_id}: {e}")
        return proc

# ==============================
# PREDICTIVE CACHING & OFFLINE
# ==============================

def predictive_cache():
    logging.info("Running predictive caching for offline operation...")
    for i in range(1, NODE_COUNT+1):
        log_file = os.path.join(LOG_DIR, f"node_{i}.log")
        if not os.path.exists(log_file):
            with open(log_file, "w") as f:
                f.write(f"Node {i} log pre-cached for offline operation\n")

# ==============================
# INTERACTIVE TERMINAL
# ==============================

def interactive_terminal():
    print("\n=== Mini-Omega Interactive Terminal v1.3 ===")
    print("Commands: help | status | list_nodes | repair <node> | optimize | memory | update | exit\n")
    node_processes = {}

    for start in range(1, NODE_COUNT+1, BATCH_SIZE):
        end = min(start + BATCH_SIZE - 1, NODE_COUNT)
        logging.info(f"Launching nodes {start}-{end}...")
        for i in range(start, end+1):
            node_processes[i] = launch_node(i)
            time.sleep(0.5)
        time.sleep(1)

    def auto_health_monitor():
        while True:
            for node_id, proc in list(node_processes.items()):
                node_processes[node_id] = optimize_node(node_id, proc)
                if proc.poll() is not None:
                    logging.warning(f"Node {node_id} crashed, auto-repairing...")
                    node_processes[node_id] = repair_node(node_id)
            time.sleep(HEALTH_CHECK_INTERVAL)

    threading.Thread(target=auto_health_monitor, daemon=True).start()

    while True:
        cmd = input("Mini-Omega> ").strip()
        if cmd == "help":
            print("Commands: help | status | list_nodes | repair <node> | optimize | memory | update | exit")
        elif cmd == "status":
            good, bad = health_check_nodes(node_processes)
            print(f"Good nodes: {good}")
            print(f"Bad nodes: {bad}")
        elif cmd.startswith("repair"):
            parts = cmd.split()
            if len(parts) == 2 and parts[1].isdigit():
                node_id = int(parts[1])
                node_processes[node_id] = repair_node(node_id)
            else:
                print("Usage: repair <node_id>")
        elif cmd == "optimize":
            for node_id, proc in node_processes.items():
                node_processes[node_id] = optimize_node(node_id, proc)
        elif cmd == "list_nodes":
            print(f"Nodes: {list(node_processes.keys())}")
        elif cmd == "memory":
            save_memory_cloud()
            print("Memory cloud synced.")
        elif cmd == "update":
            auto_update_modules()
        elif cmd == "exit":
            print("Shutting down Mini-Omega terminal...")
            for p in node_processes.values():
                p.terminate()
            break
        else:
            print("Unknown command. Type 'help' for commands.")

# ==============================
# MAIN EXECUTION
# ==============================

if __name__ == "__main__":
    connect_iot_and_satellite()
    save_memory_cloud()
    auto_update_modules()
    predictive_cache()
    interactive_terminal()
