let tasks = [];
function formatDate(iso) {
    if (!iso) return null;

    const [year, month, day] = iso.split("-");
    return `${day}/${month}/${year}`;
}

function showToast(message, type="success") {
    const container = document.getElementById("toast-container");

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.innerText = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3500);
}

function addTask() {
    const title = document.getElementById("title").value;
    const due_date = document.getElementById("due_date").value;
    const estimated_hours = parseFloat(document.getElementById("estimated_hours").value);
    const importance = parseInt(document.getElementById("importance").value);
    const deps = document.getElementById("dependencies").value
        .split(",")
        .map(d => d.trim())
        .filter(d => d.length > 0);

    if (!title) {
        alert("Title required");
        return;
    }

    const newTask = {
        id: String(tasks.length),
        title,
        due_date: due_date || null,
        estimated_hours: isNaN(estimated_hours) ? null : estimated_hours,
        importance: isNaN(importance) ? null : importance,
        dependencies: deps
    };

    tasks.push(newTask);
    showToast("Task added!", "success");

}

function analyzeTasks(event) {
    if (event) event.preventDefault();
    let inputData = tasks;

    const jsonText = document.getElementById("jsonInput").value.trim();
    const cleaned = jsonText.replace(/\s+/g, "");

    if (cleaned.length > 0) {
        try {
            inputData = JSON.parse(jsonText);
        } catch (e) {
            showToast("Invalid JSON format!", "error");
            return;
        }
    }


    const strategy = document.getElementById("strategy").value;

    fetch("http://127.0.0.1:8000/api/tasks/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ strategy, tasks: inputData })
    })
    .then(res => res.json())
    .then(data => showOutput(data))
    .catch(() => showToast("Could not connect to backend", "error"));
}

function suggestTasks() {
    fetch("http://127.0.0.1:8000/api/tasks/suggest/")
        .then(res => res.json())
        .then(data => showOutput(data))
        .catch(() =>showToast("Could not connect to backend", "error"));
}

function showOutput(data) {
    const box = document.getElementById("output");
    box.innerHTML = "";

    data.forEach(task => {
        let level = "low";
        if (task.score > 70) level = "high";
        else if (task.score > 40) level = "medium";

        box.innerHTML += `
            <div class="task-box ${level}">
                <h3>${task.title}</h3>
                <p>Score: ${task.score}</p>
                <p>${task.explanation}</p>
                <p><b>Due:</b> ${formatDate(task.due_date) || "None"}</p>
            </div>
        `;
    });
}
