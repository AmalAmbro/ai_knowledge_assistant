import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Message = {
  role: "user" | "assistant";
  text: string;
};

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendQuery = async () => {
    if (!query.trim()) return;

    const userMessage: Message = { role: "user", text: query };
    setMessages((prev) => [...prev, userMessage]);
    setQuery("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();

      const botMessage: Message = {
        role: "assistant",
        text: data.answer || "I don't know",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Something went wrong." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-wrapper">
      <div className="chat-messages">
        {messages.map((m) => (
          <div className={`bubble ${m.role}`}>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {m.text}
            </ReactMarkdown>
          </div>
        ))}

        {loading && (
          <div className="bubble assistant thinking">
            Thinking…
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="chat-input">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask something…"
          rows={2}
        />
        <button onClick={sendQuery} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}
