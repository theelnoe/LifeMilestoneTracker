const projectData = JSON.parse(
    document.getElementById("projectData").textContent
);
console.log(projectData);
const currentProject =
    new URLSearchParams(window.location.search).get("project") || 0;

// ========================================
// Global Variables
// ========================================

let timerRunning = false;
let startTime = null;
let timerInterval = null;
let editingSessionIndex = null;
let editingRow = null;

// ========================================
// Initialize
// ========================================

window.onload = function () {

    console.log("window loaded");

    // -------------------------
    // General
    // -------------------------

    restoreTimer();

    updateMilestoneUI();

    // -------------------------
    // New Project
    // -------------------------

    const newProjectBtn =
        document.getElementById("newProjectBtn");

    const newProjectModal =
        document.getElementById("newProjectModal");

    const cancelProjectBtn =
        document.getElementById("cancelProjectBtn");

    const createProjectBtn =
        document.getElementById("createProjectBtn");

    const newProjectName =
        document.getElementById("newProjectName");

    const newProjectGoal =
        document.getElementById("newProjectGoal");

    const newProjectUnit =
        document.getElementById("newProjectUnit");

    // -------------------------
    // Delete Project
    // -------------------------

    const deleteProjectBtn =
        document.getElementById("deleteProjectBtn");

    const deleteProjectModal =
        document.getElementById("deleteProjectModal");

    const cancelDeleteBtn =
        document.getElementById("cancelDeleteBtn");

    const confirmDeleteBtn =
        document.getElementById("confirmDeleteBtn");

    // -------------------------
    // Edit Project
    // -------------------------
    const editProjectBtn =
        document.getElementById("editProjectBtn");

    const editProjectModal =
        document.getElementById("editProjectModal");

    const cancelEditBtn =
        document.getElementById("cancelEditBtn");

    const saveEditBtn =
        document.getElementById("saveEditBtn");

    const editProjectName =
        document.getElementById("editProjectName");

    const editProjectGoal =
        document.getElementById("editProjectGoal");    

    // -------------------------
    // Edit Session
    // -------------------------
    const editSessionModal =
        document.getElementById("editSessionModal");

    const saveEditSessionBtn =
        document.getElementById("saveEditSessionBtn");

    const cancelEditSessionBtn =
        document.getElementById("cancelEditSessionBtn");

    const editButtons =
        document.querySelectorAll(".editSessionBtn");

    editButtons.forEach(btn => {

        btn.onclick = onEditSession;

    });

    const deleteButtons =
        document.querySelectorAll(".deleteSessionBtn");

    deleteButtons.forEach(btn => {

        btn.onclick = onDeleteSession;

    });

    saveEditSessionBtn.onclick = function () {

        const hours =
            parseInt(document.getElementById("editHours").value) || 0;

        const minutes =
            parseInt(document.getElementById("editMinutes").value) || 0;

        fetch("/edit_session", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                project_id: currentProject,

                session_id: editingSessionId,

                hours: hours,

                minutes: minutes

            })

        })

        .then(r => r.json())

        .then(data => {

            // refreshDashboard(data);

            editingRow.querySelector(".sessionDisplay").textContent =
                data.display;

            editSessionModal.style.display = "none";

        });

    };

    /* // -------------------------
    // Delete Session
    // -------------------------
    const deleteButtons =
        document.querySelectorAll(".deleteSessionBtn");

    deleteButtons.forEach(btn => {

        btn.onclick = async function () {
            
            if (!confirm("Delete this session?"))
                return;

            const sessionId = this.dataset.sessionId;

            const response = await fetch("/delete_session?project=" + currentProject, {
            
                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    session_id: sessionId

                })

            });
            
            const result = await response.json();
            
            if (result.success) {

                location.reload();

            }

        };

    }); */

    // =========================
    // Events
    // =========================

    newProjectBtn.onclick = function () {

        newProjectModal.style.display = "flex";

    };

    cancelProjectBtn.onclick = function () {

        newProjectModal.style.display = "none";

    };

    createProjectBtn.onclick = function () {

        if (newProjectName.value.trim() === "") {

            alert("Project name is required.");

            return;

        }

        if (newProjectGoal.value <= 0) {

            alert("Goal must be greater than zero.");

            return;

        }

        const form = document.createElement("form");

        form.method = "POST";

        form.action = "/create_project";

        const inputName = document.createElement("input");
        inputName.type = "hidden";
        inputName.name = "name";
        inputName.value = newProjectName.value;

        const inputGoal = document.createElement("input");
        inputGoal.type = "hidden";
        inputGoal.name = "goal";
        inputGoal.value = newProjectGoal.value;

        const inputUnit = document.createElement("input");
        inputUnit.type = "hidden";
        inputUnit.name = "domain_id";
        inputUnit.value = newProjectUnit.value;

        form.appendChild(inputName);
        form.appendChild(inputGoal);
        form.appendChild(inputUnit);

        document.body.appendChild(form);

        form.submit();

    };

    deleteProjectBtn.onclick = function () {

        deleteProjectModal.style.display = "flex";

    };

    cancelDeleteBtn.onclick = function () {

        deleteProjectModal.style.display = "none";

    };

    confirmDeleteBtn.onclick = function () {

        const form = document.createElement("form");

        form.method = "POST";

        form.action = "/delete_project";

        const inputProject = document.createElement("input");

        inputProject.type = "hidden";

        inputProject.name = "project_id";

        inputProject.value = projectData.id;

        form.appendChild(inputProject);

        document.body.appendChild(form);

        form.submit();

    };

    editProjectBtn.onclick = function () {

        editProjectName.value = projectData.name;

        editProjectGoal.value =
            projectData.goal;

        editProjectModal.style.display = "flex";

    };

    cancelEditBtn.onclick = function () {

        editProjectModal.style.display = "none";

    };

    saveEditBtn.onclick = function () {

        if (editProjectName.value.trim() === "") {

            alert("Project name is required.");

            return;

        }

        if (editProjectGoal.value <= 0) {

            alert("Goal must be greater than zero.");

            return;

        }

        const form = document.createElement("form");

        form.method = "POST";

        form.action = "/edit_project";

        const inputProject = document.createElement("input");
        inputProject.type = "hidden";
        inputProject.name = "project_id";
        inputProject.value = projectData.id;

        const inputIndex = document.createElement("input");
        inputIndex.type = "hidden";
        inputIndex.name = "project_index";
        inputIndex.value = getCurrentProject();

        const inputDomain = document.createElement("input");
        inputDomain.type = "hidden";
        inputDomain.name = "domain_id";
        inputDomain.value = projectData.domain_id;

        form.appendChild(inputProject);
        form.appendChild(inputIndex);
        form.appendChild(inputDomain);

        const inputName = document.createElement("input");
        inputName.type = "hidden";
        inputName.name = "name";
        inputName.value = editProjectName.value;

        const inputGoal = document.createElement("input");
        inputGoal.type = "hidden";
        inputGoal.name = "goal";
        inputGoal.value = editProjectGoal.value;

        form.appendChild(inputProject);
        form.appendChild(inputName);
        form.appendChild(inputGoal);

        document.body.appendChild(form);

        form.submit();

    };

    cancelEditSessionBtn.onclick = function () {

        editSessionModal.style.display = "none";

    };
};
   

// ========================================
// Project
// ========================================

function getCurrentProject() {

    return currentProject;

}

function refreshDashboard(data) {
    
    // ---------- Update project data ----------

    projectData.total = data.total_hours;

    projectData.goal = data.goal;

    projectData.milestones = data.milestones;

    // ---------- Summary ----------

    document.querySelector(".total-hours").textContent =
        data.total_text + " / " + data.goal + " h";

    document.querySelector(".percent").textContent =
        data.progress + " %";

    // ---------- Cards ----------

    document.getElementById("todayHours").textContent =
        data.today_text;

    document.getElementById("weekHours").textContent =
        data.week_text;

    document.getElementById("totalHours").textContent =
        data.total_text;

    // ---------- Milestones ----------
    
    updateMilestoneUI();
    
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

    document.getElementById("hoursInput").value = "";
    document.getElementById("minutesInput").value = "";

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

    fetch("/add_time", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            project_id: currentProject,
            hours: hours,
            minutes: minutes

        })

    })

    .then(r => r.json())

    .then(data => {

        console.log(data);

        closeDialog();

        refreshDashboard(data);

        addHistoryRow(data.new_history, 0);

    });

}

// ========================================
// Build Milestone Bar
// ========================================

function updateMilestoneUI() {

    const m = getMilestoneState();

    document.getElementById("progressFill").style.width =
        m.percent + "%";

    document.getElementById("lastMilestone").textContent =
        m.previous + " h";

    document.getElementById("nextMilestone").textContent =
        m.completed ? "Completed" : m.next + " h";

    document.getElementById("milestoneStart").textContent =
        m.previous + " h";

    document.getElementById("milestoneEnd").textContent =
        m.next + " h";

    document.getElementById("milestoneProgress").textContent =
        `${formatHours(m.current)} / ${m.goal} h`;

}

function formatHours(hours) {
    const totalMinutes = Math.round(hours * 60);

    const h = Math.floor(totalMinutes / 60);
    const m = totalMinutes % 60;

    if (h && m) return `${h} h ${m} m`;
    if (h) return `${h} h`;
    return `${m} m`;
}

function getMilestoneState() {

    const milestones = projectData.milestones;
    const total = projectData.total;

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

    let completed = false;

    if (total >= milestones[milestones.length - 1]) {

        previous = milestones[milestones.length - 1];
        next = previous;
        completed = true;

    }

    const current = total - previous;
    const goal = next - previous;

    let percent = 100;

    if (!completed && goal > 0)
        percent = current / goal * 100;

    percent = Math.max(0, Math.min(100, percent));

    return {
        previous,
        next,
        current,
        goal,
        percent,
        completed
    };

}

function createHistoryRow(item, index) {

    const row = document.createElement("tr");

    row.innerHTML = `

        <td>${item.date}</td>

        <td class="sessionDisplay">${item.display}</td>

        <td>

            <button
                class="editSessionBtn"
                data-session-id="${item.id}">
                ✏️
            </button>

            <button
                class="deleteSessionBtn"
                data-session-id="${item.id}">
                🗑
            </button>

        </td>

    `;

    return row;

}

function addHistoryRow(item, index) {

    const tbody = document.querySelector("tbody");

    const row = createHistoryRow(item, index);

    attachHistoryEvents(row);

    tbody.prepend(row);

    refreshHistoryIndexes();
}

function attachHistoryEvents(row) {

    row.querySelector(".editSessionBtn").onclick =
        onEditSession;

    row.querySelector(".deleteSessionBtn").onclick =
        onDeleteSession;

}

function onEditSession() {

    editingSessionId = parseInt(this.dataset.sessionId);
    
    const row = this.closest("tr");
    editingRow = row;
    const timeText = row.cells[1].textContent.trim();

    let hours = 0;
    let minutes = 0;

    const hourMatch = timeText.match(/(\d+)\s*h/);
    const minuteMatch = timeText.match(/(\d+)\s*m/);

    if (hourMatch)
        hours = parseInt(hourMatch[1]);

    if (minuteMatch)
        minutes = parseInt(minuteMatch[1]);

    document.getElementById("editHours").value = hours;

    document.getElementById("editMinutes").value = minutes;

    editSessionModal.style.display = "flex";

}

async function onDeleteSession() {

    console.log("DELETE CLICKED");

    if (!confirm("Delete this session?"))
        return;

    const sessionId = this.dataset.sessionId;

    const response = await fetch(
        "/delete_session",
        {
            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                project_id: currentProject,

                session_id: sessionId

            })

        }
    );

    const result = await response.json();

    console.log(result);

    if (result.success) {

        location.reload();

    }
}

function refreshHistoryIndexes() {

    const rows =
        document.querySelectorAll("tbody tr");

    rows.forEach((row, index) => {

        row.querySelector(".editSessionBtn")
            .dataset.index = index;

        row.querySelector(".deleteSessionBtn")
            .dataset.index = index;

    });

}