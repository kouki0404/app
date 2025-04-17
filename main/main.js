// ゲーム設定
const NUM_COUNT = 5;
const TIME_LIMIT = 30;
let numbers = [];
let selected = [];
let score = 0;
let gameStarted = false;
let gameOver = false;

// タイマー関連
let timer;
let timeRemaining = TIME_LIMIT;

// 数字をランダムに生成
function generateNumbers() {
  numbers = [];
  for (let i = 0; i < NUM_COUNT; i++) {
    numbers.push(Math.floor(Math.random() * 20) + 1);
  }
}

// 数字を画面上に表示
function displayNumbers() {
  const gameContainer = document.getElementById('gameContainer');
  gameContainer.innerHTML = ''; // 初期化

  numbers.forEach((num, index) => {
    const button = document.createElement('button');
    button.innerText = num;
    button.classList.add('button');
    button.style.left = `${Math.random() * 90}%`;
    button.style.top = `${Math.random() * 90}%`;

    button.addEventListener('click', () => handleClick(num));
    gameContainer.appendChild(button);
  });
}

// タイマーを更新
function updateTimer() {
  const timerElement = document.getElementById('timer');
  if (timeRemaining > 0) {
    timeRemaining--;
    timerElement.innerText = timeRemaining;
  } else {
    clearInterval(timer);
    gameOver = true;
    alert('ゲームオーバー！');
  }
}

// ゲーム開始
function startGame() {
  gameStarted = true;
  generateNumbers();
  displayNumbers();

  timer = setInterval(updateTimer, 1000);
}

// ボタンがクリックされたときの処理
function handleClick(num) {
  if (gameOver) return;

  if (selected.includes(num)) {
    alert('この数字は既に選ばれています');
    return;
  }

  selected.push(num);
  score += 10; // スコア加算

  // スコアを更新
  document.getElementById('score').innerText = score;

  if (selected.length === NUM_COUNT) {
    clearInterval(timer);
    alert('ゲームクリア！あなたのスコアは ' + score);
  }
}

// 初期化
document.addEventListener('DOMContentLoaded', () => {
  startGame();
});
