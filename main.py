# src/main.py
import json
import csv
from colorama import Fore, Style, init
from authentication import load_users, register_user, login_user
import hashlib

user_progress = []

init(autoreset=True)

users = []
flashcards = []
current_language = None
dictionaries = {
    'spanish': {'hola': 'hello', 'adios': 'goodbye'},
    'french': {'bonjour': 'hello', 'au revoir': 'goodbye'}
}

def load_progress():
    global user_progress
    try:
        with open(f'progress_{current_user}.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            user_progress = [row for row in reader]
    except FileNotFoundError:
        user_progress = []

def save_progress(score, total):
    try:
        with open(f'progress_{current_user}.csv', 'a', newline='') as csvfile:
            fieldnames = ['date', 'score', 'total']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'date': datetime.date.today().isoformat(), 'score': score, 'total': total})
    except Exception as e:
        print(f"An error occurred while saving progress: {e}")


def load_users():
    global users
    try:
        with open('users.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            users = [row for row in reader]
    except FileNotFoundError:
        users = []

def save_users():
    try:
        with open('users.csv', 'w', newline='') as csvfile:
            fieldnames = ['username', 'password']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user in users:
                writer.writerow(user)
    except Exception as e:
        print(f"An error occurred while saving users: {e}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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


def register_user():
    username = input("Enter a username: ")
    if any(user['username'] == username for user in users):
        print("Username already taken.")
        return
    password = input("Enter a password: ")
    users.append({'username': username, 'password': hash_password(password)})
    save_users()
    print("User registered successfully!")

def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)
    for user in users:
        if user['username'] == username and user['password'] == hashed_password:
            print("Login successful!")
            return True
    print("Invalid username or password.")
    return False

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
        print(Fore.RED + "No language selected. Please select a language first.")
        return

    question = input(Fore.GREEN + "Enter the question: ")
    if question in dictionaries[current_language.lower()]:
        suggested_answer = dictionaries[current_language.lower()][question]
        print(Fore.YELLOW + f"Suggested answer: {suggested_answer}")
        answer = input(Fore.GREEN + "Enter the answer (or press Enter to use the suggested answer): ")
        if not answer:
            answer = suggested_answer
    else:
        answer = input(Fore.GREEN + "Enter the answer: ")

    flashcards.append({'language': current_language, 'question': question, 'answer': answer, 'next_review': datetime.date.today().isoformat(), 'interval': 1})
    save_flashcards()
    print(Fore.GREEN + "Flashcard added!")

def edit_flashcard():
    if not flashcards:
        print(Fore.RED + "No flashcards available. Please add some first.")
        return
    
    if not current_language:
        print(Fore.RED + "No language selected. Please select a language first.")
        return
    
    for i, flashcard in enumerate(flashcards):
        if flashcard['language'].lower() == current_language.lower():
            print(Fore.CYAN + f"{i+1}. {flashcard['question']} - {flashcard['answer']}")
    
    try:
        index = int(input(Fore.GREEN + "Enter the number of the flashcard you want to edit: ")) - 1
        if flashcards[index]['language'].lower() != current_language.lower():
            print(Fore.RED + "Invalid selection. Please select a flashcard from the current language.")
            return
    except (ValueError, IndexError):
        print(Fore.RED + "Invalid selection. Please enter a valid number.")
        return

    new_question = input(Fore.GREEN + "Enter the new question (or press Enter to keep the current one): ")
    if not new_question:
        new_question = flashcards[index]['question']
    new_answer = input(Fore.GREEN + "Enter the new answer (or press Enter to keep the current one): ")
    if not new_answer:
        new_answer = flashcards[index]['answer']
    
    flashcards[index]['question'] = new_question
    flashcards[index]['answer'] = new_answer
    save_flashcards()
    print(Fore.GREEN + "Flashcard updated!")

def save_flashcards():
    try:
        with open(f'flashcards_{current_user}.csv', 'w', newline='') as csvfile:
            fieldnames = ['language', 'question', 'answer', 'next_review', 'interval']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for flashcard in flashcards:
                writer.writerow(flashcard)
    except Exception as e:
        print(f"An error occurred while saving flashcards: {e}")

def load_flashcards():
    global flashcards
    flashcards = []
    try:
        with open(f'flashcards_{current_user}.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                flashcards.append(row)
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
        print(Fore.RED + "No flashcards available. Please add some first.")
        return
    
    if not current_language:
        print(Fore.RED + "No language selected. Please select a language first.")
        return

    today = datetime.date.today().isoformat()
    filtered_flashcards = [f for f in flashcards if f['language'].lower() == current_language.lower() and f['next_review'] <= today]
    
    if not filtered_flashcards:
        print(Fore.RED + f"No flashcards due for review today in language '{current_language}'")
        return

    score = 0
    random.shuffle(filtered_flashcards)
    for flashcard in filtered_flashcards:
        print(Fore.BLUE + f"Question: {flashcard['question']}")
        answer = input(Fore.GREEN + "Your answer: ")
        if answer.lower() == flashcard['answer'].lower():
            print(Fore.GREEN + "Correct!")
            score += 1
            flashcard['interval'] *= 2
        else:
            print(Fore.RED + f"Wrong. The correct answer is: {flashcard['answer']}")
            flashcard['interval'] = 1
        flashcard['next_review'] = (datetime.date.today() + datetime.timedelta(days=flashcard['interval'])).isoformat()

    save_flashcards()
    save_progress(score, len(filtered_flashcards))
    print(Fore.GREEN + f"Quiz completed! Your score: {score}/{len(filtered_flashcards)}")

def delete_flashcard():
    if not flashcards:
        print(Fore.RED + "No flashcards available. Please add some first.")
        return
    
    if not current_language:
        print(Fore.RED + "No language selected. Please select a language first.")
        return
    
    for i, flashcard in enumerate(flashcards):
        if flashcard['language'].lower() == current_language.lower():
            print(Fore.CYAN + f"{i+1}. {flashcard['question']} - {flashcard['answer']}")
    
    try:
        index = int(input(Fore.GREEN + "Enter the number of the flashcard you want to delete: ")) - 1
        if flashcards[index]['language'].lower() != current_language.lower():
            print(Fore.RED + "Invalid selection. Please select a flashcard from the current language.")
            return
    except (ValueError, IndexError):
        print(Fore.RED + "Invalid selection. Please enter a valid number.")
        return
    
    confirmation = input(Fore.RED + "Are you sure you want to delete this flashcard? (y/n): ").lower()
    if confirmation == 'y':
        flashcards.pop(index)
        save_flashcards()
        print(Fore.GREEN + "Flashcard deleted!")
    else:
        print(Fore.YELLOW + "Flashcard deletion cancelled.")

def review_flashcards():
    if not flashcards:
        print(Fore.RED + "No flashcards available. Please add some first.")
        return
    
    print(Fore.CYAN + "Available languages:")
    languages = list(set(flashcard['language'].lower() for flashcard in flashcards))
    for i, language in enumerate(languages):
        print(Fore.CYAN + f"{i+1}. {language}")
    
    try:
        language_index = int(input(Fore.GREEN + "Select a language to review: ")) - 1
        selected_language = languages[language_index]
    except (ValueError, IndexError):
        print(Fore.RED + "Invalid selection. Please enter a valid number.")
        return
    
    filtered_flashcards = [f for f in flashcards if f['language'].lower() == selected_language]
    
    if not filtered_flashcards:
        print(Fore.RED + f"No flashcards available in language '{selected_language}'")
        return

    random.shuffle(filtered_flashcards)
    for flashcard in filtered_flashcards:
        print(Fore.BLUE + f"Question: {flashcard['question']}")
        input(Fore.GREEN + "Press Enter to reveal the answer...")
        print(Fore.GREEN + f"Answer: {flashcard['answer']}")
        input(Fore.YELLOW + "Press Enter to continue...")

    print(Fore.GREEN + "Flashcard review completed!")

def generate_example_flashcards(filename):
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['language', 'question', 'answer']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for flashcard in example_flashcards:
                writer.writerow(flashcard)
            print(f"Example flashcards saved to {filename}")
    except Exception as e:
        print(f"An error occurred while generating example flashcards: {e}")

def view_progress():
    if not user_progress:
        print(Fore.RED + "No progress available.")
        return
    
    print(Fore.CYAN + "Date       | Score | Total")
    print(Fore.CYAN + "-----------|-------|------")
    for entry in user_progress:
        print(Fore.CYAN + f"{entry['date']} | {entry['score']}    | {entry['total']}")


def main_menu():
    print(Fore.CYAN + "1. Add Flashcard")
    print(Fore.CYAN + "2. Quiz")
    print(Fore.CYAN + "3. Select Language")
    print(Fore.CYAN + "4. Edit Flashcard")
    print(Fore.CYAN + "5. Delete Flashcard")
    print(Fore.CYAN + "6. Review Flashcards")
    print(Fore.CYAN + "7. Import Flashcards")
    print(Fore.CYAN + "8. Export Flashcards")
    print(Fore.CYAN + "9. View Progress")
    print(Fore.CYAN + "10. Logout")

def main():
    load_users()
    global current_user
    while not current_user:
        print(Fore.CYAN + "1. Register")
        print(Fore.CYAN + "2. Login")
        choice = input(Fore.CYAN + "Select an option: ")
        if choice == '1':
            register_user()
        elif choice == '2':
            if login_user():
                current_user = input("Enter your username again to confirm: ")
        else:
            print(Fore.RED + "Invalid choice, please try again.")

    load_flashcards()
    load_progress()
    while True:
        main_menu()
        choice = input(Fore.CYAN + "Select an option: ")
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
            view_progress()
        elif choice == '10':
            current_user = None
            break
        else:
            print(Fore.RED + "Invalid choice, please try again.")
