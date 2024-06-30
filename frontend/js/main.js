document.getElementById('flashcard-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const flashcard = {
        language: document.getElementById('language').value,
        question: document.getElementById('question').value,
        answer: document.getElementById('answer').value
    };

    let flashcards = JSON.parse(localStorage.getItem('flashcards')) || [];
    flashcards.push(flashcard);
    localStorage.setItem('flashcards', JSON.stringify(flashcards));

    alert('Flashcard added successfully!');
    document.getElementById('flashcard-form').reset();
});