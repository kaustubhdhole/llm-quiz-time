let questions = {};
let currentAnswer = null;
let currentHint = '';
let currentElaboration = '';
let currentTopic = null;
const topicButtons = {};

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
        toggle.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

async function loadData() {
    const res = await fetch('questions.json');
    questions = await res.json();
    const topicsDiv = document.getElementById('topics');
    Object.keys(questions).forEach(topic => {
        const btn = document.createElement('div');
        btn.className = 'topic';
        btn.textContent = topic;
        btn.addEventListener('click', () => loadQuestion(topic));
        topicButtons[topic] = btn;
        topicsDiv.appendChild(btn);
    });

    // Display a random question on initial load
    loadRandomQuestion();
}

function loadRandomQuestion() {
    const topics = Object.keys(questions);
    if (topics.length === 0) return;
    const randomTopic = topics[Math.floor(Math.random() * topics.length)];
    loadQuestion(randomTopic);
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
    currentHint = q.hint || '';
    currentElaboration = q.elaboration || '';
    if (currentTopic && topicButtons[currentTopic]) {
        topicButtons[currentTopic].classList.remove('active');
    }
    currentTopic = topic;
    if (topicButtons[currentTopic]) {
        topicButtons[currentTopic].classList.add('active');
    }

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
        resultDiv.style.color = 'var(--accent-color)';
        resultDiv.innerHTML = `&#10004; Correct! ${currentElaboration}`;
    } else {
        resultDiv.style.color = 'red';
        resultDiv.innerHTML = `&#10008; Not quite, try again! ${currentHint}`;
    }
}

window.addEventListener('DOMContentLoaded', () => {
    loadData();
    const storedTheme = localStorage.getItem('theme') || 'dark';
    applyTheme(storedTheme);
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
            applyTheme(current);
        });
    }
    const refresh = document.getElementById('refresh-btn');
    if (refresh) {
        refresh.addEventListener('click', () => {
            if (currentTopic) {
                loadQuestion(currentTopic);
            } else {
                loadRandomQuestion();
            }
        });
    }
});
