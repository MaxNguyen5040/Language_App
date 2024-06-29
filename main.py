current_language = None

def main_menu():
    print("1. Add Flashcard")
    print("2. Quiz")
    print("3. Select Language")
    print("4. Exit")

def main():
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
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

def add_flashcard():
    print("Add Flashcard")

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
            print("Correct!!!")
            score += 1
        else:
            print(f"Wrong. The correct answer is: {flashcard['answer']}")
    
    print(f"Quiz completed! Your score: {score}/{len(filtered_flashcards)}")

def select_language():
    global current_language
    language = input("Enter the language you want to use: ")
    current_language = language
    print(f"Language set to: {current_language}")


main()