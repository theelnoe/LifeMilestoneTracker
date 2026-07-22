const projectData = JSON.parse(
    document.getElementById("projectData").textContent
);

const currentProject =
    new URLSearchParams(window.location.search).get("project") || 0;

const milestones = projectData.milestones;
const total = projectData.total;

// ========================================
// Global Variables
// ========================================

let timerRunning = false;
let startTime = null;
let timerInterval = null;


// ========================================
// Initialize
// ========================================

window.onload = function () {
    console.log("window loaded");
    restoreTimer();

    buildMilestoneBar();

    updateMilestones();

};

updateMilestones();

function updateMilestones() {

    let next = "Completed";
    let last = "0 h";

    for (let i = 0; i < milestones.length; i++) {

        if (total < milestones[i]) {

            next = milestones[i] + " h";

            if (i > 0)
                last = milestones[i - 1] + " h";

            break;
        }

    }

    if (total >= milestones[milestones.length - 1]) {

        last = milestones[milestones.length - 1] + " h";

        next = "Completed";

    }

    document.getElementById("nextMilestone").textContent = next;
    document.getElementById("lastMilestone").textContent = last;

}

// ========================================
// Timer
// ========================================

function startTimer() {

    if (timerRunning)
        return;

    fetch("/start_timer?project=" + currentProject, {

        method: "POST"

    })
    .then(r => r.json())
    .then(data => {

        timerRunning = true;

        startTime = new Date();

        document.getElementById("status").innerHTML =
            "🟢 Studying...";

        document.getElementById("startBtn").disabled = true;

        document.getElementById("stopBtn").disabled = false;

        timerInterval = setInterval(updateTimer,1000);

    });

}

// ========================================
// Restore Timer
// ========================================

function restoreTimer() {

    fetch("/timer_status")

        .then(r => r.json())

        .then(data => {

            if (!data.running)
                return;

            timerRunning = true;

            startTime = new Date(data.start);

            document.getElementById("status").innerHTML =
                "🟢 Studying...";

            document.getElementById("startBtn").disabled = true;

            document.getElementById("stopBtn").disabled = false;

            timerInterval = setInterval(updateTimer,1000);

            updateTimer();

        });

}


// ========================================
// Live Timer
// ========================================

function updateTimer() {

    if (!timerRunning)
        return;

    let diff = Math.floor((new Date() - startTime) / 1000);

    let hours = Math.floor(diff / 3600);

    let minutes = Math.floor((diff % 3600) / 60);

    let seconds = diff % 60;

    document.getElementById("liveTimer").innerHTML =

        String(hours).padStart(2,"0") + ":" +

        String(minutes).padStart(2,"0") + ":" +

        String(seconds).padStart(2,"0");

}

// ========================================
// Stop Timer
// ========================================

function stopTimer() {

    if (!timerRunning)
        return;

    fetch("/stop_timer?project=" + currentProject, {

        method: "POST"

    })

    .then(r => r.json())

    .then(data => {

        timerRunning = false;

        clearInterval(timerInterval);

        document.getElementById("status").innerHTML =
            "⚪ Ready";

        document.getElementById("startBtn").disabled = false;

        document.getElementById("stopBtn").disabled = true;

        location.reload();

    });

}


// ========================================
// Add Time Dialog
// ========================================

function showAddTimeDialog() {

    document.getElementById("addTimeModal").style.display = "flex";

}


function closeDialog() {

    document.getElementById("addTimeModal").style.display = "none";

}


// ========================================
// Save Manual Time
// ========================================

function saveManualTime() {

    let hours = parseInt(document.getElementById("hoursInput").value) || 0;

    let minutes = parseInt(document.getElementById("minutesInput").value) || 0;

    if (minutes < 0 || minutes > 59) {

        alert("Minutes must be between 0 and 59.");

        return;

    }

    if (hours === 0 && minutes === 0) {

        alert("Please enter a study time.");

        return;

    }

    fetch("/add_time?project=" + currentProject, {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            hours: hours,

            minutes: minutes

        })

    })

    .then(r => r.json())

    .then(data => {

        closeDialog();

        location.reload();

    });

}

// ========================================
// Build Milestone Bar
// ========================================

function buildMilestoneBar() {

    let previous = 0;
    let next = milestones[milestones.length - 1];

    for (let i = 0; i < milestones.length; i++) {

        if (total < milestones[i]) {

            next = milestones[i];

            if (i > 0)
                previous = milestones[i - 1];

            break;
        }

    }

    let current = total - previous;

    let goal = next - previous;

    let percent = (current / goal) * 100;

    document.getElementById("progressFill").style.width =
        percent + "%";

    document.getElementById("milestoneStart").innerHTML =
        previous + " h";

    document.getElementById("milestoneEnd").innerHTML =
        next + " h";

    document.getElementById("milestoneProgress").innerHTML =
        `${current.toFixed(1)} / ${goal} h`;

}