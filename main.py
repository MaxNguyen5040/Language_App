# src/main.py
import json
import csv

flashcards = []
current_language = None
dictionaries = {
    'spanish': {'hola': 'hello', 'adios': 'goodbye'},
    'french': {'bonjour': 'hello', 'au revoir': 'goodbye'}
}


def export_flashcards():
    filename = input("Enter the filename to export the flashcards to: ")
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['language', 'question', 'answer']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for flashcard in flashcards:
                writer.writerow(flashcard)
            print("Flashcards exported successfully!")
    except Exception as e:
        print(f"An error occurred while exporting flashcards: {e}")


def import_flashcards():
    global flashcards
    filename = input("Enter the filename of the CSV file to import: ")
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                flashcards.append({'language': row['language'], 'question': row['question'], 'answer': row['answer']})
            save_flashcards()
            print("Flashcards imported successfully!")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except KeyError:
        print("CSV file must contain 'language', 'question', and 'answer' columns.")

def add_flashcard():
    if not current_language:
        print("No language selected. Please select a language first.")
        return

    question = input("Enter the question: ")
    if question in dictionaries[current_language.lower()]:
        suggested_answer = dictionaries[current_language.lower()][question]
        print(f"Suggested answer: {suggested_answer}")
        answer = input("Enter the answer (or press Enter to use the suggested answer): ")
        if not answer:
            answer = suggested_answer
    else:
        answer = input("Enter the answer: ")
    
    flashcards.append({'language': current_language, 'question': question, 'answer': answer})
    save_flashcards()
   

    question = input("Enter the question: ")
    answer = input("Enter the answer: ")
    flashcards.append({'language': current_language, 'question': question, 'answer': answer})
    save_flashcards()
    print("Flashcard added!")

def edit_flashcard():
    if not flashcards:
        print("No flashcards available to edit.")
        return

    question = input("Enter the question of the flashcard you want to edit: ")
    for flashcard in flashcards:
        if flashcard['question'].lower() == question.lower() and flashcard['language'].lower() == current_language.lower():
            print(f"Current answer: {flashcard['answer']}")
            new_answer = input("Enter the new answer: ")
            flashcard['answer'] = new_answer
            save_flashcards()
            print("Flashcard updated!")
            return

    print(f"No flashcard found for question '{question}' in language '{current_language}'.")

def save_flashcards():
    with open('data/flashcards.json', 'w') as f:
        json.dump(flashcards, f)

def load_flashcards():
    global flashcards
    try:
        with open('data/flashcards.json', 'r') as f:
            flashcards = json.load(f)
    except FileNotFoundError:
        flashcards = []

def select_language():
    global current_language
    language = input("Enter the language you want to use: ")
    if language.lower() in dictionaries:
        current_language = language
        print(f"Language set to: {current_language}")
    else:
        print(f"No dictionary available for '{language}'. Please add flashcards manually.")

def start_quiz():
    if not flashcards:
        print("No flashcards available. Please add some first.")
        return
    
    if not current_language:
        print("No language selected. Please select a language first.")
        return

    filtered_flashcards = [f for f in flashcards if f['language'].lower() == current_language.lower()]
    
    if not filtered_flashcards:
        print(f"No flashcards found for language '{current_language}'")
        return
    
    score = 0
    random.shuffle(filtered_flashcards)
    for flashcard in filtered_flashcards:
        print(f"Question: {flashcard['question']}")
        answer = input("Your answer: ")
        if answer.lower() == flashcard['answer'].lower():
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. The correct answer is: {flashcard['answer']}")
    
    print(f"Quiz completed! Your score: {score}/{len(filtered_flashcards)}")

def delete_flashcard():
    if not flashcards:
        print("No flashcards available to delete.")
        return

    question = input("Enter the question of the flashcard you want to delete: ")
    for flashcard in flashcards:
        if flashcard['question'].lower() == question.lower() and flashcard['language'].lower() == current_language.lower():
            flashcards.remove(flashcard)
            save_flashcards()
            print("Flashcard deleted!")
            return

    print(f"No flashcard found for question '{question}' in language '{current_language}'.")

def review_flashcards():
    if not flashcards:
        print("No flashcards available to review.")
        return

    if not current_language:
        print("No language selected. Please select a language first.")
        return

    filtered_flashcards = [f for f in flashcards if f['language'].lower() == current_language.lower()]

    if not filtered_flashcards:
        print(f"No flashcards found for language '{current_language}'")
        return

    for flashcard in filtered_flashcards:
        print(f"Question: {flashcard['question']} - Answer: {flashcard['answer']}")

def main_menu():
    print("1. Add Flashcard")
    print("2. Quiz")
    print("3. Select Language")
    print("4. Edit Flashcard")
    print("5. Delete Flashcard")
    print("6. Review Flashcards")
    print("7. Import Flashcards")
    print("8. Export Flashcards")
    print("9. Exit")

def main():
    load_flashcards()
    while True:
        main_menu()
        choice = input("Select an option: ")
        if choice == '1':
            add_flashcard()
        elif choice == '2':
            start_quiz()
        elif choice == '3':
            select_language()
        elif choice == '4':
            edit_flashcard()
        elif choice == '5':
            delete_flashcard()
        elif choice == '6':
            review_flashcards()
        elif choice == '7':
            import_flashcards()
        elif choice == '8':
            export_flashcards()
        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")
