document.addEventListener('DOMContentLoaded', () => {
    const timeDisplay = document.querySelector('#time');
    const modeDisplay = document.querySelector('#mode');
    const startButton = document.querySelector('#start');
    const stopButton = document.querySelector('#stop');
    const resetButton = document.querySelector('#reset');
    const body = document.body;

    let timerInterval = null;
    let isWorkSession = true;
    let timeLeft = 1500; // 25 minutes in seconds
    let isPaused = true;

    const WORK_TIME = 1500;
    const BREAK_TIME = 300; // 5 minutes in seconds

    function updateDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        const formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        timeDisplay.textContent = formattedTime;
        document.title = `${formattedTime} - ${isWorkSession ? 'Work' : 'Break'}`;
    }

    function switchMode() {
        isWorkSession = !isWorkSession;
        timeLeft = isWorkSession ? WORK_TIME : BREAK_TIME;
        modeDisplay.textContent = isWorkSession ? 'Work' : 'Break';
        
        if (isWorkSession) {
            body.classList.remove('break-mode');
        } else {
            body.classList.add('break-mode');
        }
        
        updateDisplay();
        alert(isWorkSession ? "Time for a work session!" : "Time for a break!");
    }

    function tick() {
        if (timeLeft > 0) {
            timeLeft--;
            updateDisplay();
        } else {
            switchMode();
        }
    }

    startButton.addEventListener('click', () => {
        if (isPaused) {
            isPaused = false;
            timerInterval = setInterval(tick, 1000);
        }
    });

    stopButton.addEventListener('click', () => {
        isPaused = true;
        clearInterval(timerInterval);
    });

    resetButton.addEventListener('click', () => {
        isPaused = true;
        clearInterval(timerInterval);
        isWorkSession = true;
        timeLeft = WORK_TIME;
        modeDisplay.textContent = 'Work';
        body.classList.remove('break-mode');
        updateDisplay();
    });

    // Initial display update
    updateDisplay();
});
