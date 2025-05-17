import React, { useState, useRef, useEffect } from "react";
import "./Home.css";
import { sendUserInput } from "../utils/apiroutes";

const Home = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const chatRef = useRef(null);

  const handleSubmit = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const result = await sendUserInput(input);
      const fullText = result.reply || "No response received.";
      simulateTyping(fullText);
    } catch (error) {
      simulateTyping("⚠️ Error talking to server.");
    }
  };

  const simulateTyping = (text) => {
    let i = 0;
    let current = "";
    const speed = 15;

    const interval = setInterval(() => {
      current += text.charAt(i);
      i++;

      // Update the last message
      setMessages((prev) => {
        const copy = [...prev];
        if (copy[copy.length - 1]?.sender === "bot") {
          copy[copy.length - 1].text = current;
        } else {
          copy.push({ sender: "bot", text: current });
        }
        return copy;
      });

      if (i >= text.length) {
        clearInterval(interval);
        setIsTyping(false);
      }
    }, speed);
  };

  useEffect(() => {
    chatRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-container">
      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
          >
            {msg.text}
          </div>
        ))}
        <div ref={chatRef} />
      </div>

      <div className="chat-input-area">
        <input
          type="text"
          value={input}
          placeholder="Type your message..."
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          disabled={isTyping}
        />
        <button onClick={handleSubmit} disabled={isTyping}>
          {isTyping ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default Home;
