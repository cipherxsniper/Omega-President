#!/bin/bash
# Mini-Omega Supervisor launcher (Termux persistent)
cd ~/Omega-President

# Run supervisor in background, redirect stdout and stderr
nohup python3 mini_omega_supervisor.py > logs/mini_omega_supervisor.log 2>&1 &
echo "Mini-Omega Supervisor started with PID $!"
