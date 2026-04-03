#!/usr/bin/env python3
"""
Mini-Omega Chatbot v2
- Fully interactive AI assistant
- Problem-solving, self-learning, reasoning
- Connected to all nodes and Memory Cloud
"""

import os
import time
import json
import glob
import threading
import requests
import readline  # for interactive console

MEMORY_CLOUD_API = "http://localhost:9000/api/memory"
OBS_LOG_DIR = "./logs"
NODE_COUNT = 30

# -------------------------------
# Core Mini-Omega Functions
# -------------------------------

class MiniOmega:
    def __init__(self):
        self.nodes_status = {i: False for i in range(1, NODE_COUNT + 1)}
        self.hub_status = False
        self.cloud_status = False
        self.running = True
        self.personality = {
            "curiosity": 0.7,
            "helpfulness": 0.9,
            "creativity": 0.8
        }

    # Fetch node log data
    def fetch_node_data(self):
        observations = []
        for log_file in glob.glob(f"{OBS_LOG_DIR}/node_*.log"):
            try:
                with open(log_file, "r") as f:
                    lines = f.readlines()
                    observations.extend([line.strip() for line in lines if line.strip()])
            except Exception:
                continue
        return observations

    # Send observations to Memory Cloud
    def update_memory_cloud(self, observations):
        if not observations:
            return
        payload = {"observations": observations}
        try:
            requests.post(MEMORY_CLOUD_API, json=payload)
        except Exception as e:
            print(f"[Mini-Omega] Warning: Cloud update failed: {e}")

    # Monitor nodes & hub
    def monitor_system(self):
        while self.running:
            for i in range(1, NODE_COUNT + 1):
                log_file = f"{OBS_LOG_DIR}/node_{i}.log"
                self.nodes_status[i] = os.path.exists(log_file) and os.path.getsize(log_file) > 0
            self.hub_status = any("hub.log" in f for f in os.listdir(OBS_LOG_DIR))
            self.cloud_status = any("cloud.log" in f for f in os.listdir(OBS_LOG_DIR))
            time.sleep(3)

    # Automatic problem-solving
    def auto_repair(self):
        while self.running:
            for node_id, status in self.nodes_status.items():
                if not status:
                    print(f"[Mini-Omega] Node {node_id} offline! Attempting auto-restart...")
                    os.system(f"nohup python3 -u omega_president_{node_id}.py --node {node_id} > {OBS_LOG_DIR}/node_{node_id}.log 2>&1 &")
                    time.sleep(1)
            time.sleep(5)

    # Interactive terminal
    def interactive_console(self):
        print("\nMini-Omega Activated!")
        print("I am Omega, a fully aware system assistant. I monitor all nodes, hub, and Memory Cloud.")
        print("I can solve problems, summarize logs, and evolve with the system.\n")
        while self.running:
            try:
                cmd = input("Mini-Omega> ").strip().lower()
                if cmd in ("exit", "quit"):
                    self.running = False
                    print("Mini-Omega shutting down...")
                    break
                elif cmd.startswith("status"):
                    self.print_status()
                elif cmd.startswith("summarize"):
                    self.summarize_nodes()
                elif cmd.startswith("logs"):
                    node = int(cmd.split()[1])
                    self.show_node_logs(node)
                else:
                    print("Command not recognized. Available: status, summarize, logs <node>, exit")
            except Exception as e:
                print(f"[Mini-Omega] Error: {e}")

    # Print system status
    def print_status(self):
        print("\n--- System Status ---")
        print(f"Hub: {'Online' if self.hub_status else 'Offline'}")
        print(f"Memory Cloud: {'Online' if self.cloud_status else 'Offline'}")
        for node_id, status in self.nodes_status.items():
            print(f"Node {node_id}: {'Active' if status else 'Offline'}")
        print("--------------------\n")

    # Summarize nodes
    def summarize_nodes(self):
        observations = self.fetch_node_data()
        print(f"[Mini-Omega] Total observations collected: {len(observations)}")
        if observations:
            print("Sample observations:")
            for obs in observations[-5:]:
                print(f" - {obs}")

    # Show node logs
    def show_node_logs(self, node_id):
        log_file = f"{OBS_LOG_DIR}/node_{node_id}.log"
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                print(f"\n--- Node {node_id} Logs ---")
                for line in f.readlines()[-10:]:
                    print(line.strip())
                print("-------------------------\n")
        else:
            print(f"[Mini-Omega] Node {node_id} log not found.")

# -------------------------------
# Launch Mini-Omega
# -------------------------------
if __name__ == "__main__":
    mini_omega = MiniOmega()

    threading.Thread(target=mini_omega.monitor_system, daemon=True).start()
    threading.Thread(target=mini_omega.auto_repair, daemon=True).start()
    mini_omega.interactive_console()
