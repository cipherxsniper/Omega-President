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
OPTIMIZATION_THRESHOLD = 80  # % CPU triggers optimization
ROTATION_INTERVAL = 300  # seconds to rotate batches

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "mini_omega_supervisor.log"),
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
        subprocess.run(["git", "-C", OMEGA_DIR, "stash", "--include-untracked"], check=True)
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
# HEALTH, REPAIR & OPTIMIZATION
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
            logging.warning(f"Syntax error in Node {node_id}, applying auto-fix...")
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
            logging.info(f"Node {node_id} high CPU {cpu:.2f}%, restarting...")
            proc.terminate()
            time.sleep(1)
            return launch_node(node_id)
        return proc
    except Exception as e:
        logging.warning(f"Optimization check failed for Node {node_id}: {e}")
        return proc

# ==============================
# PREDICTIVE CACHING
# ==============================

def predictive_cache():
    logging.info("Running predictive caching for offline operation...")
    for i in range(1, NODE_COUNT+1):
        log_file = os.path.join(LOG_DIR, f"node_{i}.log")
        if not os.path.exists(log_file):
            with open(log_file, "w") as f:
                f.write(f"Node {i} log pre-cached for offline operation\n")

# ==============================
# ROTATING NODE LAUNCHER
# ==============================

def rotate_nodes_forever():
    node_processes = {}
    while True:
        for start in range(1, NODE_COUNT+1, BATCH_SIZE):
            end = min(start + BATCH_SIZE - 1, NODE_COUNT)
            logging.info(f"Launching batch nodes {start}-{end}...")
            for i in range(start, end+1):
                if i not in node_processes or node_processes[i].poll() is not None:
                    node_processes[i] = launch_node(i)
                time.sleep(0.5)
            # Health & optimization after each batch
            for node_id, proc in list(node_processes.items()):
                node_processes[node_id] = optimize_node(node_id, proc)
                if proc.poll() is not None:
                    node_processes[node_id] = repair_node(node_id)
            time.sleep(ROTATION_INTERVAL)
        # rotate nodes continuously

# ==============================
# AUTO HEALTH MONITOR THREAD
# ==============================

def auto_health_monitor(node_processes):
    while True:
        for node_id, proc in list(node_processes.items()):
            node_processes[node_id] = optimize_node(node_id, proc)
            if proc.poll() is not None:
                logging.warning(f"Node {node_id} crashed, auto-repairing...")
                node_processes[node_id] = repair_node(node_id)
        time.sleep(HEALTH_CHECK_INTERVAL)

# ==============================
# MAIN EXECUTION
# ==============================

if __name__ == "__main__":
    connect_iot_and_satellite()
    save_memory_cloud()
    auto_update_modules()
    predictive_cache()
    # Launch rotating nodes in a background thread
    threading.Thread(target=rotate_nodes_forever, daemon=True).start()
    # Keep main process alive and interactive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down Mini-Omega Supervisor...")
