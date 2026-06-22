let resume = "";

function send() {
    let msg = document.getElementById("msg").value;

    let form = new FormData();
    form.append("message", msg);
    form.append("resume_text", resume);

    fetch("/chat", { method: "POST", body: form })
    .then(res => res.json())
    .then(data => {
        document.getElementById("chat").innerHTML +=
        `<p><b>You:</b> ${msg}</p><p><b>AI:</b> ${data.reply}</p>`;
    });
}

function upload() {
    let file = document.getElementById("file").files[0];

    let form = new FormData();
    form.append("file", file);

    fetch("/upload", { method: "POST", body: form })
    .then(res => res.json())
    .then(data => {
        resume = data.skills.join(", ");

        document.getElementById("dashboard").innerHTML = `
            <h3>ATS Score: ${data.score}/100</h3>
            <p>Skills: ${data.skills.join(", ")}</p>
            <p>Missing: ${data.missing.join(", ")}</p>
        `;
    });
}
