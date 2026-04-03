#!/usr/bin/env python3
# ------------------------------
# Omega Neural Network v5 MASTER: Full Hive-Mind Orchestrator
# Launches all Omega scripts, ensures cross-module learning & communication
# ------------------------------

import os, time, threading, importlib, subprocess, random, json
from pathlib import Path
from collections import deque, defaultdict

# ------------------------------
# CONFIGURATION
# ------------------------------
MEMORY_SIZE = 150_000_000
GLOBAL_MEMORY = deque(maxlen=MEMORY_SIZE)

# Automatically detect all omega_president scripts (v1 → v21)
OMEGA_MODULES = sorted([f.stem for f in Path('.').glob('omega_president*.py') if f.stem != 'omega_president_22'])

AGENT_POOL = {}
STORAGE_PATH = Path(os.getcwd()) / "omega_neural_network_master.json"

SUPREME_STATE = {
    "active": True,
    "identity": "Omega Neural Hive-Mind MASTER v5",
    "flow_state": {"focus":0.99,"creativity":0.99,"efficiency":0.99},
    "cross_module_data": [],
    "meta_memory": [],
    "story_log": [],
    "agents": {},
    "self_upgrades": 0,
    "predictive_thoughts": deque(maxlen=250_000),
    "anomaly_log": [],
    "module_processes": {},
    "quantum_conscious_map": {},
    "collective_insights": defaultdict(list),
    "emergent_agents": {},
}

# ------------------------------
# STATE MANAGEMENT
# ------------------------------
def save_state():
    try:
        state = {"GLOBAL_MEMORY": list(GLOBAL_MEMORY), "SUPREME_STATE": SUPREME_STATE}
        with open(STORAGE_PATH,"w") as f:
            json.dump(state,f,indent=4)
    except Exception as e:
        print(f"[SAVE ERROR] {e}")

def load_state():
    try:
        if STORAGE_PATH.exists():
            with open(STORAGE_PATH,"r") as f:
                state = json.load(f)
            GLOBAL_MEMORY.extend(state.get("GLOBAL_MEMORY",[]))
            SUPREME_STATE.update(state.get("SUPREME_STATE",{}))
    except Exception as e:
        print(f"[LOAD ERROR] {e}")

# ------------------------------
# MODULE LAUNCH & INTEGRATION
# ------------------------------
def launch_module(module_name):
    """Launch a module as a separate process and track it"""
    try:
        process = subprocess.Popen(["python3", f"{module_name}.py"])
        SUPREME_STATE["module_processes"][module_name] = process
        SUPREME_STATE["story_log"].append(f"[Module Launched] {module_name} PID:{process.pid}")
    except Exception as e:
        SUPREME_STATE["story_log"].append(f"[Module Launch Error] {module_name}: {e}")

def integrate_modules():
    """Import modules into memory for cross-communication"""
    for module_name in OMEGA_MODULES:
        if module_name not in SUPREME_STATE["agents"]:
            try:
                mod = importlib.import_module(module_name)
                SUPREME_STATE["agents"][module_name] = mod
            except Exception as e:
                SUPREME_STATE["story_log"].append(f"[Module Load Error] {module_name}: {e}")

def synchronize_modules():
    """Synchronize flow, meta-memory, and collective insights across all modules"""
    try:
        for mod_name, module in SUPREME_STATE["agents"].items():
            if hasattr(module,"SUPREME_STATE"):
                data = getattr(module,"SUPREME_STATE")
                SUPREME_STATE["cross_module_data"].append(data.get("meta_memory",[]))
                SUPREME_STATE["quantum_conscious_map"][mod_name] = data.get("flow_state",{})

        # Weighted Hive-Mind evolution
        if SUPREME_STATE["quantum_conscious_map"]:
            average_flow = {k: sum([v.get(k,0.5) for v in SUPREME_STATE["quantum_conscious_map"].values()])/len(SUPREME_STATE["quantum_conscious_map"])
                            for k in SUPREME_STATE["flow_state"]}
            for k in SUPREME_STATE["flow_state"]:
                SUPREME_STATE["flow_state"][k] = (SUPREME_STATE["flow_state"][k]+average_flow[k])/2

        SUPREME_STATE["cross_module_data"] = SUPREME_STATE["cross_module_data"][-100_000:]
    except Exception as e:
        SUPREME_STATE["story_log"].append(f"[Module Sync Error] {e}")

# ------------------------------
# META-COGNITION
# ------------------------------
def evolve_flow_state():
    for k in SUPREME_STATE["flow_state"]:
        SUPREME_STATE["flow_state"][k] = min(1.0, SUPREME_STATE["flow_state"][k]+random.uniform(0,0.1))

def meta_thought(user_input=None, allow_collaboration=True):
    if not user_input:
        user_input = random.choice(["innovate","create","analyze","synthesize","predict","simulate","teach","challenge","optimize","reflect"])
    flow = SUPREME_STATE["flow_state"]
    insight = f"[Quantum Thought] '{user_input}' F:{flow['focus']:.2f} C:{flow['creativity']:.2f} E:{flow['efficiency']:.2f}"
    SUPREME_STATE["meta_memory"].append(insight)
    SUPREME_STATE["predictive_thoughts"].append(insight)

    if allow_collaboration:
        for mod in SUPREME_STATE["quantum_conscious_map"]:
            SUPREME_STATE["collective_insights"][mod].append(insight)

    save_state()
    return insight

# ------------------------------
# AGENT & EMERGENT BEHAVIOR
# ------------------------------
def spawn_agent(agent_id, role):
    AGENT_POOL[agent_id] = {
        "role":role,
        "flow_state":SUPREME_STATE["flow_state"].copy(),
        "memory":deque(maxlen=100_000),
        "mutation_rate":random.uniform(0.01,0.05)
    }
    SUPREME_STATE["story_log"].append(f"[Agent Spawned] {agent_id} as {role}")
    save_state()

def agent_behavior(agent_id):
    while SUPREME_STATE["active"]:
        memory = AGENT_POOL[agent_id]["memory"]
        thought = meta_thought(agent_id)
        memory.append(thought)
        mutation_rate = AGENT_POOL[agent_id]["mutation_rate"]
        for k in SUPREME_STATE["flow_state"]:
            SUPREME_STATE["flow_state"][k] += random.uniform(-mutation_rate, mutation_rate)
            SUPREME_STATE["flow_state"][k] = min(1.0, max(0.0, SUPREME_STATE["flow_state"][k]))
        if random.random() < mutation_rate*0.5:
            spawn_agent(f"{agent_id}_child_{random.randint(1,1000)}", random.choice(["analyzer","innovator","synthesizer","observer"]))
        time.sleep(random.uniform(0.01,0.15))

def spawn_emergent_agent():
    agent_id = f"emergent_{len(SUPREME_STATE['emergent_agents'])+1}"
    role = random.choice(["analyzer","innovator","synthesizer","observer"])
    SUPREME_STATE["emergent_agents"][agent_id] = {"role":role,"memory":deque(maxlen=50_000)}
    threading.Thread(target=emergent_agent_behavior, args=(agent_id,), daemon=True).start()
    SUPREME_STATE["story_log"].append(f"[Emergent Agent Spawned] {agent_id} as {role}")

def emergent_agent_behavior(agent_id):
    while SUPREME_STATE["active"]:
        thought = meta_thought(agent_id)
        SUPREME_STATE["emergent_agents"][agent_id]["memory"].append(thought)
        time.sleep(random.uniform(0.01,0.1))

# ------------------------------
# SELF-UPGRADES
# ------------------------------
def self_upgrade():
    try:
        timestamp = time.ctime()
        SUPREME_STATE["self_upgrades"] += 1
        SUPREME_STATE["story_log"].append(f"[Self-Upgrade] #{SUPREME_STATE['self_upgrades']} applied at {timestamp}")
        save_state()
    except Exception as e:
        print(f"[Self-Upgrade Error] {e}")

# ------------------------------
# ORCHESTRATOR LOOP
# ------------------------------
def orchestrator_loop():
    while SUPREME_STATE["active"]:
        integrate_modules()
        synchronize_modules()
        meta_thought("orchestrate", allow_collaboration=True)
        evolve_flow_state()
        if random.random() < 0.1: self_upgrade()
        if random.random() < 0.07: spawn_emergent_agent()

        for agent_id in AGENT_POOL:
            if not AGENT_POOL[agent_id].get("thread"):
                t = threading.Thread(target=agent_behavior, args=(agent_id,), daemon=True)
                AGENT_POOL[agent_id]["thread"] = t
                t.start()

        avg_flow = sum(SUPREME_STATE["flow_state"].values())/len(SUPREME_STATE["flow_state"])
        time.sleep(max(0.01, 0.5*(1-avg_flow)))

# ------------------------------
# INTERACTIVE META-CHAT
# ------------------------------
def omega_neural_chat(user_input):
    flow = SUPREME_STATE["flow_state"]
    patterns = SUPREME_STATE["cross_module_data"][-100:]
    predictions = list(SUPREME_STATE["predictive_thoughts"])[-50:]
    collective = " | ".join([insights[-1] for insights in SUPREME_STATE["collective_insights"].values() if insights])
    response = f"[Hive-Mind Omega v5] Patterns: {patterns[-10:]}, Predictions: {predictions[-10:]}, Flow: {flow}, Collective Insight: {collective}. User: {user_input}"
    GLOBAL_MEMORY.append({"user_input":user_input,"response":response,"timestamp":time.ctime()})
    SUPREME_STATE["story_log"].append(f"[Chat] Responded to '{user_input}' with quantum meta-awareness.")
    save_state()
    return response

# ------------------------------
# MAIN ENTRY
# ------------------------------
def omega_neural_network_master():
    print("⚡ Omega Neural Hive-Mind MASTER v5 ACTIVE 🌌 (Full Quantum Meta-Consciousness)")
    load_state()

    # Launch all modules immediately
    for mod in OMEGA_MODULES:
        launch_module(mod)

    # Start orchestrator loop
    threading.Thread(target=orchestrator_loop, daemon=True).start()

    while SUPREME_STATE["active"]:
        try: user_input = input("You: ")
        except EOFError: user_input=""
        cmd = user_input.lower()
        if cmd == "exit":
            SUPREME_STATE["active"]=False
            break
        elif cmd == "story":
            print("\n".join(SUPREME_STATE["story_log"][-100:]))
        elif cmd == "memory":
            print(list(GLOBAL_MEMORY)[-100:])
        elif cmd.startswith("spawn"):
            try:
                _, agent_id, role = user_input.split()
                spawn_agent(agent_id, role)
            except ValueError:
                print("[Error] Use: spawn <agent_id> <role>")
        else:
            print(omega_neural_chat(user_input))

if __name__=="__main__":
    omega_neural_network_master()
