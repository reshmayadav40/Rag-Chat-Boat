import { useState } from "react";

import Message from "./Message";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const initialMessage = {
  role: "assistant",
  content: "Welcome. Ask me something from the React, Node.js, or MongoDB documents.",
  sources: [],
};

function Chat() {
  const [messages, setMessages] = useState([initialMessage]);
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function sendQuestion(event) {
    event?.preventDefault();
    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || isLoading) {
      return;
    }

    setError("");
    setQuestion("");
    setMessages((current) => [
      ...current,
      { role: "user", content: trimmedQuestion },
    ]);
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmedQuestion }),
      });

      let payload;
      try {
        payload = await response.json();
      } catch {
        throw new Error("The chatbot server returned an invalid response.");
      }

      if (!response.ok) {
        throw new Error(payload.detail || "The chatbot server could not answer.");
      }

      if (typeof payload.answer !== "string" || !Array.isArray(payload.sources)) {
        throw new Error("The chatbot server returned an invalid response.");
      }

      setMessages((current) => [
        ...current,
        { role: "assistant", content: payload.answer, sources: payload.sources },
      ]);
    } catch (requestError) {
      setError(
        requestError.message === "Failed to fetch"
          ? "Unable to connect to the chatbot server. Make sure the FastAPI backend is running."
          : requestError.message,
      );
    } finally {
      setIsLoading(false);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendQuestion(event);
    }
  }

  return (
    <section className="chat-panel" aria-label="Document chat">
      <div className="chat-toolbar">
        <div>
          <span className="toolbar-label">Live retrieval</span>
          <span className="toolbar-title">Conversation</span>
        </div>
        <span className="top-k">TOP-K <strong>3</strong></span>
      </div>

      <div className="messages" aria-live="polite">
        {messages.map((message, index) => (
          <Message key={`${message.role}-${index}`} message={message} />
        ))}
        {isLoading && (
          <div className="thinking" aria-label="Thinking">
            <span className="thinking-dots"><i /><i /><i /></span>
            Thinking through the documents...
          </div>
        )}
      </div>

      {error && <div className="error-message" role="alert">{error}</div>}

      <form className="composer" onSubmit={sendQuestion}>
        <label className="sr-only" htmlFor="question">Ask a question</label>
        <textarea
          id="question"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about the documents..."
          rows="1"
          disabled={isLoading}
        />
        <button type="submit" disabled={!question.trim() || isLoading}>
          {isLoading ? "Working" : "Send"}
          <span aria-hidden="true">↗</span>
        </button>
      </form>
      <p className="composer-note">Press Enter to send · Shift + Enter for a new line</p>
    </section>
  );
}

export default Chat;