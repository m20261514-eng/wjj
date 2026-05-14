# wjj
# ✖️ 곱셈구구 플래시 게임

학생들이 **2단 ~ 9단** 곱셈구구를 재미있게 복습할 수 있는 웹 기반 게임입니다.  
HTML 파일 하나로 실행되며, 별도 설치나 서버 없이 브라우저에서 바로 사용할 수 있습니다.

---

## 🎮 주요 기능

- 무작위 곱셈 문제 (2~9단), 4지선다형 선택지
- 정답 시 랜덤 점수 획득 (5~20점)
- 게임 시간(분) 자유 설정
- 학생 이름 입력 후 개인 플레이
- 게임 종료 시 이름·점수 순위표 자동 출력
- 여러 명이 순서대로 플레이하면 순위가 누적됨

---

## 🚀 실행 방법

### 방법 1 — HTML 파일 직접 실행 (가장 쉬움)

1. 아래 전체 코드를 복사해 `index.html` 파일로 저장
2. 파일을 더블클릭 → 브라우저에서 바로 실행

### 방법 2 — CodeSandbox (링크 공유)

1. [codesandbox.io](https://codesandbox.io) 접속 → **Create Sandbox** → **Static** 선택
2. `index.html`에 아래 코드 전체 붙여넣기
3. **Share** 버튼 → 링크 복사 → 학생들에게 공유

### 방법 3 — GitHub Pages (무료 웹 호스팅)

1. 이 저장소를 Fork 또는 `index.html`로 파일 추가
2. 저장소 **Settings → Pages → Branch: main** 선택 후 저장
3. `https://<유저명>.github.io/<저장소명>/` 링크로 접속 가능

---

## 📄 전체 코드

아래 코드를 `index.html`로 저장하면 바로 실행됩니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>곱셈구구 플래시 게임</title>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #f0f4ff;
      --card: #ffffff;
      --primary: #4f46e5;
      --primary-light: #eef2ff;
      --primary-dark: #3730a3;
      --success: #10b981;
      --success-light: #d1fae5;
      --danger: #ef4444;
      --danger-light: #fee2e2;
      --text: #1e1b4b;
      --text-sub: #6b7280;
      --border: #e5e7eb;
      --radius: 16px;
      --shadow: 0 4px 24px rgba(79,70,229,0.10);
    }

    body {
      font-family: 'Nunito', sans-serif;
      background: var(--bg);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1rem;
    }

    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background:
        radial-gradient(circle at 20% 20%, #c7d2fe44 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, #fde68a33 0%, transparent 50%);
      pointer-events: none;
    }

    #app { width: 100%; max-width: 440px; position: relative; z-index: 1; }
    .screen { display: none; }
    .screen.active { display: block; }

    .card {
      background: var(--card);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 2rem;
    }

    .game-header { text-align: center; margin-bottom: 2rem; }
    .game-header .emoji { font-size: 48px; display: block; margin-bottom: 0.5rem; }
    .game-header h1 { font-size: 26px; font-weight: 900; color: var(--text); letter-spacing: -0.5px; }
    .game-header p { font-size: 14px; color: var(--text-sub); margin-top: 4px; }

    .field { margin-bottom: 1.25rem; }
    .field label {
      display: block; font-size: 13px; font-weight: 700; color: var(--text-sub);
      text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;
    }
    .field input {
      width: 100%; padding: 12px 16px; border: 2px solid var(--border); border-radius: 12px;
      font-family: 'Nunito', sans-serif; font-size: 16px; font-weight: 600;
      color: var(--text); outline: none; transition: border-color 0.2s;
    }
    .field input:focus { border-color: var(--primary); }

    .btn {
      width: 100%; padding: 14px; border: none; border-radius: 12px;
      font-family: 'Nunito', sans-serif; font-size: 16px; font-weight: 900;
      cursor: pointer; transition: transform 0.1s, box-shadow 0.1s;
    }
    .btn:active { transform: scale(0.97); }
    .btn-primary { background: var(--primary); color: #fff; box-shadow: 0 4px 16px rgba(79,70,229,0.3); }
    .btn-primary:hover { background: var(--primary-dark); }
    .btn-outline {
      background: transparent; color: var(--text-sub);
      border: 2px solid var(--border); margin-top: 10px;
    }
    .btn-outline:hover { background: var(--bg); }

    .hud { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 1rem; }
    .hud-item { background: var(--card); border-radius: 12px; padding: 10px; text-align: center; box-shadow: var(--shadow); }
    .hud-label { font-size: 11px; font-weight: 700; color: var(--text-sub); text-transform: uppercase; letter-spacing: 0.5px; }
    .hud-value { font-size: 22px; font-weight: 900; color: var(--text); margin-top: 2px; }
    .hud-value.danger { color: var(--danger); }

    .question-box {
      background: var(--primary-light); border-radius: var(--radius);
      padding: 2rem 1.5rem 1.5rem; text-align: center; margin-bottom: 1rem;
    }
    .player-tag {
      display: inline-block; background: var(--primary); color: #fff;
      font-size: 12px; font-weight: 700; padding: 3px 12px;
      border-radius: 99px; margin-bottom: 1rem;
    }
    .question-text { font-size: 42px; font-weight: 900; color: var(--primary-dark); letter-spacing: -1px; }

    .feedback { height: 22px; text-align: center; font-size: 14px; font-weight: 700; margin-bottom: 0.75rem; }
    .feedback.correct { color: var(--success); }
    .feedback.wrong { color: var(--danger); }

    .choices { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .choice-btn {
      padding: 20px; font-family: 'Nunito', sans-serif; font-size: 22px; font-weight: 900;
      border: 2.5px solid var(--border); border-radius: 14px; background: var(--card);
      color: var(--text); cursor: pointer;
      transition: border-color 0.15s, background 0.15s, transform 0.1s;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .choice-btn:hover:not(:disabled) {
      border-color: var(--primary); background: var(--primary-light); transform: translateY(-2px);
    }
    .choice-btn.correct { border-color: var(--success); background: var(--success-light); color: #065f46; }
    .choice-btn.wrong { border-color: var(--danger); background: var(--danger-light); color: #991b1b; }
    .choice-btn:disabled { cursor: default; transform: none; }

    .result-banner {
      background: linear-gradient(135deg, var(--primary) 0%, #818cf8 100%);
      border-radius: var(--radius); padding: 1.5rem; text-align: center;
      color: #fff; margin-bottom: 1.25rem;
    }
    .result-banner .big-score { font-size: 52px; font-weight: 900; letter-spacing: -2px; }
    .result-banner .result-name { font-size: 14px; opacity: 0.85; margin-bottom: 4px; }
    .result-banner .result-correct { font-size: 13px; opacity: 0.75; margin-top: 4px; }

    .rank-list { list-style: none; }
    .rank-item { display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--border); }
    .rank-item:last-child { border-bottom: none; }
    .rank-badge {
      width: 30px; height: 30px; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 13px; font-weight: 900; flex-shrink: 0;
    }
    .rank-badge.r1 { background: #fef3c7; color: #92400e; }
    .rank-badge.r2 { background: #f3f4f6; color: #374151; }
    .rank-badge.r3 { background: #fee2e2; color: #7f1d1d; }
    .rank-badge.rn { background: var(--primary-light); color: var(--primary); }
    .rank-name { flex: 1; font-size: 15px; font-weight: 700; color: var(--text); }
    .rank-score { font-size: 15px; font-weight: 900; color: var(--primary); }

    @keyframes pop { 0%{transform:scale(0.8);opacity:0} 60%{transform:scale(1.1)} 100%{transform:scale(1);opacity:1} }
    .pop { animation: pop 0.3s ease; }
    @keyframes scoreFlash { 0%{transform:scale(1)} 40%{transform:scale(1.4)} 100%{transform:scale(1)} }
    .score-flash { animation: scoreFlash 0.3s ease; }
  </style>
</head>
<body>
<div id="app">

  <!-- 이름 입력 화면 -->
  <div id="screen-name" class="screen active">
    <div class="card">
      <div class="game-header">
        <span class="emoji">✖️</span>
        <h1>곱셈구구 게임</h1>
        <p>2단 ~ 9단 도전!</p>
      </div>
      <div class="field">
        <label>이름</label>
        <input type="text" id="name-input" placeholder="홍길동" maxlength="10" />
      </div>
      <div class="field">
        <label>게임 시간 (분)</label>
        <input type="number" id="time-input" value="3" min="1" max="10" />
      </div>
      <button class="btn btn-primary" onclick="startGame()">🚀 게임 시작!</button>
    </div>
  </div>

  <!-- 게임 화면 -->
  <div id="screen-game" class="screen">
    <div class="hud">
      <div class="hud-item">
        <div class="hud-label">⏱ 시간</div>
        <div class="hud-value" id="timer-display">3:00</div>
      </div>
      <div class="hud-item">
        <div class="hud-label">✅ 정답</div>
        <div class="hud-value" id="correct-count">0</div>
      </div>
      <div class="hud-item">
        <div class="hud-label">⭐ 점수</div>
        <div class="hud-value" id="score-display">0</div>
      </div>
    </div>

    <div class="question-box">
      <div class="player-tag" id="player-tag">플레이어</div>
      <div class="question-text" id="question-text">? × ? = ?</div>
    </div>

    <div class="feedback" id="feedback"></div>
    <div class="choices" id="choices"></div>
  </div>

  <!-- 결과 화면 -->
  <div id="screen-end" class="screen">
    <div class="result-banner" id="result-banner">
      <div class="result-name" id="result-name"></div>
      <div class="big-score" id="result-score"></div>
      <div class="result-correct" id="result-correct"></div>
    </div>
    <div class="card">
      <h2 style="font-size:15px;font-weight:900;color:#6b7280;margin-bottom:1rem;text-transform:uppercase;letter-spacing:0.5px;">🏆 전체 순위</h2>
      <ul class="rank-list" id="rank-list"></ul>
    </div>
    <button class="btn btn-outline" onclick="resetToName()">👤 다른 학생 차례</button>
  </div>

</div>
<script>
  let playerName = '', score = 0, correctCount = 0;
  let timeLeft = 0, timerInterval = null;
  let results = [];
  let currentAnswer = 0, canAnswer = true;

  function ri(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }

  function genQuestion() {
    const a = ri(2, 9), b = ri(2, 9), ans = a * b;
    const opts = new Set([ans]);
    while (opts.size < 4) { const f = ri(4, 81); if (f !== ans) opts.add(f); }
    return { a, b, ans, choices: [...opts].sort(() => Math.random() - 0.5) };
  }

  function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
  }

  function startGame() {
    playerName = document.getElementById('name-input').value.trim();
    const mins = parseInt(document.getElementById('time-input').value) || 3;
    if (!playerName) { alert('이름을 입력해주세요!'); return; }
    score = 0; correctCount = 0; canAnswer = true;
    timeLeft = mins * 60;
    document.getElementById('player-tag').textContent = playerName + ' 님';
    updateHud();
    showScreen('screen-game');
    loadQuestion();
    clearInterval(timerInterval);
    timerInterval = setInterval(tick, 1000);
  }

  function tick() {
    timeLeft--;
    updateHud();
    const tv = document.getElementById('timer-display');
    if (timeLeft <= 10) tv.classList.add('danger'); else tv.classList.remove('danger');
    if (timeLeft <= 0) endGame();
  }

  function updateHud() {
    const m = Math.floor(timeLeft / 60), s = String(timeLeft % 60).padStart(2, '0');
    document.getElementById('timer-display').textContent = m + ':' + s;
    document.getElementById('score-display').textContent = score;
    document.getElementById('correct-count').textContent = correctCount;
  }

  function loadQuestion() {
    const q = genQuestion();
    currentAnswer = q.ans;
    const qt = document.getElementById('question-text');
    qt.textContent = q.a + ' × ' + q.b + ' = ?';
    qt.classList.remove('pop'); void qt.offsetWidth; qt.classList.add('pop');
    document.getElementById('feedback').textContent = '';
    document.getElementById('feedback').className = 'feedback';
    const container = document.getElementById('choices');
    container.innerHTML = '';
    q.choices.forEach(c => {
      const btn = document.createElement('button');
      btn.className = 'choice-btn';
      btn.textContent = c;
      btn.onclick = () => handleAnswer(c, btn);
      container.appendChild(btn);
    });
    canAnswer = true;
  }

  function handleAnswer(choice, btn) {
    if (!canAnswer) return;
    canAnswer = false;
    document.querySelectorAll('.choice-btn').forEach(b => {
      b.disabled = true;
      if (parseInt(b.textContent) === currentAnswer) b.classList.add('correct');
    });
    const fb = document.getElementById('feedback');
    if (choice === currentAnswer) {
      btn.classList.add('correct');
      const gained = ri(5, 20);
      score += gained; correctCount++;
      fb.textContent = '🎉 정답! +' + gained + '점';
      fb.className = 'feedback correct';
      const sd = document.getElementById('score-display');
      sd.classList.remove('score-flash'); void sd.offsetWidth; sd.classList.add('score-flash');
    } else {
      btn.classList.add('wrong');
      fb.textContent = '😅 틀렸어요!';
      fb.className = 'feedback wrong';
    }
    updateHud();
    setTimeout(loadQuestion, 900);
  }

  function endGame() {
    clearInterval(timerInterval);
    results.push({ name: playerName, score, correct: correctCount });
    const sorted = [...results].sort((a, b) => b.score - a.score);
    document.getElementById('result-name').textContent = playerName + ' 님의 최종 점수';
    document.getElementById('result-score').textContent = score + '점';
    document.getElementById('result-correct').textContent = '정답 ' + correctCount + '개';
    const rl = document.getElementById('rank-list');
    rl.innerHTML = '';
    sorted.forEach((r, i) => {
      const li = document.createElement('li');
      li.className = 'rank-item';
      const badgeClass = i === 0 ? 'rank-badge r1' : i === 1 ? 'rank-badge r2' : i === 2 ? 'rank-badge r3' : 'rank-badge rn';
      const medal = i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : (i + 1);
      li.innerHTML = '<div class="' + badgeClass + '">' + medal + '</div><div class="rank-name">' + r.name + '</div><div class="rank-score">' + r.score + '점</div>';
      rl.appendChild(li);
    });
    showScreen('screen-end');
  }

  function resetToName() {
    document.getElementById('name-input').value = '';
    showScreen('screen-name');
  }
</script>
</body>
</html>
```

---

## 📁 파일 구조

별도 파일 구조 없이 `index.html` 단일 파일로 동작합니다.

```
your-repo/
└── index.html
```

---

## 🛠 커스터마이즈

| 항목 | 위치 | 설명 |
|------|------|------|
| 문제 범위 | `ri(2, 9)` | 단 범위 변경 (예: 2~5단만) |
| 점수 범위 | `ri(5, 20)` | 획득 점수 조정 |
| 기본 시간 | `value="3"` | 기본 게임 시간(분) 변경 |
| 색상 테마 | `:root { --primary: ... }` | CSS 변수로 색상 일괄 변경 |

---

## 📝 참고

- 여러 명이 함께 실시간으로 플레이하려면 서버 및 데이터베이스 연동이 필요합니다.
- 현재는 같은 브라우저 세션 내에서 순위가 누적됩니다 (페이지 새로고침 시 초기화).
