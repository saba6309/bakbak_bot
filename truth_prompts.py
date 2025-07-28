import random

TRUTHS = [
    "What is your biggest secret?",
    "Who is your best friend?",
    "Describe your happiest moment.",
    "What’s a funny story from your life?",
    "What’s a local word/slang you use a lot?",
]

def get_truth_prompt():
    return random.choice(TRUTHS)

def handle_truth(question, answer):
    return {"question": question, "answer": answer}