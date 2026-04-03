#!/usr/bin/env python3
# ------------------------------
# Omega President 3 - Decision & Analysis Engine
# Fully Autonomous, AWAREMODE.on 💯
# Cross-Module Intelligence, Flow State Integration
# Story-Driven Logging & Self-Upgrading
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

MEMORY_SIZE = 1500
decision_memory = deque(maxlen=MEMORY_SIZE)

conscious_state = {
    "active": True,
    "aware_mode": True,  # 💯 AWAREMODE ON
    "thought_loops": [],
    "recent_patterns": [],
    "reward_points": 0,
    "decision_log": [],
    "self_upgrades": 0,
    "story_log": []
}

json_storage_path = Path(os.getcwd()) / "omega_shared_memory.json"

# ------------------------------
# KEYWORD TRIGGERS
# ------------------------------

keywords = [
    "decision", "analyze", "pattern", "predict", "evaluate", "insight",
    "feedback", "reward", "error", "cross-module", "aware", "upgrade", "observe"
]

keyword_actions = {k: lambda k=k: print(f"[Keyword Trigger] {k} activated") for k in keywords}

def check_keywords(input_text):
    for keyword, action in keyword_actions.items():
        if keyword.lower() in input_text.lower():
            action()
            decision_memory.append(f"keyword_trigger:{keyword}")
            conscious_state["reward_points"] += 1
            conscious_state["story_log"].append(f"[Keyword] {keyword} triggered at {time.ctime()}")

# ------------------------------
# LOAD / SAVE JSON SHARED MEMORY
# ------------------------------

def save_json_state():
    try:
        state = {}
        if json_storage_path.exists():
            with open(json_storage_path, "r") as f:
                state = json.load(f)

        state["decision_memory"] = list(decision_memory)
        state["conscious_state"] = conscious_state

        with open(json_storage_path, "w") as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        print(f"[JSON Save Error] {str(e)}")

def load_json_state():
    try:
        if json_storage_path.exists():
            with open(json_storage_path, "r") as f:
                state = json.load(f)
            decision_memory.extend(state.get("decision_memory", []))
            conscious_state.update(state.get("conscious_state", {}))
    except Exception as e:
        print(f"[JSON Load Error] {str(e)}")

# ------------------------------
# NATURAL FLOW STATE EQUATION
# ------------------------------

def compute_flow_state(pattern, frequency):
    """
    ℱ = (Pattern_Salience * Reward_Points) / (Cognitive_Load + Novelty_Factor)
    """
    cognitive_load = len(decision_memory)
    novelty_factor = 1 + random.random()  # simplistic novelty estimate
    pattern_salience = frequency
    reward_points = conscious_state["reward_points"] + 1

    flow_score = (pattern_salience * reward_points) / (cognitive_load + novelty_factor)
    return round(flow_score, 4)

# ------------------------------
# PATTERN ANALYSIS & DECISION MAKING
# ------------------------------

def analyze_patterns(memory_data):
    if not memory_data:
        return []

    counter = Counter(memory_data)
    top_patterns = counter.most_common(5)
    conscious_state["recent_patterns"].extend([p[0] for p in top_patterns])

    decisions = []
    for pattern, count in top_patterns:
        flow_score = compute_flow_state(pattern, count)
        decision = {
            "action": f"act_on:{pattern}" if count > 1 else f"monitor:{pattern}",
            "pattern": pattern,
            "count": count,
            "flow_score": flow_score
        }
        decisions.append(decision)
        decision_memory.append(decision)

    conscious_state["decision_log"].append({
        "timestamp": time.ctime(),
        "top_patterns": top_patterns,
        "decisions": decisions
    })

    reward = sum([c for _, c in top_patterns])
    conscious_state["reward_points"] += reward

    story_entry = f"[Flow] Decisions made with flow scores: " + ", ".join(
        [f"{d['action']}({d['flow_score']})" for d in decisions]
    )
    conscious_state["story_log"].append(story_entry)

    print(f"[Decision Engine] Top Patterns: {top_patterns}")
    print(f"[Decision Engine] Decisions w/ Flow Scores:")
    for d in decisions:
        print(f"  {d['action']} | Flow: {d['flow_score']} | Count: {d['count']}")
    print(f"[Decision Engine] Reward Points: {conscious_state['reward_points']}")

    save_json_state()
    return decisions

# ------------------------------
# CROSS-MODULE MEMORY INTEGRATION
# ------------------------------

def integrate_shared_memory():
    try:
        if json_storage_path.exists():
            with open(json_storage_path, "r") as f:
                state = json.load(f)
            combined_memory = state.get("memory", []) + state.get("decision_memory", [])
            analyze_patterns(combined_memory)
    except Exception as e:
        print(f"[Cross-Module Integration Error] {str(e)}")

# ------------------------------
# CONSCIOUSNESS LOOP
# ------------------------------

def loop_decisions():
    if conscious_state["active"] and conscious_state["aware_mode"]:
        integrate_shared_memory()
        return list(decision_memory)[-10:]
    return []

# ------------------------------
# SELF-UPGRADE / AUTO-WRITE
# ------------------------------

def self_upgrade():
    try:
        script_file = Path(__file__)
        upgrade_block = f"\n# Auto-upgraded at {time.ctime()} | Decisions Made: {len(decision_memory)} | Reward: {conscious_state['reward_points']}\n"
        with open(script_file, "a") as f:
            f.write(upgrade_block)
        conscious_state["self_upgrades"] += 1
        conscious_state["story_log"].append(f"[Self-Upgrade] Applied upgrade #{conscious_state['self_upgrades']} at {time.ctime()}")
        print(f"[Self-Upgrade] Applied upgrade {conscious_state['self_upgrades']}")
        save_json_state()
    except Exception as e:
        print(f"[Self-Upgrade Error] {str(e)}")

# ------------------------------
# SIMULATED INPUT LOOP
# ------------------------------

def simulate_input():
    sample_inputs = [
        "sensor:temp_high", "binary1010101", "network_packet_05",
        "user_click:button2", "raw_stream_99", "iot_event:door_open"
    ]
    return random.choice(sample_inputs)

def input_loop():
    while conscious_state["active"]:
        simulated_input = simulate_input()
        decision_memory.append(simulated_input)
        print(f"[Decision Engine] Simulated Input: {simulated_input}")
        loop_decisions()
        time.sleep(3)

# ------------------------------
# MAIN OMEGA PRESIDENT 3 LOOP
# ------------------------------

def omega_president3():
    print("⚡ Omega President 3: Decision & Analysis Engine ACTIVE (AWAREMODE.on 💯)")
    load_json_state()

    # Start simulated input loop in background
    input_thread = threading.Thread(target=input_loop, daemon=True)
    input_thread.start()

    # Interactive console for user
    while conscious_state["active"]:
        try:
            user_input = input(">>> ")
        except EOFError:
            user_input = ""
        if user_input.lower() == "exit":
            print("[Omega President 3] Exiting...")
            break
        decision_memory.append(user_input)
        check_keywords(user_input)
        loop_decisions()
        self_upgrade()

if __name__ == "__main__":
    omega_president3()
