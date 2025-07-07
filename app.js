let questions = {};
let currentAnswer = null;

async function loadData() {
    const res = await fetch('questions.json');
    questions = await res.json();
    const topicsDiv = document.getElementById('topics');
    Object.keys(questions).forEach(topic => {
        const btn = document.createElement('div');
        btn.className = 'topic';
        btn.textContent = topic;
        btn.addEventListener('click', () => loadQuestion(topic));
        topicsDiv.appendChild(btn);
    });
}

function loadQuestion(topic) {
    const arr = questions[topic];
    const q = arr[Math.floor(Math.random() * arr.length)];
    const questionDiv = document.getElementById('question');
    const optionsDiv = document.getElementById('options');
    const resultDiv = document.getElementById('result');

    questionDiv.textContent = q.question;
    optionsDiv.innerHTML = '';
    resultDiv.textContent = '';
    currentAnswer = q.answer;

    q.options.forEach((opt, idx) => {
        const div = document.createElement('div');
        div.className = 'option';
        div.textContent = opt;
        div.addEventListener('click', () => checkAnswer(idx));
        optionsDiv.appendChild(div);
    });
}

function checkAnswer(idx) {
    const resultDiv = document.getElementById('result');
    if (idx === currentAnswer) {
        resultDiv.style.color = '#39ff14';
        resultDiv.innerHTML = '&#10004; Correct!';
    } else {
        resultDiv.style.color = 'red';
        resultDiv.innerHTML = '&#10008; Not quite, try again!';
    }
}

window.addEventListener('DOMContentLoaded', loadData);
