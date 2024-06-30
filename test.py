import json
from datetime import datetime, timedelta
import random

flashcards = [
    {"language": "Spanish", "question": "Hello", "answer": "Hola"},
    {"language": "Spanish", "question": "Goodbye", "answer": "Adiós"},
    {"language": "Spanish", "question": "Please", "answer": "Por favor"},
    {"language": "Spanish", "question": "Thank you", "answer": "Gracias"},
    {"language": "Spanish", "question": "Yes", "answer": "Sí"},
    {"language": "Spanish", "question": "No", "answer": "No"},
    {"language": "Spanish", "question": "Good morning", "answer": "Buenos días"},
    {"language": "Spanish", "question": "Good night", "answer": "Buenas noches"},
    {"language": "Spanish", "question": "How are you?", "answer": "¿Cómo estás?"},
    {"language": "Spanish", "question": "I love you", "answer": "Te quiero"}
]

# Simulate user progress
progress = []
start_time = datetime.now() - timedelta(days=1)
for i in range(60):  # Simulate 60 minutes of activity
    flashcard = random.choice(flashcards)
    user_answer_correct = random.choice([True, False])
    progress.append({
        "date": (start_time + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M'),
        "score": 1 if user_answer_correct else 0,
        "total": 1
    })

# Save to local storage simulation (JSON file)
with open('flashcards.json', 'w') as f:
    json.dump(flashcards, f)

with open('progress.json', 'w') as f:
    json.dump(progress, f)

print("Flashcards and progress data generated.")