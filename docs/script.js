const API = window.location.origin;
let gameId = null;

const guessInput = document.getElementById('guessInput');
const guessBtn = document.getElementById('guessBtn');
const newGameBtn = document.getElementById('newGameBtn');
const feedback = document.getElementById('feedback');
const attempts = document.getElementById('attempts');
const historyList = document.getElementById('historyList');
const alert = document.getElementById('alert');

function showAlert(msg) {
  alert.textContent = msg;
  alert.classList.remove('hidden');
  setTimeout(() => alert.classList.add('hidden'), 3000);
}

function setFeedback(text, type) {
  feedback.textContent = text;
  feedback.className = 'feedback ' + (type || '');
  if (type) feedback.classList.remove('hidden');
  else feedback.classList.add('hidden');
}

function hintClass(hint) {
  return hint === 'Burning hot!' ? 'hint-hot'
    : hint === 'Very close' || hint === 'Close' ? ''
    : hint === 'Warm' ? 'hint-warm'
    : '';
}

function addHistory(num, result, correct) {
  const li = document.createElement('li');
  li.className = 'history-item';
  if (correct) {
    li.innerHTML = `<span class="num">${num}</span><span class="result-correct">Correct!</span>`;
  } else {
    const cls = hintClass(result);
    li.innerHTML = `<span class="num">${num}</span><span class="hint ${cls}">${result}</span>`;
  }
  historyList.appendChild(li);
  historyList.scrollTop = historyList.scrollHeight;
}

function enableGame() {
  guessInput.disabled = false;
  guessBtn.disabled = false;
  guessInput.focus();
}

function disableGame() {
  guessInput.disabled = true;
  guessBtn.disabled = true;
}

async function newGame() {
  try {
    const res = await fetch(`${API}/new-game`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to start game');
    const data = await res.json();
    gameId = data.game_id;
    setFeedback('', '');
    attempts.textContent = '0';
    historyList.innerHTML = '';
    guessInput.value = '';
    enableGame();
    guessInput.focus();
    showAlert('New game started!');
  } catch (e) {
    showAlert('Error: ' + e.message);
  }
}

async function makeGuess() {
  const val = parseInt(guessInput.value, 10);
  if (isNaN(val) || val < 1 || val > 100) {
    showAlert('Enter a number between 1 and 100');
    return;
  }
  guessBtn.disabled = true;
  try {
    const res = await fetch(`${API}/guess`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ game_id: gameId, number: val }),
    });
    const data = await res.json();
    if (!res.ok) {
      showAlert(data.detail || 'Error');
      disableGame();
      return;
    }
    attempts.textContent = data.attempts;

    let feedbackText, feedbackType;
    if (data.result === 'correct') {
      feedbackText = `Correct! The number was ${data.secret}. You got it in ${data.attempts} ${data.attempts === 1 ? 'try' : 'tries'}!`;
      feedbackType = 'correct';
      disableGame();
    } else {
      feedbackText = data.hint;
      feedbackType = data.hint === 'Burning hot!' ? 'hot'
        : data.hint === 'Very close' || data.hint === 'Close' ? 'close'
        : data.hint === 'Warm' ? 'warm'
        : data.hint === 'Cool' ? 'cool'
        : data.hint === 'Cold' ? 'cold'
        : 'freezing';
      guessInput.value = '';
      guessInput.focus();
    }
    setFeedback(feedbackText, feedbackType);
    addHistory(val, data.hint || data.result, data.result === 'correct');
  } catch (e) {
    showAlert('Error: ' + e.message);
  } finally {
    guessBtn.disabled = !gameId || guessInput.disabled;
  }
}

newGameBtn.addEventListener('click', newGame);
guessBtn.addEventListener('click', makeGuess);
guessInput.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !guessBtn.disabled) makeGuess(); });
