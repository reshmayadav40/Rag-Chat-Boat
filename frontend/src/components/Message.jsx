import SourceList from "./SourceList";

function Message({ message }) {
  const isUser = message.role === "user";

  return (
    <article className={`message ${isUser ? "message-user" : "message-assistant"}`}>
      <div className="message-meta">
        <span className="message-avatar">{isUser ? "You" : "KD"}</span>
        <span>{isUser ? "Your question" : "Knowledge Desk"}</span>
      </div>
      <div className="message-body">
        <p>{message.content}</p>
        {!isUser && <SourceList sources={message.sources} />}
      </div>
    </article>
  );
}

export default Message;