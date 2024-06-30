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

function loadProgress() {
    const progress = JSON.parse(localStorage.getItem('progress')) || [];
    const tableBody = document.getElementById('progress-table').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
    progress.forEach(entry => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${entry.date}</td><td>${entry.score}</td><td>${entry.total}</td>`;
        tableBody.appendChild(row);
    });
}

if (window.location.pathname.endsWith('view_progress.html')) {
    loadProgress();
}

function loadExampleProgress() {
    fetch('progress.json')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('progress-table').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = '';
            data.forEach(entry => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${entry.date}</td><td>${entry.score}</td><td>${entry.total}</td>`;
                tableBody.appendChild(row);
            });
        });
}

if (window.location.pathname.endsWith('view_progress.html')) {
    loadExampleProgress();
}



document.addEventListener('DOMContentLoaded', () => {
    const progressData = [
        { date: '2024-06-24 10:00', language: 'Spanish', score: 7, total: 10 },
        { date: '2024-06-24 10:15', language: 'French', score: 8, total: 10 },
        { date: '2024-06-24 10:30', language: 'German', score: 9, total: 10 },
        { date: '2024-06-24 10:45', language: 'Spanish', score: 6, total: 10 },
        { date: '2024-06-24 11:00', language: 'French', score: 8, total: 10 },
        { date: '2024-06-24 11:15', language: 'German', score: 23, total: 25 },
        { date: '2024-06-24 11:30', language: 'Spanish', score: 19, total: 20 },
        { date: '2024-06-24 11:45', language: 'French', score: 22, total: 25 },
    ];

    const summaryData = {};

    progressData.forEach(entry => {
        if (!summaryData[entry.language]) {
            summaryData[entry.language] = { totalScore: 0, totalEntries: 0, totalPossible: 0 };
        }
        summaryData[entry.language].totalScore += entry.score;
        summaryData[entry.language].totalEntries += 1;
        summaryData[entry.language].totalPossible += entry.total;
    });

    const tableBody = document.getElementById('summary-table').getElementsByTagName('tbody')[0];

    Object.keys(summaryData).forEach(language => {
        const row = document.createElement('tr');
        const totalScore = summaryData[language].totalScore;
        const totalEntries = summaryData[language].totalEntries;
        const totalPossible = summaryData[language].totalPossible;
        const averageScore = (totalScore / totalPossible) * 100;

        row.innerHTML = `
            <td>${language}</td>
            <td>${totalScore} / ${totalPossible}</td>
            <td>${averageScore.toFixed(2)}%</td>
        `;
        tableBody.appendChild(row);
    });
});