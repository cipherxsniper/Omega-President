#!/usr/bin/env python3
import os
import subprocess
import time
import threading
import logging
import json
from datetime import datetime

# ==============================
# CONFIG
# ==============================
OMEGA_DIR = os.path.expanduser("~/Omega-President")
CLOUD_DIR = os.path.expanduser("~/Omega-Cloud/mini_omega_data")
NODE_COUNT = 30
BATCH_SIZE = 5
HEALTH_CHECK_INTERVAL = 10
UPDATE_INTERVAL = 1800
MAX_RESTARTS = 5

os.makedirs(CLOUD_DIR, exist_ok=True)

LOG_FILE = os.path.join(CLOUD_DIR, "mini_omega_cloud.jsonl")
logging.basicConfig(level=logging.INFO)

# ==============================
# UTILITIES
# ==============================

def log_event(event_type, node_id=None, message=""):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        "node": node_id,
        "message": message
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    logging.info(f"{event_type} | Node {node_id} | {message}")

def auto_update_repo():
    log_event("git_update_start")
    try:
        subprocess.run(["git", "-C", OMEGA_DIR, "stash", "--include-untracked"], check=True)
        subprocess.run(["git", "-C", OMEGA_DIR, "pull"], check=True)
        subprocess.run(["git", "-C", OMEGA_DIR, "stash", "pop"], check=False)
        log_event("git_update_complete")
    except Exception as e:
        log_event("git_update_failed", message=str(e))

def launch_node(node_id):
    script = os.path.join(OMEGA_DIR, f"omega_president_{node_id}.py")
    log_file = os.path.join(CLOUD_DIR, f"node_{node_id}.log")
    if not os.path.exists(script):
        log_event("node_missing", node_id, "Creating placeholder")
        with open(script, "w") as f:
            f.write(f"print('Node {node_id} placeholder running')\n")

    proc = subprocess.Popen(
        ["python3", "-u", script],
        stdout=open(log_file, "a"),
        stderr=subprocess.STDOUT
    )
    log_event("node_launched", node_id, f"PID {proc.pid}")
    return proc

def repair_node(node_id):
    log_event("node_repair_start", node_id)
    script = os.path.join(OMEGA_DIR, f"omega_president_{node_id}.py")
    try:
        subprocess.run(["python3", "-m", "py_compile", script], capture_output=True)
        proc = launch_node(node_id)
        log_event("node_repair_success", node_id, f"New PID {proc.pid}")
        return proc
    except Exception as e:
        log_event("node_repair_failed", node_id, str(e))
        return None

# ==============================
# ROTATING CLOUD LAUNCH
# ==============================

def rotate_nodes_forever():
    node_processes = {}
    crash_counts = {i: 0 for i in range(1, NODE_COUNT+1)}

    while True:
        # Auto-update Git before launching each batch
        auto_update_repo()

        for start in range(1, NODE_COUNT+1, BATCH_SIZE):
            end = min(start + BATCH_SIZE - 1, NODE_COUNT)
            log_event("batch_start", message=f"Batch {start}-{end} launching")

            for i in range(start, end+1):
                if i in node_processes:
                    if node_processes[i].poll() is not None:
                        log_event("node_crash_detected", i)
                        crash_counts[i] += 1
                        if crash_counts[i] <= MAX_RESTARTS:
                            node_processes[i] = repair_node(i)
                        else:
                            log_event("node_crash_limit", i)
                else:
                    node_processes[i] = launch_node(i)
                    time.sleep(0.5)  # stagger start

            # Health-check previous batch
            for i in range(max(1, start-BATCH_SIZE), start):
                if i in node_processes and node_processes[i].poll() is not None:
                    log_event("node_crash_detected", i)
                    crash_counts[i] += 1
                    if crash_counts[i] <= MAX_RESTARTS:
                        node_processes[i] = repair_node(i)
                    else:
                        log_event("node_crash_limit", i)

            time.sleep(HEALTH_CHECK_INTERVAL)

# ==============================
# AUTO UPDATE THREAD
# ==============================

def auto_update_forever():
    while True:
        auto_update_repo()
        time.sleep(UPDATE_INTERVAL)

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    log_event("launcher_start", message="Mini-Omega Cloud Launcher STARTED")
    threading.Thread(target=auto_update_forever, daemon=True).start()
    rotate_nodes_forever()
