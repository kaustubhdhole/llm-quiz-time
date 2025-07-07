async function loadQuestion() {
    const res = await fetch('questions.json');
    const data = await res.json();
    const q = data[Math.floor(Math.random() * data.length)];
    const questionDiv = document.getElementById('question');
    const optionsDiv = document.getElementById('options');

    questionDiv.textContent = q.question;
    optionsDiv.innerHTML = '';
    q.options.forEach(opt => {
        const div = document.createElement('div');
        div.className = 'option';
        div.textContent = opt;
        optionsDiv.appendChild(div);
    });
}

window.addEventListener('DOMContentLoaded', loadQuestion);
