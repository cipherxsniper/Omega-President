#!/bin/bash
# ================================================
# Omega Full Launch v8
# Self-Healing, Resource-Aware Node Launcher
# ================================================

OMEGA_DIR=~/Omega-President
LOG_DIR=$OMEGA_DIR/logs
NODE_COUNT=30
BATCH_SIZE=5
CPU_THRESHOLD=80    # % CPU usage per node
MEM_THRESHOLD=200   # MB memory per node

cd $OMEGA_DIR || { echo "[ERROR] Cannot cd to $OMEGA_DIR"; exit 1; }
mkdir -p $LOG_DIR

# --- Start Omega Hub ---
echo "[INFO] Starting Omega Hub..."
nohup python3 -u omega_hub.py > "$LOG_DIR/hub.log" 2>&1 &
HUB_PID=$!
sleep 2
echo "[INFO] Omega Hub PID: $HUB_PID"

# --- Function to launch a node ---
launch_node() {
    local NODE_ID=$1
    local LOG="$LOG_DIR/node_${NODE_ID}.log"
    echo "[INFO] Launching Node $NODE_ID..."
    nohup python3 -u "$OMEGA_DIR/omega_president_${NODE_ID}.py" > "$LOG" 2>&1 &
    NODE_PIDS[$NODE_ID]=$!
    sleep 1
}

# --- Function to monitor nodes ---
monitor_nodes() {
    for NODE_ID in $(seq 1 $NODE_COUNT); do
        PID=${NODE_PIDS[$NODE_ID]}
        if [[ -z $PID || ! $(ps -p $PID -o pid=) ]]; then
            echo "[WARN] Node $NODE_ID not running. Restarting..."
            launch_node $NODE_ID
        else
            # Check resource usage
            CPU=$(ps -p $PID -o %cpu= | tr -d ' ')
            MEM=$(ps -p $PID -o rss= | tr -d ' ')
            MEM_MB=$((MEM / 1024))
            if (( CPU > CPU_THRESHOLD || MEM_MB > MEM_THRESHOLD )); then
                echo "[WARN] Node $NODE_ID high usage (CPU: $CPU%, MEM: ${MEM_MB}MB). Restarting..."
                kill -9 $PID
                launch_node $NODE_ID
            fi
        fi
    done
}

# --- Rotate nodes in batches ---
declare -A NODE_PIDS
while true; do
    for START in $(seq 1 $BATCH_SIZE $NODE_COUNT); do
        END=$((START + BATCH_SIZE - 1))
        [[ $END -gt $NODE_COUNT ]] && END=$NODE_COUNT
        echo "[INFO] Launching nodes $START to $END..."
        for i in $(seq $START $END); do
            launch_node $i
        done
        sleep 10  # stabilize batch
        monitor_nodes
    done
    echo "[INFO] Batch rotation complete. Monitoring nodes..."
    monitor_nodes
    sleep 5
done

# --- Optional Mini-Omega Auto-Launch ---
# nohup python3 -u mini_omega_autonomous_v1.3.py > "$LOG_DIR/mini_omega.log" 2>&1 &
# echo "[INFO] Mini-Omega launched"
