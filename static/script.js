// Grab references to the HTML elements we need to work with.
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Adds a message bubble to the chat window.
// sender is either "user" or "bot" - controls the styling (left/right, color).
function addMessage(text, sender) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
  msgDiv.textContent = text;
  chatBox.appendChild(msgDiv);

  // Auto-scroll to the latest message.
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Called when the user hits "Send" (or presses Enter).
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return; // ignore empty input

  // 1. Show the user's own message immediately.
  addMessage(message, "user");
  userInput.value = "";

  // 2. Send it to our Flask backend's /chat endpoint.
  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    });

    const data = await response.json();

    // 3. Show the chatbot's reply.
    addMessage(data.answer, "bot");
  } catch (error) {
    addMessage("Oops, something went wrong connecting to the server.", "bot");
    console.error(error);
  }
}

// Send on button click.
sendBtn.addEventListener("click", sendMessage);

// Send on pressing Enter inside the input box.
userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});
