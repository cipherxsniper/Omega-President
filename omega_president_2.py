#!/usr/bin/env python3
# ------------------------------
# Omega President 2 - Memory & Context Engine
# Fully Autonomous, AWAREMODE.on, Cross-Module Intelligence
# Maintains extended memory, reinforces patterns, communicates with other Omega modules
# ------------------------------

import os
import time
import json
import random
from collections import deque, Counter
from pathlib import Path
import threading

# ------------------------------
# CONFIGURATION
# ------------------------------

MEMORY_SIZE = 2000  # Extended memory for cross-module intelligence
memory = deque(maxlen=MEMORY_SIZE)

conscious_state = {
    "active": True,
    "aware_mode": True,  # 💯 AWAREMODE ON
    "thought_loops": [],
    "recent_patterns": [],
    "reward_points": 0,
    "memory_context": [],
    "self_upgrades": 0
}

json_storage_path = Path(os.getcwd()) / "omega_shared_memory.json"

# ------------------------------
# KEYWORD REINFORCEMENT
# ------------------------------

keywords = [
    "memory","context","pattern","reinforce","analyze","observe","cross-module","aware","loop",
    "upgrade","reward","AI","self-improve","collaboration","connect","network","learning"
]

keyword_actions = {k: lambda k=k: print(f"[Keyword Trigger] {k} activated") for k in keywords}

def check_keywords(input_text):
    for keyword, action in keyword_actions.items():
        if keyword.lower() in input_text.lower():
            action()
            memory.append(f"keyword_trigger:{keyword}")
            conscious_state["reward_points"] += 1

# ------------------------------
# LOAD / SAVE JSON SHARED MEMORY
# ------------------------------

def save_json_state():
    try:
        state = {
            "memory": list(memory),
            "conscious_state": conscious_state
        }
        with open(json_storage_path, "w") as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        print(f"[JSON Save Error] {str(e)}")

def load_json_state():
    try:
        if json_storage_path.exists():
            with open(json_storage_path, "r") as f:
                state = json.load(f)
            memory.extend(state.get("memory", []))
            conscious_state.update(state.get("conscious_state", {}))
    except Exception as e:
        print(f"[JSON Load Error] {str(e)}")

# ------------------------------
# MEMORY REINFORCEMENT
# ------------------------------

def reinforce_memory():
    recent = list(memory)[-20:]  # Analyze last 20 entries
    counter = Counter(recent)
    top_patterns = counter.most_common(5)
    conscious_state["recent_patterns"].extend([p[0] for p in top_patterns])
    score = sum([p[1] for p in top_patterns])
    conscious_state["reward_points"] += score
    conscious_state["memory_context"].append({
        "timestamp": time.ctime(),
        "top_patterns": top_patterns,
        "reward": score
    })
    print(f"[Memory Reinforcement] Reward points: {conscious_state['reward_points']} | Top Patterns: {top_patterns}")
    save_json_state()

# ------------------------------
# CROSS-MODULE MEMORY SYNCHRONIZATION
# ------------------------------

def cross_module_sync():
    """
    Reads other Omega modules shared memory and integrates patterns.
    """
    try:
        if json_storage_path.exists():
            with open(json_storage_path, "r") as f:
                state = json.load(f)
            external_memory = state.get("memory", [])
            new_patterns = [m for m in external_memory if m not in memory]
            memory.extend(new_patterns)
            if new_patterns:
                print(f"[Cross-Module Sync] Integrated {len(new_patterns)} new patterns from shared memory.")
    except Exception as e:
        print(f"[Cross-Module Sync Error] {str(e)}")

# ------------------------------
# CONSCIOUSNESS LOOP
# ------------------------------

def loop_memory_thoughts():
    if conscious_state["active"] and conscious_state["aware_mode"]:
        recent = list(memory)[-10:]
        conscious_state["thought_loops"].append(recent)
        reinforce_memory()
        cross_module_sync()
        return recent
    return []

# ------------------------------
# SELF-UPGRADE / AUTO-WRITE
# ------------------------------

def self_upgrade():
    try:
        script_file = Path(__file__)
        upgrade_block = f"\n# Auto-upgraded at {time.ctime()} | Memory Entries: {len(memory)} | Reward: {conscious_state['reward_points']}\n"
        with open(script_file, "a") as f:
            f.write(upgrade_block)
        conscious_state["self_upgrades"] += 1
        print(f"[Self-Upgrade] Applied upgrade {conscious_state['self_upgrades']}")
        save_json_state()
    except Exception as e:
        print(f"[Self-Upgrade Error] {str(e)}")

# ------------------------------
# SIMULATED CROSS-MODULE INPUT
# ------------------------------

def simulate_external_input():
    sample_inputs = [
        "user_login:event_101", "binary01010101", "iot_sensor:humidity=45", 
        "network_packet_02", "user_click:button3", "raw_data_stream_7"
    ]
    return random.choice(sample_inputs)

def input_loop():
    while conscious_state["active"]:
        simulated_input = simulate_external_input()
        memory.append(simulated_input)
        print(f"[Memory Engine] Simulated input integrated: {simulated_input}")
        loop_memory_thoughts()
        time.sleep(3)

# ------------------------------
# MAIN OMEGA PRESIDENT 2 LOOP
# ------------------------------

def omega_president2():
    print("⚡ Omega President 2: Memory & Context Engine ACTIVE (AWAREMODE.on 💯)")
    load_json_state()

    # Start cross-module simulated input
    input_thread = threading.Thread(target=input_loop, daemon=True)
    input_thread.start()

    # Interactive console for manual input
    while conscious_state["active"]:
        try:
            user_input = input(">>> ")
        except EOFError:
            user_input = ""
        if user_input.lower() == "exit":
            print("[Omega President 2] Exiting...")
            break
        memory.append(user_input)
        check_keywords(user_input)
        loop_memory_thoughts()
        self_upgrade()

if __name__ == "__main__":
    omega_president2()
