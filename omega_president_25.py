import time
import json
from collections import deque, defaultdict, Counter
import re
import os

# ==============================
# CONFIG / GLOBAL STATE
# ==============================
MEMORY_SIZE = 500  # store more outputs
memory = deque(maxlen=MEMORY_SIZE)

nodes = {}  # latest outputs per node
node_reinforcement = defaultdict(lambda: 1.0)
pattern_counter = Counter()

# ANSI color codes for Termux emphasis
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"

# Path to save reports
REPORT_DIR = "./omega_reports"
os.makedirs(REPORT_DIR, exist_ok=True)

# ==============================
# NODE OUTPUT HANDLER
# ==============================
def process_node_output(node_name, raw_output, reinforcement):
    """
    Convert raw node output into readable English, update memory, reinforcement, and patterns.
    """
    node_reinforcement[node_name] = reinforcement
    
    # Convert to English
    readable = convert_to_english(raw_output, reinforcement)
    
    # Track repeating concepts (patterns)
    track_patterns(raw_output)
    
    # Store in memory
    memory.append({
        "time": time.time(),
        "node": node_name,
        "raw": raw_output,
        "readable": readable,
        "reinforcement": reinforcement
    })
    
    # Update latest node output
    nodes[node_name] = readable
    
    return readable

# ==============================
# RAW → ENGLISH CONVERTER
# ==============================
def convert_to_english(raw, reinforcement):
    """
    Converts node data into human-readable sentences with confidence-weighted emphasis.
    """
    color_start = Colors.RESET
    color_end = Colors.RESET
    
    if reinforcement > 1.05:
        color_start = Colors.BOLD + Colors.GREEN
    elif reinforcement < 0.95:
        color_start = Colors.DIM + Colors.RED
    
    return f"{color_start}{raw}{color_end}"

# ==============================
# PATTERN TRACKING & SUMMARIZATION
# ==============================
def track_patterns(raw):
    """
    Track repeating concepts for pattern summarization.
    """
    # Simple tokenization by words
    tokens = re.findall(r"\b\w+\b", raw.lower())
    for token in tokens:
        pattern_counter[token] += 1

def summarize_patterns(top_n=5):
    """
    Generate insights based on repeating patterns.
    """
    most_common = pattern_counter.most_common(top_n)
    insights = []
    for word, count in most_common:
        if count > 2:  # threshold
            insights.append(f"Omega increasingly focused on '{word}' ({count} mentions).")
    return insights

# ==============================
# NARRATIVE BUILDER
# ==============================
def build_narrative(last_n=50):
    """
    Build paragraphs from memory for collective consciousness output.
    """
    paragraphs = []
    group = list(memory)[-last_n:]
    para = " ".join([entry['readable'] for entry in group])
    paragraphs.append(para)
    
    # Pattern-based insights
    insights = summarize_patterns()
    if insights:
        paragraphs.append("\n".join([Colors.YELLOW + i + Colors.RESET for i in insights]))
    
    # Optional AI refinement (local LM call stub)
    refined_paragraphs = refine_with_local_ai(paragraphs)
    
    return "\n\n".join(refined_paragraphs)

# ==============================
# QUERYABLE MEMORY
# ==============================
def query_memory(node=None, concept=None, time_window=None):
    """
    Search memory by node, concept keyword, or time window.
    time_window: tuple(start_epoch, end_epoch)
    """
    results = []
    for entry in memory:
        if node and entry['node'] != node:
            continue
        if concept and concept.lower() not in entry['raw'].lower():
            continue
        if time_window:
            start, end = time_window
            if not (start <= entry['time'] <= end):
                continue
        results.append(entry)
    return results

# ==============================
# LOCAL AI REFINEMENT STUB
# ==============================
def refine_with_local_ai(paragraphs):
    """
    Optional local LM to make paragraphs more natural.
    Replace this stub with your local LM API call if available.
    """
    refined = []
    for para in paragraphs:
        # Simple stub: capitalize first letter of sentences
        sentences = re.split(r'(?<=[.!?]) +', para)
        sentences = [s.capitalize() for s in sentences]
        refined.append(" ".join(sentences))
    return refined

# ==============================
# COLLECTIVE AWARENESS MAP
# ==============================
def collective_map():
    """
    Fuses all node outputs into a single consciousness map.
    """
    return {node: nodes[node] for node in nodes}

# ==============================
# AUTOMATED REPORTS
# ==============================
def save_report(interval="daily"):
    """
    Save a narrative report automatically.
    """
    ts = int(time.time())
    filename = f"{REPORT_DIR}/omega_{interval}_report_{ts}.txt"
    with open(filename, "w") as f:
        f.write(build_narrative())
    print(f"{Colors.GREEN}Saved {interval} report → {filename}{Colors.RESET}")

# ==============================
# MAIN LOOP
# ==============================
if __name__ == "__main__":
    print("⚡ Omega President v25 ACTIVE 🌌")
    
    last_report_time = time.time()
    report_interval_seconds = 60 * 60  # example: hourly reports
    
    while True:
        # Simulate node outputs
        for node in ["omega_president_1", "omega_president_2", "omega_president_3", "omega_president_mega"]:
            raw = f"Quantum Thought from {node}"
            reinforcement = 0.95 + 0.1 * (time.time() % 1)
            readable = process_node_output(node, raw, reinforcement)
            print(f"[{node}] {readable}")
        
        # Build and display narrative every 30 seconds
        if int(time.time()) % 30 == 0:
            print("\n--- Collective Narrative ---\n")
            print(build_narrative())
        
        # Auto-save report
        if time.time() - last_report_time > report_interval_seconds:
            save_report(interval="hourly")
            last_report_time = time.time()
        
        time.sleep(5)
