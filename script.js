// This file contains the JavaScript code for the game interface

const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const aiToggleBtn = document.getElementById('ai-toggle');
const winsElement = document.getElementById('wins');
const lossesElement = document.getElementById('losses');
const rewardElement = document.getElementById('reward');

// Set canvas dimensions (adjust as needed to match your game dimensions)
canvas.width = 800;
canvas.height = 500;

// Initialize game state
let gameImage = new Image();
let isAIEnabled = false;
let totalReward = 0;
let wins = 0;
let losses = 0;

// Render the game state
function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(gameImage, 0, 0, canvas.width, canvas.height);
}

// Handle user input
function handleKeydown(event) {
  let action;
  if (event.key === 'ArrowUp') {
    action = 0; // Take action 0 (thrust)
  } else if (event.key === 'ArrowLeft') {
    action = 1; // Take action 1 (rotate left)
  } else if (event.key === 'ArrowRight') {
    action = 2; // Take action 2 (rotate right)
  } else if (event.key === 'r' || event.key === 'R') {
    resetGame();
    return;
  }

  if (action !== undefined) {
    takeAction(action);
  }
}

// Handle AI toggle
aiToggleBtn.addEventListener('click', () => {
  isAIEnabled = !isAIEnabled;
  if (isAIEnabled) {
    aiPlay();
  }
});

function resetGame() {
  fetch('/new_game')
    .then(response => response.json())
    .then((data) => {
      gameImage.src = `data:image/png;base64,${data.image}`;
      gameImage.onload = () => {
        render();
      };
    });
}

function takeAction(action) {
  fetch('/step', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action: action })
  })
    .then(response => response.json())
    .then((data) => {
      if (data.error) {
        console.error(data.error);
        return;
      }
      gameImage.src = `data:image/png;base64,${data.image}`;
      gameImage.onload = () => {
        render();
      };
      totalReward += data.reward;
      rewardElement.textContent = totalReward;
      if (data.done) {
        if (data.reward > 0) {
          wins++;
          winsElement.textContent = wins;
        } else {
          losses++;
          lossesElement.textContent = losses;
        }
        resetGame();
      }
    });
}

function aiPlay() {
  if (!isAIEnabled) return;

  fetch('/ai_step', {
    method: 'POST'
  })
    .then(response => response.json())
    .then((data) => {
      if (data.error) {
        console.error(data.error);
        return;
      }
      gameImage.src = `data:image/png;base64,${data.image}`;
      gameImage.onload = () => {
        render();
      };
      totalReward += data.reward;
      rewardElement.textContent = totalReward;
      if (data.done) {
        if (data.reward > 0) {
          wins++;
          winsElement.textContent = wins;
        } else {
          losses++;
          lossesElement.textContent = losses;
        }
        resetGame();
      } else {
        aiPlay();
      }
    });
}

// Initialize the game
resetGame();
document.addEventListener('keydown', handleKeydown);
