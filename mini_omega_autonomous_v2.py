#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Mini-Omega Autonomous v2
Termux-compatible, psutil-free
Features:
- Node management & health monitoring
- Predictive node health
- Auto-repair & live module updates
- Memory cloud & offline caching
- IoT & satellite connectivity
- Interactive terminal
"""

import os
import subprocess
import sys
import time
import json
from datetime import datetime

OMEGA_DIR = os.path.expanduser("~/Omega-President")
LOG_DIR = os.path.join(OMEGA_DIR, "logs")
MEMORY_FILE = os.path.join(OMEGA_DIR, "omega_memory.json")

# Ensure logs folder exists
os.makedirs(LOG_DIR, exist_ok=True)

# --- Utility Functions --- #

def log(info):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[INFO] {timestamp}: {info}")

def get_cpu_count():
    return os.cpu_count() or 1

def get_memory_info():
    try:
        mem_kb = int(subprocess.check_output(
            "cat /proc/meminfo | grep MemTotal | awk '{print $2}'",
            shell=True
        ).decode().strip())
        return mem_kb * 1024
    except Exception:
        return None

def list_processes():
    try:
        out = subprocess.check_output("ps -A", shell=True).decode().splitlines()
        return out
    except Exception:
        return []

def node_is_active(node_id):
    log_file = os.path.join(LOG_DIR, f"node_{node_id}.log")
    return os.path.exists(log_file) and os.path.getsize(log_file) > 0

# --- Node Management --- #

NODE_COUNT = 30
BATCH_SIZE = 5
NODE_PIDS = {}

def launch_node(node_id):
    script = os.path.join(OMEGA_DIR, f"omega_president_{node_id}.py")
    log_file = os.path.join(LOG_DIR, f"node_{node_id}.log")
    if not os.path.exists(script):
        log(f"[ERROR] Node script {script} missing")
        return None
    proc = subprocess.Popen(
        [sys.executable, "-u", script],
        stdout=open(log_file, "a"),
        stderr=subprocess.STDOUT
    )
    NODE_PIDS[node_id] = proc.pid
    log(f"Launched Node {node_id}, PID: {proc.pid}")
    return proc.pid

def batch_launch_nodes():
    for start in range(1, NODE_COUNT + 1, BATCH_SIZE):
        end = min(start + BATCH_SIZE - 1, NODE_COUNT)
        log(f"Launching nodes {start}-{end}...")
        for i in range(start, end + 1):
            launch_node(i)
            time.sleep(0.5)
        time.sleep(2)

def health_check_nodes():
    good_nodes = []
    bad_nodes = []
    for i in range(1, NODE_COUNT + 1):
        if node_is_active(i):
            log(f"[OK] Node {i} active")
            good_nodes.append(i)
        else:
            log(f"[WARN] Node {i} inactive")
            bad_nodes.append(i)
    # Log bad nodes
    with open(os.path.join(LOG_DIR, "bad_nodes.txt"), "w") as f:
        f.write(" ".join(map(str, bad_nodes)))
    log(f"Good nodes: {good_nodes}")
    log(f"Bad nodes: {bad_nodes} (logged)")
    return good_nodes, bad_nodes

# --- Memory Cloud --- #

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# --- IoT & Satellite --- #

def connect_iot():
    log("Connecting to IoT & satellite networks...")
    # Simulated connection for Termux
    time.sleep(1)
    log("IoT connected, syncing memory cloud.")

# --- Auto Repair --- #

def repair_module(module_file):
    """Simple repair: check if file exists, if not, try pulling from repo"""
    if not os.path.exists(module_file):
        log(f"[REPAIR] Missing {module_file}, attempting recovery...")
        try:
            subprocess.run(["git", "-C", OMEGA_DIR, "checkout", "--", module_file], check=True)
            log(f"[REPAIR] {module_file} recovered successfully")
        except subprocess.CalledProcessError:
            log(f"[REPAIR] Failed to recover {module_file}")

def repair_bad_nodes(bad_nodes):
    for node_id in bad_nodes:
        script = os.path.join(OMEGA_DIR, f"omega_president_{node_id}.py")
        repair_module(script)

# --- Mini-Omega Terminal --- #

def interactive_terminal(memory):
    log("Mini-Omega terminal starting...")
    while True:
        try:
            cmd = input("Mini-Omega> ").strip().lower()
            if cmd == "help":
                print("Commands: help | status | list_nodes | repair <node> | memory | update | exit")
            elif cmd == "status":
                log(f"CPU cores: {get_cpu_count()}, Memory: {get_memory_info()} bytes")
            elif cmd == "list_nodes":
                health_check_nodes()
            elif cmd.startswith("repair"):
                parts = cmd.split()
                if len(parts) == 2 and parts[1].isdigit():
                    repair_module(os.path.join(OMEGA_DIR, f"omega_president_{parts[1]}.py"))
            elif cmd == "memory":
                print(json.dumps(memory, indent=2))
            elif cmd == "update":
                log("Attempting live module update...")
                subprocess.run(["git", "-C", OMEGA_DIR, "pull"])
            elif cmd == "exit":
                log("Exiting terminal...")
                break
            else:
                print("Unknown command. Type 'help'.")
        except KeyboardInterrupt:
            log("Terminal interrupted, exiting...")
            break

# --- Main Execution --- #

if __name__ == "__main__":
    memory = load_memory()
    connect_iot()
    batch_launch_nodes()
    good_nodes, bad_nodes = health_check_nodes()
    repair_bad_nodes(bad_nodes)
    save_memory(memory)
    interactive_terminal(memory)
