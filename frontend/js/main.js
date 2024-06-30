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


function loadQuiz() {
    const flashcards = JSON.parse(localStorage.getItem('flashcards')) || [];
    if (flashcards.length === 0) {
        document.getElementById('quiz-container').innerHTML = '<p>No flashcards available.</p>';
        return;
    }
    const flashcard = flashcards[Math.floor(Math.random() * flashcards.length)];
    document.getElementById('question').innerText = flashcard.question;
    document.getElementById('question').dataset.answer = flashcard.answer;
}

function checkAnswer() {
    const userAnswer = document.getElementById('user-answer').value;
    const correctAnswer = document.getElementById('question').dataset.answer;
    if (userAnswer.toLowerCase() === correctAnswer.toLowerCase()) {
        document.getElementById('result').innerText = 'Correct!';
    } else {
        document.getElementById('result').innerText = `Incorrect. The correct answer was: ${correctAnswer}`;
    }
    document.getElementById('user-answer').value = '';
    loadQuiz();
}

if (window.location.pathname.endsWith('quiz.html')) {
    loadQuiz();
}