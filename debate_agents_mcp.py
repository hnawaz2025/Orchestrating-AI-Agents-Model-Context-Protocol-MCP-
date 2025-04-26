# debate_agents_mcp.py

import openai
import time
import os 
from dotenv import load_dotenv
from groq import Groq
load_dotenv('environment.env')

# --- CONFIGURATION ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# --- MESSAGE CLASS ---
class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content

# Debate Topic
DEBATE_TOPIC = "Should governments regulate AI development?"

# --- UTILITY FUNCTION TO CALL LLM ---

def call_llm(prompt, temperature=0.7):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,)
    return response.choices[0].message.content.strip()

# --- AGENT DEFINITION ---

class DebateAgent:
    def __init__(self, name, stance):
        self.name = name
        self.stance = stance

    def receive(self, incoming_message):
        context = incoming_message.content
        reply = self.generate_reply(context)
        return Message(sender=self.name, content=reply)

    def generate_reply(self, context):
        prompt = (
            f"You are {self.name}, participating in a debate.\n"
            f"Your stance is: {self.stance}\n\n"
            f"Here is what your opponent said:\n{context}\n\n"
            f"Craft your reply in a formal debate tone. "
            f"If it's your first turn, make an opening argument.\n"
            f"If it's a second turn, rebut the opponent's points.\n"
            f"If it's the final turn, give a closing statement."
        )
        response = call_llm(prompt)
        return response

# --- ORCHESTRATOR FUNCTION ---

def run_debate():
    # Initialize Agents
    agent_pro = DebateAgent(name="Agent Pro", stance="In favor of government regulation of AI")
    agent_con = DebateAgent(name="Agent Con", stance="Against government regulation of AI")
    
    # Turn 1: Pro Opening
    print("\n--- TURN 1: Pro Opening ---")
    pro_opening = agent_pro.generate_reply(DEBATE_TOPIC)
    print(f"[Agent Pro]: {pro_opening}\n")
    message_to_con = Message(sender=agent_pro.name, content=pro_opening)
    time.sleep(1)

    # Turn 2: Con Opening
    print("--- TURN 2: Con Response ---")
    message_from_con = agent_con.receive(message_to_con)
    print(f"[Agent Con]: {message_from_con.content}\n")
    time.sleep(1)

    # Turn 3: Pro Rebuttal
    print("--- TURN 3: Pro Rebuttal ---")
    message_from_pro = agent_pro.receive(message_from_con)
    print(f"[Agent Pro]: {message_from_pro.content}\n")
    time.sleep(1)

    # Turn 4: Con Rebuttal
    print("--- TURN 4: Con Rebuttal ---")
    message_from_con_2 = agent_con.receive(message_from_pro)
    print(f"[Agent Con]: {message_from_con_2.content}\n")
    time.sleep(1)

    # Turn 5: Pro Closing
    print("--- TURN 5: Pro Closing Statement ---")
    pro_closing = agent_pro.generate_reply("Please give your final closing statement for the debate.")
    print(f"[Agent Pro]: {pro_closing}\n")
    time.sleep(1)

    # Turn 6: Con Closing
    print("--- TURN 6: Con Closing Statement ---")
    con_closing = agent_con.generate_reply("Please give your final closing statement for the debate.")
    print(f"[Agent Con]: {con_closing}\n")

# --- RUN THE DEBATE ---

if __name__ == "__main__":
    run_debate()
