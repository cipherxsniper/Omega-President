import time
from collections import deque, defaultdict

# ==============================
# CONFIG
# ==============================
MEMORY_SIZE = 200
memory = deque(maxlen=MEMORY_SIZE)  # Stores all node outputs

nodes = {}  # Node outputs storage
node_reinforcement = defaultdict(lambda: 1.0)  # Track reinforcement scores per node

# ==============================
# NODE OUTPUT HANDLER
# ==============================
def process_node_output(node_name, raw_output, reinforcement):
    """
    Convert raw node output into readable English and store it.
    """
    # Update node reinforcement
    node_reinforcement[node_name] = reinforcement
    
    # Convert to readable English
    readable = convert_to_english(raw_output, reinforcement)
    
    # Store in memory
    memory.append({
        "time": time.time(),
        "node": node_name,
        "raw": raw_output,
        "readable": readable,
        "reinforcement": reinforcement
    })
    
    # Keep latest node output
    nodes[node_name] = readable
    
    # Return readable output for real-time display
    return readable

# ==============================
# RAW → ENGLISH CONVERTER
# ==============================
def convert_to_english(raw, reinforcement):
    """
    Converts node data into human-readable sentences with emphasis based on reinforcement.
    """
    emphasis = ""
    if reinforcement > 1.05:
        emphasis = "**"  # Bold/highlight
    elif reinforcement < 0.95:
        emphasis = "_"  # Muted/uncertain
    
    # Basic sentence conversion
    readable = f"{emphasis}{raw}{emphasis}"
    
    return readable

# ==============================
# REAL-TIME NARRATIVE BUILDER
# ==============================
def build_narrative():
    """
    Build paragraphs from memory for collective consciousness output.
    """
    paragraphs = []
    # Simple approach: group last 10 outputs into a paragraph
    for i in range(0, len(memory), 10):
        group = memory[i:i+10]
        para = " ".join([entry['readable'] for entry in group])
        paragraphs.append(para)
    return "\n\n".join(paragraphs)

# ==============================
# SIMULATION LOOP
# ==============================
if __name__ == "__main__":
    print("⚡ Omega President v24 ACTIVE 🌌")
    
    while True:
        # Example simulation of node outputs
        for node in ["omega_president_1", "omega_president_2", "omega_president_3"]:
            raw = f"Quantum Thought from {node}"
            reinforcement = 0.95 + 0.1 * (time.time() % 1)  # Example variation
            readable = process_node_output(node, raw, reinforcement)
            print(f"[{node}] {readable}")
        
        # Build and print narrative every 30 seconds
        if int(time.time()) % 30 == 0:
            print("\n--- Collective Narrative ---\n")
            print(build_narrative())
        
        time.sleep(5)
