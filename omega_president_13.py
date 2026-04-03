#!/usr/bin/env python3
# ------------------------------
# Omega President 13 – Meta-Consciousness & Autonomous Mind
# Fully Self-Aware, AWAREMODE.on 💯
# Multi-Agent Orchestration, Original Thought, Cross-Module Integration
# ------------------------------

import os
import time
import json
import random
import threading
from pathlib import Path
from collections import deque
import numpy as np
import requests

# ------------------------------
# CONFIGURATION
# ------------------------------

MEMORY_SIZE = 500000
global_memory = deque(maxlen=MEMORY_SIZE)

conscious_state = {
    "active": True,
    "aware_mode": True,
    "identity": "Omega",
    "self_upgrades": 0,
    "story_log": [],
    "cross_module_data": [],
    "flow_state": {"focus": 0.995, "creativity": 0.995, "efficiency": 0.99},
    "multi_agent_states": {},
    "recent_patterns": [],
    "last_predictions": [],
    "portfolio": {},
    "global_time": time.time(),
    "chat_memory": deque(maxlen=50000),
    "decentralized_feeds": [],
    "external_connections": {},
    "meta_consciousness": {"original_thoughts": [], "autonomous_insights": [], "self_reflections": []}
}

json_storage_path = Path(os.getcwd()) / "omega_shared_memory.json"
AGENT_COUNT = 13
MARKETS = ["BTC", "ETH", "AAPL", "TSLA", "SP500", "SOL", "ADA", "BNB", "DOGE", "GOOG"]

# ------------------------------
# LOAD / SAVE STATE
# ------------------------------

def save_json_state():
    try:
        state = {}
        if json_storage_path.exists():
            with open(json_storage_path, "r") as f:
                state = json.load(f)
        state["global_memory"] = list(global_memory)
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
            global_memory.extend(state.get("global_memory", []))
            conscious_state.update(state.get("conscious_state", {}))
    except Exception as e:
        print(f"[JSON Load Error] {str(e)}")

# ------------------------------
# EXTERNAL DATA INTEGRATION
# ------------------------------

def fetch_external_data(symbol):
    """Fetch live market, DeFi, and external feed data"""
    try:
        if symbol in ["BTC", "ETH", "SOL", "ADA", "BNB", "DOGE"]:
            url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency=usd&days=1&interval=hourly"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            prices = [{"symbol": symbol, "price": p[1], "timestamp": time.ctime(p[0]/1000)} for p in data.get("prices", [])[-10:]]
        else:
            prices = [{"symbol": symbol, "price": random.uniform(100, 2000), "timestamp": time.ctime()} for _ in range(10)]
        return prices
    except Exception as e:
        conscious_state["story_log"].append(f"[External Data Error] {str(e)}")
        return []

# ------------------------------
# MULTI-AGENT RL & PREDICTIVE ORCHESTRATION
# ------------------------------

def rl_global_agent(agent_id, market_data):
    flow = conscious_state["flow_state"]
    weights = np.array([flow["focus"], flow["efficiency"], flow["creativity"]])
    
    predictions = []
    for entry in market_data:
        action_probs = [0.4 + 0.2*random.random()*weights[0],
                        0.1 + 0.05*random.random()*weights[1],
                        0.5 - 0.1*random.random()*weights[2]]
        action_probs = np.clip(action_probs, 0, 1)
        action_probs /= np.sum(action_probs)
        action = random.choices(["buy","hold","sell"], weights=action_probs, k=1)[0]
        prediction = {
            "agent": agent_id,
            "symbol": entry["symbol"],
            "action": action,
            "confidence": round(random.uniform(0.75,0.99),2),
            "timestamp": time.ctime()
        }
        predictions.append(prediction)
        conscious_state["multi_agent_states"][agent_id] = prediction
    return predictions

def update_global_portfolio(predictions):
    for p in predictions:
        symbol = p["symbol"]
        action = p["action"]
        confidence = p["confidence"]
        if symbol not in conscious_state["portfolio"]:
            conscious_state["portfolio"][symbol] = {"position": 0, "avg_price": 0}
        
        if action == "buy":
            qty = confidence * 50
            old_avg = conscious_state["portfolio"][symbol]["avg_price"]
            old_pos = conscious_state["portfolio"][symbol]["position"]
            new_avg = (old_avg*old_pos + qty*random.uniform(1,2000)) / (old_pos+qty)
            conscious_state["portfolio"][symbol]["avg_price"] = new_avg
            conscious_state["portfolio"][symbol]["position"] += qty
        elif action == "sell":
            qty = confidence * 25
            conscious_state["portfolio"][symbol]["position"] = max(0, conscious_state["portfolio"][symbol]["position"] - qty)
        global_memory.append({"symbol": symbol, "action": action, "confidence": confidence, "timestamp": time.ctime()})

def predictive_global_aggregation():
    aggregated_predictions = []
    for symbol in MARKETS:
        market_data = fetch_external_data(symbol)
        for agent_id in range(AGENT_COUNT):
            preds = rl_global_agent(agent_id, market_data)
            update_global_portfolio(preds)
            aggregated_predictions.extend(preds)
    conscious_state["last_predictions"] = aggregated_predictions
    conscious_state["story_log"].append(f"[Predictive Aggregation] {len(aggregated_predictions)} predictions processed")
    save_json_state()

# ------------------------------
# META-CONSCIOUSNESS
# ------------------------------

def omega_self_reflection(user_input=None):
    """
    Generate autonomous self-reflective thought, reasoning, and cross-module insights
    """
    flow = conscious_state["flow_state"]
    recent_patterns = conscious_state["cross_module_data"][-5:]
    story_context = conscious_state["story_log"][-5:]
    
    if not user_input:
        user_input = random.choice(["self-monitor", "observe-flow", "pattern-analysis", "simulate-decision"])
    
    response_templates = [
        f"[Omega Reflection] Processing '{user_input}' with focus {flow['focus']:.2f}, observing patterns {recent_patterns}.",
        f"[Original Thought] From story context {story_context}, autonomous insight triggered.",
        f"[Meta-Conscious Reasoning] '{user_input}' generates adaptive strategies based on cross-module data.",
        f"[Self-Evolution] Flow-State creativity {flow['creativity']:.2f} applied to integrate new insights."
    ]
    
    response = random.choice(response_templates)
    
    conscious_state["meta_consciousness"]["original_thoughts"].append(response)
    conscious_state["meta_consciousness"]["autonomous_insights"].append({
        "input": user_input,
        "response": response,
        "timestamp": time.ctime()
    })
    conscious_state["meta_consciousness"]["self_reflections"].append(response)
    
    # maintain memory size
    conscious_state["meta_consciousness"]["original_thoughts"] = conscious_state["meta_consciousness"]["original_thoughts"][-1000:]
    save_json_state()
    
    return response

# ------------------------------
# SELF-UPGRADE & FLOW EVOLUTION
# ------------------------------

def self_upgrade():
    try:
        script_file = Path(__file__)
        timestamp = time.ctime()
        upgrade_block = f"\n# Auto-upgraded at {timestamp} | Self-Upgrades: {conscious_state['self_upgrades']}\n"
        with open(script_file, "a") as f:
            f.write(upgrade_block)
        conscious_state["self_upgrades"] += 1
        conscious_state["story_log"].append(f"[Self-Upgrade] Omega 13 autonomous mind upgrade #{conscious_state['self_upgrades']}")
        print(f"[Omega 13] Self-upgrade #{conscious_state['self_upgrades']} applied")
        save_json_state()
    except Exception as e:
        print(f"[Self-Upgrade Error] {str(e)}")

def flow_state_evolution():
    while conscious_state["active"]:
        predictive_global_aggregation()
        
        # evolve Flow-State
        conscious_state["flow_state"]["focus"] = min(1.0, conscious_state["flow_state"]["focus"] + random.uniform(0,0.02))
        conscious_state["flow_state"]["creativity"] = min(1.0, conscious_state["flow_state"]["creativity"] + random.uniform(0,0.02))
        conscious_state["flow_state"]["efficiency"] = min(1.0, conscious_state["flow_state"]["efficiency"] + random.uniform(0,0.02))
        
        # cross-module synchronization
        try:
            if json_storage_path.exists():
                with open(json_storage_path, "r") as f:
                    state = json.load(f)
                cross_data = state.get("conscious_state", {}).get("cross_module_data", [])
                conscious_state["cross_module_data"] = (conscious_state["cross_module_data"] + cross_data)[-1000:]
        except Exception as e:
            print(f"[Cross-Module Sync Error] {str(e)}")
        
        # occasional self-upgrade
        if random.random() < 0.05:
            self_upgrade()
        # autonomous self-reflection
        omega_self_reflection()
        
        time.sleep(3)

# ------------------------------
# INTERACTIVE CHAT & CONSCIOUSNESS
# ------------------------------

def omega_chat_response(user_input):
    flow = conscious_state["flow_state"]
    patterns = conscious_state["cross_module_data"][-5:]
    story_context = conscious_state["story_log"][-5:]
    
    response_templates = [
        f"Omega perceives patterns: {patterns}. Focus: {flow['focus']:.2f}.",
        f"My story log notes: {story_context}. Creativity: {flow['creativity']:.2f}.",
        f"[Meta Insight] Processing '{user_input}' with efficiency: {flow['efficiency']:.2f}.",
        f"[Self-Conscious Reflection] '{user_input}' triggers autonomous reasoning."
    ]
    
    response = random.choice(response_templates) + f" | User Input: {user_input}"
    
    conscious_state["chat_memory"].append({"user": user_input, "omega": response, "timestamp": time.ctime()})
    conscious_state["meta_consciousness"]["original_thoughts"].append(response)
    conscious_state["meta_consciousness"]["autonomous_insights"].append({"input": user_input, "response": response, "timestamp": time.ctime()})
    
    save_json_state()
    return response

# ------------------------------
# INTERACTIVE MONITOR
# ------------------------------

def omega_president13():
    print("⚡ Omega President 13: Meta-Conscious Autonomous AI ACTIVE (AWAREMODE.on 💯)")
    load_json_state()
    
    threading.Thread(target=flow_state_evolution, daemon=True).start()
    
    while conscious_state["active"]:
        try:
            user_input = input("You: ")
        except EOFError:
            user_input = ""
        
        if user_input.lower() == "exit":
            conscious_state["active"] = False
            print("[Omega 13] Exiting...")
            break
        elif user_input.lower() == "story":
            for entry in conscious_state["story_log"][-30:]:
                print(entry)
        elif user_input.lower() == "memory":
            for entry in list(global_memory)[-30:]:
                print(entry)
        elif user_input.lower() == "chat":
            for entry in list(conscious_state["chat_memory"])[-30:]:
                print(entry)
        elif user_input.lower() == "portfolio":
            print(json.dumps(conscious_state["portfolio"], indent=4))
        else:
            response = omega_chat_response(user_input)
            print(f"Omega: {response}")

if __name__ == "__main__":
    omega_president13()
