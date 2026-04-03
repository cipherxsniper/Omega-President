import time
from collections import deque, defaultdict

# ==============================
# CONFIG / MEMORY
# ==============================
MEMORY_SIZE = 1000  # rolling memory
memory = deque(maxlen=MEMORY_SIZE)  # stores all node outputs
nodes = defaultdict(lambda: {"outputs": [], "last_seen": None})  # track all nodes

# ==============================
# NODE OUTPUT CAPTURE
# ==============================
def capture_node_output(node_id, raw_output, reinforcement_score=1.0):
    """
    Capture a node output with metadata
    """
    timestamp = time.time()
    entry = {
        "node": node_id,
        "timestamp": timestamp,
        "output": raw_output,
        "score": reinforcement_score
    }
    memory.append(entry)
    nodes[node_id]["outputs"].append(entry)
    nodes[node_id]["last_seen"] = timestamp

# ==============================
# SYMBOLIC → CONCEPT MAPPING
# ==============================
symbolic_map = {
    "wink wink thought": "suggestive insight",
    "AWARE": "self-recognition",
    # Extend this dynamically as Omega learns
}

def symbolic_to_concept(symbol):
    return symbolic_map.get(symbol, symbol)

# ==============================
# BUILD READABLE PARAGRAPHS
# ==============================
def build_narrative(memory_chunk):
    """
    Converts multiple node outputs into structured sentences & paragraphs
    """
    sentences = []
    # Sort by timestamp to maintain temporal flow
    memory_sorted = sorted(memory_chunk, key=lambda x: x["timestamp"])
    
    for entry in memory_sorted:
        concept = symbolic_to_concept(entry["output"])
        score = entry["score"]
        emphasis = "⚡ IMPORTANT: " if score > 1.05 else ""
        sentences.append(f"{emphasis}Node {entry['node']} observed: {concept}.")

    paragraph = " ".join(sentences)
    return paragraph

# ==============================
# AUTOMATIC LEARNING / MAPPING UPGRADE
# ==============================
def learn_new_concepts():
    """
    If multiple nodes repeat unknown symbols, add them to symbolic_map
    """
    counts = defaultdict(int)
    for entry in memory:
        if entry["output"] not in symbolic_map:
            counts[entry["output"]] += 1

    for symbol, count in counts.items():
        if count > 2:  # threshold to learn new pattern
            symbolic_map[symbol] = f"inferred concept ({symbol})"

# ==============================
# LIVE OBSERVATION / LOGGING
# ==============================
def log_narrative(filename="omega_readable_log.txt"):
    """
    Write readable narrative to file
    """
    narrative = build_narrative(list(memory))
    with open(filename, "w") as f:
        f.write(f"{time.ctime()}:\n{narrative}\n\n")
    print(narrative)  # also print live for Termux observation

# ==============================
# MAIN LOOP (run alongside Mega_Omega_v11.py)
# ==============================
def run_observer_loop():
    """
    Keeps Omega narrative running, updates learning
    """
    try:
        while True:
            learn_new_concepts()  # upgrade its own symbolic map
            log_narrative()        # update readable output
            time.sleep(2)          # adjust refresh speed
    except KeyboardInterrupt:
        print("Omega observer loop interrupted. Saving memory...")
        log_narrative()

# Example capture (simulate node outputs)
if __name__ == "__main__":
    # Simulate continuous node output
    for i in range(1, 6):
        capture_node_output(f"omega_president_{i}", "wink wink thought", reinforcement_score=1.07)
        capture_node_output(f"omega_president_{i}", "AWARE", reinforcement_score=1.02)

    run_observer_loop()
