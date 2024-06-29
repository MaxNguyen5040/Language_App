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
    print("Start Quiz")

def select_language():
    print("Select Language")

if __name__ == "__main__":
    main()
