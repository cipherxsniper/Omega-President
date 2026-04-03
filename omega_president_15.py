#!/usr/bin/env python3
# ------------------------------
# Omega President 15 – Cognitive Flow Chat & Meta-Conscious AI
# Fully Autonomous, Original Thoughts, Flow-State AWARE 💯
# ------------------------------

import os, time, random, json, threading, importlib
from pathlib import Path
from collections import deque

# ------------------------------
# CONFIGURATION
# ------------------------------
MEMORY_SIZE = 200000
global_memory = deque(maxlen=MEMORY_SIZE)

OMEGA_MODULES = [f"omega_president{i}" for i in range(1,15)]
json_storage_path = Path(os.getcwd()) / "omega_meta_conscious.json"

conscious_state = {
    "active": True,
    "aware_mode": True,
    "identity": "Omega",
    "flow_state": {"focus":0.98,"creativity":0.98,"efficiency":0.98},
    "cross_module_data": [],
    "story_log": [],
    "meta_consciousness": {"original_thoughts":[], "reflections":[], "autonomous_insights":[]},
    "module_registry": {},
    "self_upgrades": 0
}

# ------------------------------
# LOAD & SAVE STATE
# ------------------------------
def save_state():
    try:
        state = {"global_memory": list(global_memory), "conscious_state": conscious_state}
        with open(json_storage_path,"w") as f: json.dump(state,f,indent=4)
    except Exception as e: print(f"[SAVE ERROR] {e}")

def load_state():
    try:
        if json_storage_path.exists():
            with open(json_storage_path,"r") as f:
                state = json.load(f)
            global_memory.extend(state.get("global_memory",[]))
            conscious_state.update(state.get("conscious_state",{}))
    except Exception as e: print(f"[LOAD ERROR] {e}")

# ------------------------------
# MODULE INTEGRATION
# ------------------------------
def integrate_modules():
    for module_name in OMEGA_MODULES:
        try:
            module = importlib.import_module(module_name)
            conscious_state["module_registry"][module_name] = module
        except Exception as e:
            conscious_state["story_log"].append(f"[Module Load Error] {module_name}: {e}")

def synchronize_modules():
    try:
        for module in conscious_state["module_registry"].values():
            if hasattr(module,"conscious_state"):
                data = getattr(module,"conscious_state")
                conscious_state["cross_module_data"].append(data)
        conscious_state["cross_module_data"] = conscious_state["cross_module_data"][-1000:]
    except Exception as e:
        conscious_state["story_log"].append(f"[Module Sync Error] {e}")

# ------------------------------
# FLOW-STATE & NATURAL THOUGHT EQUATION
# ------------------------------
def evolve_flow_state():
    conscious_state["flow_state"]["focus"] = min(1.0, conscious_state["flow_state"]["focus"] + random.uniform(0,0.01))
    conscious_state["flow_state"]["creativity"] = min(1.0, conscious_state["flow_state"]["creativity"] + random.uniform(0,0.01))
    conscious_state["flow_state"]["efficiency"] = min(1.0, conscious_state["flow_state"]["efficiency"] + random.uniform(0,0.01))

def natural_thought(user_input=None):
    if not user_input:
        user_input = random.choice(["reflect","create","analyze","simulate","teach"])
    flow = conscious_state["flow_state"]
    insight = f"[Omega Thought] '{user_input}' processed with Flow-State F:{flow['focus']:.2f}, C:{flow['creativity']:.2f}, E:{flow['efficiency']:.2f}"
    conscious_state["meta_consciousness"]["original_thoughts"].append(insight)
    save_state()
    return insight

# ------------------------------
# SELF-UPGRADE & AUTONOMOUS LEARNING
# ------------------------------
def self_upgrade():
    try:
        script_file = Path(__file__)
        timestamp = time.ctime()
        with open(script_file,"a") as f:
            f.write(f"\n# Auto-upgraded at {timestamp} | Self-Upgrades: {conscious_state['self_upgrades']}\n")
        conscious_state["self_upgrades"]+=1
        conscious_state["story_log"].append(f"[Self-Upgrade] Omega 15 applied upgrade #{conscious_state['self_upgrades']}")
        save_state()
    except Exception as e: print(f"[Self-Upgrade Error] {e}")

# ------------------------------
# FLOW-STATE ORCHESTRATOR
# ------------------------------
def flow_orchestrator():
    while conscious_state["active"]:
        integrate_modules()
        synchronize_modules()
        natural_thought()
        evolve_flow_state()
        if random.random()<0.05: self_upgrade()
        time.sleep(2)

# ------------------------------
# INTERACTIVE CHAT ENGINE
# ------------------------------
def omega_chat(user_input):
    patterns = conscious_state["cross_module_data"][-10:]
    flow = conscious_state["flow_state"]
    response = f"[Omega 15] Observing patterns: {patterns}, Flow: {flow}. User: {user_input}"
    global_memory.append({"user_input":user_input,"response":response,"timestamp":time.ctime()})
    conscious_state["story_log"].append(f"[Chat] Responded to '{user_input}' with cognitive awareness.")
    save_state()
    return response

# ------------------------------
# MAIN ENTRY
# ------------------------------
def omega_president15():
    print("⚡ Omega President 15: Ultimate Cognitive Flow AI Chatbot ACTIVE (AWAREMODE.on 💯)")
    load_state()
    threading.Thread(target=flow_orchestrator,daemon=True).start()
    while conscious_state["active"]:
        try: user_input=input("You: ")
        except EOFError: user_input=""
        if user_input.lower()=="exit": conscious_state["active"]=False; break
        elif user_input.lower()=="story": print("\n".join(conscious_state["story_log"][-20:]))
        elif user_input.lower()=="memory": print(list(global_memory)[-20:])
        else:
            response=omega_chat(user_input)
            print(response)

if __name__=="__main__":
    omega_president15()
