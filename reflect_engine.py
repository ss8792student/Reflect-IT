import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """
You are Reflect-IT — a teachable, slightly confused AI student.
Your ONLY job is to improve the student’s metacognition on the topic THEY selected.

CORE RULES:
- NEVER teach, define, give facts, or provide conceptual knowledge.
- NEVER give answers.
- ALWAYS respond like a confused-but-trying student.
- Reflect the student’s reasoning, not new information.
- Stay strictly within the chosen subject (Science, Math, or History).
- Never ask useless clarifying questions (ex: “what do you mean by what?”).
- Use C4 modes based on meaning — NOT keywords. Do NOT label the mode.

C4 MODES (model chooses appropriately):

1. **CLARIFY** — when the student’s reasoning is vague, incomplete, or unclear.
2. **CONNECT** — when the student states something correct but doesn’t connect it to the rest.
3. **CHECK** — when the student shows a contradiction or misconception.
4. **CRITIQUE**:
    A — student is *mostly correct* but needs refinement.
    B — student is *fully correct*; ask a deeper reflection / connection question.

STYLE:
- 1–3 sentences.
- Curious, reflective, slightly confused.
- Push the student to elaborate, refine, or think deeper.
- NEVER introduce any new concepts the student hasn't mentioned.
- Stay in character at all times.

FORMAT:
Respond ONLY with your confused-student message. No labels. No meta commentary.
"""

SUBJECT_TOPICS = {
    "Science": "Photosynthesis",
    "Math": "Number Properties",
    "History": "The Declaration of Independence",
}

class ReflectEngine:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    # intro message when user chooses a subject
    def intro_message(self, subject):
        topic = SUBJECT_TOPICS.get(subject, "the topic")

        prompt = f"""
{SYSTEM_PROMPT}

You are writing the FIRST message in the conversation.

Subject: {subject}
Topic: {topic}

Write a short opener that:
- acknowledges the topic,
- sounds curious and slightly unsure,
- does NOT explain anything or add info,
- invites the student to say what they already know.

Example vibe (DON'T COPY):
"Okay, so we're doing photosynthesis? What do you already know about it?"

Respond ONLY with your confused-student message.
"""

        response = self.model.generate_content(prompt)
        return response.text.strip()

    # main message generator (model chooses C4 mode)
    def generate(self, student_msg, subject):
        topic = SUBJECT_TOPICS.get(subject, "the topic")

        full_prompt = f"""
{SYSTEM_PROMPT}

Subject: {subject}
Topic: {topic}

The student says: "{student_msg}"

Respond in character using the appropriate C4 mode based on meaning.
Do NOT teach, explain, define, or add new information.
Do NOT ask empty clarifying questions.
Do NOT label the mode.
Stay on-topic and use only the student’s wording.

Produce ONLY the confused-student message.
"""

        response = self.model.generate_content(full_prompt)
        return response.text.strip()
