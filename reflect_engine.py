import re
from openai import OpenAI
from prompts import SYSTEM_PROMPT
from dotenv import load_dotenv
import os

load_dotenv() # loads .env

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ReflectEngine:
    def __init__(self):
        pass

    def detect_trigger(self, student_msg):
        msg = student_msg.lower()

        # uncertainty / confusion triggers Mirror
        if any(word in msg for word in ["not sure", "idk", "don't know", "maybe", "?"]):
            return "mirror"

        # if partially correct → Probe
        if any(word in msg for word in ["i think", "probably", "maybe", "kind of"]):
            return "probe"

        # incorrect factual patterns → Socratic
        if re.search(r"(wrong pattern regex later)", msg):
            return "socratic"

        # if message is confident + correct → Reinforce
        return "reinforce"

    def build_prompt(self, trigger, student_msg):
        return f"""
{SYSTEM_PROMPT}

Trigger chosen: {trigger}
Student message: {student_msg}

Respond ONLY using the rules for this trigger.
"""

    def generate(self, student_msg):
        trigger = self.detect_trigger(student_msg)
        prompt = self.build_prompt(trigger, student_msg)

        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )

        return result.choices[0].message.content, trigger
