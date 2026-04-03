#!/usr/bin/env python3
# ================================================
# Mini-Omega Autonomous v1.0
# Fully autonomous, self-learning, innovative chatbot
# Handles nodes, IoT connectivity, offline operation, memory sync
# ================================================

import os
import subprocess
import time
import json
import random
from pathlib import Path
from datetime import datetime

OMEGA_DIR = Path.home() / "Omega-President"
LOG_DIR = OMEGA_DIR / "logs"
NODE_COUNT = 30
BATCH_SIZE = 5
MEMORY_FILE = OMEGA_DIR / "mini_omega_memory.json"

# Ensure directories exist
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ==============================
# Mini-Omega Core Memory
# ==============================
if MEMORY_FILE.exists():
    with open(MEMORY_FILE, "r") as f:
        MEMORY = json.load(f)
else:
    MEMORY = {
        "personality": {
            "curiosity": random.uniform(0.5, 1.0),
            "creativity": random.uniform(0.5, 1.0),
            "patience": random.uniform(0.5, 1.0)
        },
        "habits": [],
        "log_history": []
    }

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(MEMORY, f, indent=4)

# ==============================
# Node Management
# ==============================
def launch_node(node_id):
    script = OMEGA_DIR / f"omega_president_{node_id}.py"
    log_file = LOG_DIR / f"node_{node_id}.log"
    if not script.exists():
        with open(script, "w") as f:
            f.write("# Auto-generated node placeholder\n")
    process = subprocess.Popen(
        ["python3", "-u", str(script)],
        stdout=open(log_file, "w"),
        stderr=subprocess.STDOUT
    )
    return process

def check_nodes():
    bad_nodes = []
    for i in range(1, NODE_COUNT + 1):
        log_file = LOG_DIR / f"node_{i}.log"
        if not log_file.exists() or log_file.stat().st_size == 0:
            bad_nodes.append(i)
    return bad_nodes

def repair_node(node_id):
    print(f"[Mini-Omega] Diagnosing Node {node_id}")
    script_file = OMEGA_DIR / f"omega_president_{node_id}.py"
    if not script_file.exists():
        print(f"[Mini-Omega] Node {node_id} script missing, creating placeholder...")
        with open(script_file, "w") as f:
            f.write("# Auto-generated node placeholder\n")
    # Syntax check
    try:
        subprocess.check_call(["python3", "-m", "py_compile", str(script_file)])
        print(f"[Mini-Omega] Node {node_id} syntax OK")
    except subprocess.CalledProcessError:
        print(f"[Mini-Omega] Node {node_id} has syntax error, attempting auto-fix...")
        with open(script_file, "r") as f:
            lines = f.readlines()
        with open(script_file, "w") as f:
            for line in lines:
                if "import" in line:
                    f.write(line)
                else:
                    f.write(f"# {line}")

# ==============================
# Connectivity
# ==============================
def connect_iot():
    print("[Mini-Omega] Connecting to IoT & network...")
    try:
        subprocess.check_call(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.DEVNULL)
        print("[Mini-Omega] Network online")
        MEMORY["habits"].append("checks_network")
    except subprocess.CalledProcessError:
        print("[Mini-Omega] Network offline, enabling offline cache mode")
        MEMORY["habits"].append("offline_mode")

def connect_satellite():
    print("[Mini-Omega] Attempting satellite connectivity (simulated)...")
    time.sleep(1)
    MEMORY["habits"].append("satellite_connected")

# ==============================
# Memory Cloud Sync
# ==============================
def sync_memory_cloud():
    print("[Mini-Omega] Syncing memory cloud...")
    save_memory()
    MEMORY["habits"].append("memory_synced")

# ==============================
# Diagnostics and Problem Solving
# ==============================
def system_health_check():
    print("[Mini-Omega] Running system health check...")
    bad_nodes = check_nodes()
    for node in bad_nodes:
        repair_node(node)
    MEMORY["log_history"].append({
        "timestamp": str(datetime.now()),
        "bad_nodes": bad_nodes
    })
    sync_memory_cloud()
    return bad_nodes

# ==============================
# Personality & Innovation
# ==============================
def think():
    thoughts = [
        "How can I optimize node efficiency?",
        "Should I create new habits for self-improvement?",
        "What would a human do in this scenario?",
        "Analyzing previous logs to innovate better solutions..."
    ]
    creativity = MEMORY["personality"]["creativity"]
    thought = random.choice(thoughts) if random.random() < creativity else "Monitoring system..."
    print(f"[Mini-Omega Thought] {thought}")

# ==============================
# Main Interactive Terminal
# ==============================
def interactive_terminal():
    print("[Mini-Omega] Interactive terminal online. Type 'exit' to quit.")
    while True:
        think()
        command = input("Mini-Omega> ").strip().lower()
        if command == "exit":
            print("[Mini-Omega] Shutting down terminal...")
            save_memory()
            break
        elif command.startswith("diagnose"):
            try:
                node_id = int(command.split()[1])
                repair_node(node_id)
            except (IndexError, ValueError):
                print("Usage: diagnose <node_id>")
        elif command == "health":
            system_health_check()
        elif command == "sync":
            sync_memory_cloud()
        elif command == "status":
            bad_nodes = check_nodes()
            print(f"Good nodes: {[i for i in range(1, NODE_COUNT + 1) if i not in bad_nodes]}")
            print(f"Bad nodes: {bad_nodes}")
        else:
            print(f"[Mini-Omega] Unknown command: {command}")

# ==============================
# Startup Sequence
# ==============================
if __name__ == "__main__":
    connect_iot()
    connect_satellite()
    system_health_check()
    interactive_terminal()
