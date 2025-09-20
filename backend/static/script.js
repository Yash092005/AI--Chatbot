const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const toggle = document.getElementById("mode-toggle");

toggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  toggle.textContent = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
});

function appendMessage(message, sender) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);

  const content = document.createElement("span");
  content.classList.add("content");
  content.textContent = message;

  const time = document.createElement("span");
  time.classList.add("timestamp");
  const now = new Date();
  time.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  msgDiv.appendChild(content);
  msgDiv.appendChild(time);

  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
  const message = input.value.trim();
  if (!message) return;
  appendMessage(message, "user");
  input.value = "";

  const typingDiv = document.createElement("div");
  typingDiv.classList.add("typing");
  typingDiv.innerHTML = `<span></span><span></span><span></span>`;
  chatBox.appendChild(typingDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
    .then(response => response.json())
    .then(data => {
      typingDiv.remove();
      appendMessage(data.reply, "bot");
    })
    .catch(err => {
      typingDiv.remove();
      appendMessage("Error generating response", "bot");
    });
}

input.addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});
