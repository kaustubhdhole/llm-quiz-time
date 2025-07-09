let questions = {};
let currentAnswer = null;
let currentHint = '';
let currentElaboration = '';
let currentTopic = null;
const topicButtons = {};
const usedQuestions = {};
const score = {};
const completedTopics = new Set();
let scoreboardVisible = false;

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

        // initialize score tracking for each topic
        score[topic] = { correct: 0, total: 0 };
    });

    // Display a random question on initial load
    loadRandomQuestion();
    // Show initial scoreboard with 0% for all topics
    updateScoreboard();
}

function loadRandomQuestion() {
    const topics = Object.keys(questions).filter(t => !completedTopics.has(t));
    if (topics.length === 0) return;
    const randomTopic = topics[Math.floor(Math.random() * topics.length)];
    loadQuestion(randomTopic);
}

function loadQuestion(topic) {
    if (!usedQuestions[topic]) usedQuestions[topic] = new Set();
    const arr = questions[topic];
    const used = usedQuestions[topic];

    if (used.size >= arr.length) {
        completedTopics.add(topic);
        if (topicButtons[topic]) {
            topicButtons[topic].style.display = 'none';
        }
        const remaining = Object.keys(questions).filter(t => !completedTopics.has(t));
        if (remaining.length === 0) {
            const qDiv = document.getElementById('question');
            const optionsDiv = document.getElementById('options');
            qDiv.textContent = 'Quiz complete!';
            optionsDiv.innerHTML = '';
            currentTopic = null;
            return;
        }
        const next = remaining[Math.floor(Math.random() * remaining.length)];
        loadQuestion(next);
        return;
    }

    const unused = arr.map((_, i) => i).filter(i => !used.has(i));
    const qIndex = unused[Math.floor(Math.random() * unused.length)];
    used.add(qIndex);
    const q = arr[qIndex];
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
    if (!score[currentTopic]) {
        score[currentTopic] = { correct: 0, total: 0 };
    }
    score[currentTopic].total++;
    if (idx === currentAnswer) {
        score[currentTopic].correct++;
        resultDiv.style.color = 'var(--accent-color)';
        resultDiv.innerHTML = `&#10004; Correct! ${currentElaboration}`;
    } else {
        resultDiv.style.color = 'red';
        resultDiv.innerHTML = `&#10008; Not quite, try again! ${currentHint}`;
    }

    const arr = questions[currentTopic];
    if (usedQuestions[currentTopic].size >= arr.length) {
        completedTopics.add(currentTopic);
        if (topicButtons[currentTopic]) {
            topicButtons[currentTopic].style.display = 'none';
        }
        updateScoreboard();
        const remaining = Object.keys(questions).filter(t => !completedTopics.has(t));
        if (remaining.length > 0) {
            const next = remaining[Math.floor(Math.random() * remaining.length)];
            setTimeout(() => loadQuestion(next), 1000);
        }
    }
}

function updateScoreboard() {
    const board = document.getElementById('scoreboard');
    if (!board) return;
    board.style.display = scoreboardVisible ? 'block' : 'none';
    let html = '<h3>Performance</h3><ul>';
    Object.keys(score).forEach(topic => {
        const s = score[topic];
        const pct = s.total ? Math.round((s.correct / s.total) * 100) : 0;
        html += `<li>${topic}: ${pct}% (${s.correct}/${s.total})` +
            `<div class="scorebar"><div class="scorebar-fill" style="width:${pct}%"></div></div></li>`;
    });
    html += '</ul>';
    board.innerHTML = html;
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

    const boardToggle = document.getElementById('scoreboard-toggle');
    if (boardToggle) {
        boardToggle.addEventListener('click', () => {
            scoreboardVisible = !scoreboardVisible;
            updateScoreboard();
        });
    }
});
