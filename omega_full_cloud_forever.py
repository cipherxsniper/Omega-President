#!/usr/bin/env python3
import os
import subprocess
import time
import threading
import logging
from datetime import datetime, timezone

# ==============================
# CONFIG
# ==============================
OMEGA_DIR = os.path.expanduser("~/Omega-President")
LOG_DIR = os.path.join(OMEGA_DIR, "logs")
NODE_COUNT = 30
HEALTH_CHECK_INTERVAL = 10    # seconds
UPDATE_INTERVAL = 3600        # seconds (auto-update Git every hour)

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "omega_cloud_forever.log"),
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s: %(message)s'
)

# ==============================
# GIT AUTO-UPDATE
# ==============================
def safe_git_update():
    try:
        lock_file = os.path.join(OMEGA_DIR, ".git/index.lock")
        if os.path.exists(lock_file):
            os.remove(lock_file)
            logging.warning("Removed stale git index.lock")
        subprocess.run(["git", "-C", OMEGA_DIR, "stash", "--include-untracked"], check=True)
        subprocess.run(["git", "-C", OMEGA_DIR, "pull"], check=True)
        subprocess.run(["git", "-C", OMEGA_DIR, "stash", "pop"], check=False)
        logging.info("Git update successful")
    except Exception as e:
        logging.warning(f"Git update failed: {e}")

def auto_update_loop():
    while True:
        safe_git_update()
        time.sleep(UPDATE_INTERVAL)

# ==============================
# NODE MANAGEMENT
# ==============================
def launch_node(node_id):
    script = os.path.join(OMEGA_DIR, f"omega_president_{node_id}.py")
    log_file = os.path.join(LOG_DIR, f"node_{node_id}.log")
    if not os.path.exists(script):
        logging.warning(f"Node {node_id} missing, creating placeholder.")
        with open(script, "w") as f:
            f.write(f"print('Node {node_id} placeholder running')\n")
    proc = subprocess.Popen(
        ["python3", "-u", script],
        stdout=open(log_file, "a"),
        stderr=subprocess.STDOUT
    )
    logging.info(f"Launched Node {node_id}, PID {proc.pid}")
    return proc

def repair_node(node_id):
    logging.info(f"Repairing Node {node_id}...")
    script = os.path.join(OMEGA_DIR, f"omega_president_{node_id}.py")
    try:
        subprocess.run(["python3", "-m", "py_compile", script], capture_output=True)
        return launch_node(node_id)
    except Exception as e:
        logging.error(f"Repair failed for Node {node_id}: {e}")

# ==============================
# FOREVER NODE ROTATION
# ==============================
def launch_all_nodes_forever():
    node_processes = {}
    while True:
        for i in range(1, NODE_COUNT + 1):
            if i in node_processes:
                if node_processes[i].poll() is not None:  # crashed
                    logging.warning(f"Node {i} crashed, repairing...")
                    node_processes[i] = repair_node(i)
            else:
                node_processes[i] = launch_node(i)
            time.sleep(0.2)
        logging.info(f"All {NODE_COUNT} nodes launched. Health check sleeping {HEALTH_CHECK_INTERVAL}s...")
        time.sleep(HEALTH_CHECK_INTERVAL)

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    logging.info("=== Omega Cloud Full Forever Launcher STARTED ===")
    threading.Thread(target=auto_update_loop, daemon=True).start()
    launch_all_nodes_forever()
