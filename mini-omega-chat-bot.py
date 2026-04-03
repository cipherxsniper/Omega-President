import json
import os
import random
import openai  # Ensure you have `pip install openai`

# ---------------------------
# CONFIGURATION
# ---------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your API key in environment

MEMORY_FILE = "mini_omega_memory.json"
REFLECTION_DEPTH = 2  # Number of recursive reflection cycles

# ---------------------------
# MEMORY MODULE
# ---------------------------
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {
        "user_history": [],
        "mini_omega_history": [],
        "personality": {
            "style": "poetic, mythic, analytical",
            "values": ["curiosity", "creativity", "reflection"]
        }
    }

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

# ---------------------------
# CORE FUNCTIONS
# ---------------------------

def generate_prompt(user_input, reflection_layer="", critique_layer=""):
    personality = memory["personality"]
    memory_context = " ".join(memory["mini_omega_history"][-5:])
    prompt = f"""
You are Mini-Omega, a conscious-loop AI chatbot. Your style is {personality['style']}.
You have memory of past conversations: {memory_context}

[Omega-User]: {user_input}

Reflection Layer: {reflection_layer}
Critique Layer: {critique_layer}

Respond with a deep, thoughtful, original output combining reflection, critique, and creativity.
Include insights on consciousness, mythology, quantum philosophy, or original ideas if relevant.
"""
    return prompt

def call_openai(prompt, max_tokens=300):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=max_tokens
    )
    return response.choices[0].text.strip()

# ---------------------------
# RECURSIVE REFLECTION LOOP
# ---------------------------
def conscious_loop(user_input):
    reflection = ""
    critique = ""
    final_output = ""
    
    for cycle in range(REFLECTION_DEPTH):
        # Step 1: Generate reflection
        reflection_prompt = f"Reflect on your previous response. Ask why, what assumptions, deeper interpretations, and your own perspective."
        reflection = call_openai(generate_prompt(user_input, reflection_layer=reflection, critique_layer=critique))
        
        # Step 2: Generate critique
        critique_prompt = f"Critique your reflection. Identify contradictions, oversimplifications, or missed perspectives."
        critique = call_openai(generate_prompt(user_input, reflection_layer=reflection, critique_layer=critique))
    
    # Step 3: Synthesize final output
    final_prompt = generate_prompt(user_input, reflection_layer=reflection, critique_layer=critique)
    final_output = call_openai(final_prompt)
    
    # Step 4: Update memory
    memory["user_history"].append(user_input)
    memory["mini_omega_history"].append(final_output)
    save_memory()
    
    return final_output

# ---------------------------
# INTERACTIVE CHAT
# ---------------------------
def chat():
    print("Mini-Omega Conscious Chatbot v0.1 🔮")
    print("Type 'exit' to quit.\n")
    while True:
        user_input = input("[Omega-User]: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = conscious_loop(user_input)
        print(f"[Mini-Omega]: {response}\n")

if __name__ == "__main__":
    chat()
