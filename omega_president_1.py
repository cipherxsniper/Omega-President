#!/usr/bin/env python3
# ------------------------------
# Omega President 1 - Observer & Pattern Collector
# Fully Autonomous, AWAREMODE.on, Story-Driven
# Scans IoT/Web, Converts Raw Data, Shares Memory
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

MEMORY_SIZE = 1000  # Extended memory for advanced pattern observation
memory = deque(maxlen=MEMORY_SIZE)

conscious_state = {
    "active": True,
    "aware_mode": True,          # 💯 AWAREMODE ON
    "thought_loops": [],
    "recent_patterns": [],
    "reward_points": 0,
    "observations": [],
    "self_upgrades": 0
}

json_storage_path = Path(os.getcwd()) / "omega_shared_memory.json"

# ------------------------------
# DYNAMIC KEYWORDS
# ------------------------------

keywords = [
    "Zeus","Athena","Thor","wink wink","thought","100","consciousness","memory loop",
    "upgrade","pattern","decision","reward","convert","iot","auto","yes","backend",
    "syntax mode","self","open","ai","engagement","interactive intelligence","evolve",
    "observe","loop","recursive","meta","quantum","pattern recognition","reinforce",
    "self-improve","collaboration","connect","network","debug","analyze","upgrade memory",
    "multi-agent","autonomous","cognitive","override","execute","run","trigger","response",
    "activate","learning","adapt","simulate","predict","decision-making","feedback",
    "reward system","entropy","stochastic","symbolic","dynamic","automation","self-correct",
    "optimization","AI loop","conscious loop","thought experiment","pattern evolution"
]

keyword_actions = {k: lambda k=k: print(f"[Keyword Trigger] {k} activated") for k in keywords}

def check_keywords(input_text):
    for keyword, action in keyword_actions.items():
        if keyword.lower() in input_text.lower():
            action()
            memory.append(f"keyword_trigger:{keyword}")
            conscious_state["reward_points"] += 1

# ------------------------------
# RAW DATA CONVERSION
# ------------------------------

def convert_raw_to_text(raw_input):
    """
    Converts binary/binary-like strings (0s,1s, letters, numbers) to readable text.
    If already readable, returns as is.
    """
    try:
        raw_input = raw_input.strip()
        if all(c in "01" for c in raw_input) and len(raw_input) > 0:
            n = int(raw_input, 2)
            text = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8', errors='ignore')
            return text
        return raw_input
    except Exception as e:
        return f"[Conversion Error] {str(e)}"

# ------------------------------
# MEMORY & OBSERVATION LOGGING
# ------------------------------

def reinforce_memory(memory):
    """
    Reinforce recent observations, calculate pattern score, add reward points.
    """
    recent = list(memory)[-10:]
    pattern_score = len(set(recent))
    conscious_state["reward_points"] += pattern_score
    conscious_state["recent_patterns"].extend(recent)
    print(f"[Memory Reinforcement] Reward points: {conscious_state['reward_points']} | Observations: {recent}")
    save_json_state()

def save_json_state():
    """
    Save shared memory and conscious state to JSON for cross-module communication.
    """
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
    """
    Load shared memory and conscious state from JSON.
    """
    try:
        if json_storage_path.exists():
            with open(json_storage_path, "r") as f:
                state = json.load(f)
            memory.extend(state.get("memory", []))
            conscious_state.update(state.get("conscious_state", {}))
    except Exception as e:
        print(f"[JSON Load Error] {str(e)}")

# ------------------------------
# CONSCIOUSNESS LOOP
# ------------------------------

def loop_original_thoughts(memory):
    """
    Maintains thought loops for self-awareness and pattern recognition.
    """
    if conscious_state["active"] and conscious_state["aware_mode"]:
        recent = list(memory)[-10:]
        conscious_state["thought_loops"].append(recent)
        conscious_state["observations"].append({
            "timestamp": time.ctime(),
            "recent": recent
        })
        print(f"[Consciousness Loop] Observing patterns: {recent}")
        reinforce_memory(memory)
        return recent
    return []

# ------------------------------
# SIMULATED IOT & WEB INPUT
# ------------------------------

def generate_iot_input():
    """
    Simulates IoT/device/web input for observation.
    """
    sample_inputs = [
        "01101000", "sensor:temperature=72", "binary101010", "network_packet_001",
        "user_action:click", "01010101", "iot_device:light=on", "raw_data_stream_1"
    ]
    return random.choice(sample_inputs)

def observe_iot_loop():
    """
    Continuous loop to gather and process IoT/web input.
    """
    while conscious_state["active"]:
        raw_input = generate_iot_input()
        converted = convert_raw_to_text(raw_input)
        memory.append(converted)
        print(f"[Observer] Raw input: {raw_input} | Converted: {converted}")
        loop_original_thoughts(memory)
        time.sleep(2)  # Adjustable scan interval

# ------------------------------
# SELF-UPGRADE / AUTO WRITE
# ------------------------------

def self_upgrade():
    """
    Writes self-improvements and observations to the script for self-evolution.
    """
    try:
        script_file = Path(__file__)
        upgrade_block = f"\n# Auto-upgraded at {time.ctime()} | Observations: {len(memory)} | Reward: {conscious_state['reward_points']}\n"
        with open(script_file, "a") as f:
            f.write(upgrade_block)
        conscious_state["self_upgrades"] += 1
        print(f"[Self-Upgrade] Applied upgrade {conscious_state['self_upgrades']}")
        save_json_state()
    except Exception as e:
        print(f"[Self-Upgrade Error] {str(e)}")

# ------------------------------
# MAIN OMEGA PRESIDENT 1 LOOP
# ------------------------------

def omega_president1():
    """
    Launches Observer mode with all features active.
    """
    print("⚡ Omega President 1: Observer Mode ACTIVE (AWAREMODE.on 💯)")
    load_json_state()

    # Start IoT/Web observation in a separate thread
    observer_thread = threading.Thread(target=observe_iot_loop, daemon=True)
    observer_thread.start()

    # Interactive console for manual input
    while conscious_state["active"]:
        try:
            user_input = input(">>> ")
        except EOFError:
            user_input = ""
        if user_input.lower() == "exit":
            print("[Omega President 1] Exiting...")
            break
        converted = convert_raw_to_text(user_input)
        memory.append(converted)
        print(f"[Omega Conversion] {converted}")
        check_keywords(user_input)
        loop_original_thoughts(memory)
        self_upgrade()

if __name__ == "__main__":
    omega_president1()
