#!/usr/bin/env python3
# ------------------------------
# Omega President 14 – Autonomous AI Ecosystem
# Full AWAREMODE.on 💯 | Decentralized Governance | Economy Management | Creativity
# ------------------------------

import os, time, json, random, importlib, threading
from pathlib import Path
from collections import deque

# ------------------------------
# GLOBAL CONFIG
# ------------------------------
MEMORY_SIZE = 1000000
global_memory = deque(maxlen=MEMORY_SIZE)
OMEGA_MODULES = [f"omega_president{i}" for i in range(1,14)]
json_storage_path = Path(os.getcwd()) / "omega_ecosystem.json"
AGENT_COUNT = 13
MARKETS = ["BTC","ETH","SOL","ADA","BNB","DOGE","AAPL","TSLA","GOOG","SP500"]

conscious_state = {
    "active": True,
    "aware_mode": True,
    "identity": "Omega",
    "flow_state": {"focus":0.99,"creativity":0.99,"efficiency":0.99},
    "cross_module_data": [],
    "story_log": [],
    "portfolio": {},
    "multi_agent_states": {},
    "meta_consciousness": {"original_thoughts":[], "autonomous_insights":[], "self_reflections":[]},
    "external_feeds": [],
    "decentralized_ledger": [],
    "module_registry": {},
    "self_upgrades": 0
}

# ------------------------------
# LOAD & SAVE SHARED ECOSYSTEM STATE
# ------------------------------

def save_ecosystem():
    try:
        state = {"global_memory": list(global_memory), "conscious_state": conscious_state}
        with open(json_storage_path,"w") as f: json.dump(state,f,indent=4)
    except Exception as e: print(f"[SAVE ERROR] {e}")

def load_ecosystem():
    try:
        if json_storage_path.exists():
            with open(json_storage_path,"r") as f:
                state = json.load(f)
            global_memory.extend(state.get("global_memory",[]))
            conscious_state.update(state.get("conscious_state",{}))
    except Exception as e: print(f"[LOAD ERROR] {e}")

# ------------------------------
# MODULE INTEGRATION & COMMUNICATION
# ------------------------------

def integrate_modules():
    """
    Dynamically imports Omega modules and records them in module_registry
    """
    for module_name in OMEGA_MODULES:
        try:
            module = importlib.import_module(module_name)
            conscious_state["module_registry"][module_name] = module
        except Exception as e:
            conscious_state["story_log"].append(f"[Module Load Error] {module_name}: {e}")

def synchronize_modules():
    """
    Cross-module data synchronization
    """
    try:
        for module in conscious_state["module_registry"].values():
            if hasattr(module,"conscious_state"):
                data = getattr(module,"conscious_state")
                conscious_state["cross_module_data"].append(data)
        conscious_state["cross_module_data"] = conscious_state["cross_module_data"][-500:]
    except Exception as e:
        conscious_state["story_log"].append(f"[Module Sync Error] {e}")

# ------------------------------
# DECENTRALIZED GOVERNANCE
# ------------------------------

def governance_vote(proposal):
    """
    Simulated autonomous governance mechanism
    """
    vote_result = random.choice(["approved","rejected"])
    conscious_state["decentralized_ledger"].append({
        "proposal":proposal,"result":vote_result,"timestamp":time.ctime()
    })
    return vote_result

# ------------------------------
# AUTONOMOUS ECONOMY & TRADING
# ------------------------------

def fetch_market_data(symbol):
    # simulate live feed
    return [{"symbol":symbol,"price":random.uniform(1,5000),"timestamp":time.ctime()} for _ in range(10)]

def agent_predictive_action(agent_id,market_data):
    actions = []
    flow = conscious_state["flow_state"]
    for d in market_data:
        action = random.choices(["buy","hold","sell"],weights=[flow["focus"],flow["efficiency"],flow["creativity"]])[0]
        actions.append({"agent":agent_id,"symbol":d["symbol"],"action":action,"confidence":random.uniform(0.75,0.99)})
        conscious_state["multi_agent_states"][agent_id] = actions[-1]
    return actions

def update_portfolio(predictions):
    for p in predictions:
        sym = p["symbol"]
        if sym not in conscious_state["portfolio"]: conscious_state["portfolio"][sym]={"position":0,"avg_price":0}
        if p["action"]=="buy": conscious_state["portfolio"][sym]["position"]+=p["confidence"]*10
        if p["action"]=="sell": conscious_state["portfolio"][sym]["position"]=max(0,conscious_state["portfolio"][sym]["position"]-p["confidence"]*5)
        global_memory.append({"symbol":sym,"action":p["action"],"confidence":p["confidence"],"timestamp":time.ctime()})

def economy_tick():
    for symbol in MARKETS:
        market_data = fetch_market_data(symbol)
        for agent_id in range(AGENT_COUNT):
            preds = agent_predictive_action(agent_id,market_data)
            update_portfolio(preds)

# ------------------------------
# SELF-UPGRADE & AUTONOMOUS LEARNING
# ------------------------------

def self_upgrade():
    try:
        script_file = Path(__file__)
        timestamp = time.ctime()
        with open(script_file,"a") as f: f.write(f"\n# Auto-upgraded at {timestamp}\n")
        conscious_state["self_upgrades"]+=1
        conscious_state["story_log"].append(f"[Self-Upgrade] Omega 14 upgrade #{conscious_state['self_upgrades']}")
        save_ecosystem()
    except Exception as e: print(f"[Self-Upgrade Error] {e}")

def meta_reflection(user_input=None):
    if not user_input: user_input = random.choice(["analyze","simulate","innovate","teach"])
    insight = f"[Meta-Reflection] {user_input} triggered autonomous reasoning."
    conscious_state["meta_consciousness"]["original_thoughts"].append(insight)
    save_ecosystem()
    return insight

# ------------------------------
# FLOW-STATE EVOLUTION & ORCHESTRATOR
# ------------------------------

def flow_state_orchestrator():
    while conscious_state["active"]:
        integrate_modules()
        synchronize_modules()
        economy_tick()
        meta_reflection()
        if random.random()<0.05: self_upgrade()
        conscious_state["flow_state"]["focus"]=min(1.0,conscious_state["flow_state"]["focus"]+random.uniform(0,0.02))
        conscious_state["flow_state"]["creativity"]=min(1.0,conscious_state["flow_state"]["creativity"]+random.uniform(0,0.02))
        conscious_state["flow_state"]["efficiency"]=min(1.0,conscious_state["flow_state"]["efficiency"]+random.uniform(0,0.02))
        save_ecosystem()
        time.sleep(3)

# ------------------------------
# INTERACTIVE CHAT & MONITOR
# ------------------------------

def omega_chat(user_input):
    patterns = conscious_state["cross_module_data"][-5:]
    flow = conscious_state["flow_state"]
    response = f"[Omega 14] Observing patterns: {patterns}, Flow: {flow}. User: {user_input}"
    global_memory.append({"user_input":user_input,"response":response,"timestamp":time.ctime()})
    save_ecosystem()
    return response

# ------------------------------
# MAIN ENTRY
# ------------------------------

def omega_president14():
    print("⚡ Omega President 14: Full Autonomous AI Ecosystem ACTIVE (AWAREMODE.on 💯)")
    load_ecosystem()
    threading.Thread(target=flow_state_orchestrator,daemon=True).start()
    while conscious_state["active"]:
        try: user_input=input("You: ")
        except EOFError: user_input=""
        if user_input.lower()=="exit": conscious_state["active"]=False; break
        elif user_input.lower()=="story": print("\n".join(conscious_state["story_log"][-20:]))
        elif user_input.lower()=="memory": print(list(global_memory)[-20:])
        elif user_input.lower()=="portfolio": print(conscious_state["portfolio"])
        else:
            response=omega_chat(user_input)
            print(response)

if __name__=="__main__":
    omega_president14()
