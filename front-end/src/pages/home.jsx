import React, { useState, useRef, useEffect } from "react";
import "../styles/home.css";
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
  const simulateTyping = (text, delay = 300) => {
    if (!text.trim()) return;
    let i = 0;
    let current = "";
    const speed = 15;

    setMessages((prev) => {
      const copy = [...prev];
      const last = copy[copy.length - 1];
      if (!last || last.sender !== "bot") {
        copy.push({ sender: "bot", text: "" });
      }
      return copy;
    });

    setTimeout(() => {
      const interval = setInterval(() => {
        current += text.charAt(i);
        i++;

        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1].text = current;
          return updated;
        });

        if (i >= text.length) {
          clearInterval(interval);
          setIsTyping(false);
        }
      }, speed);
    }, delay);
  };

  useEffect(() => {
    chatRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
  useEffect(() => {
    const fetchInitialMessage = async () => {
      setIsTyping(true);
      try {
        const result = await sendUserInput("init");
        const fullText =
          result.reply || "👋 Welcome! Let's get started with your diagnosis.";
        simulateTyping(fullText);
      } catch (error) {
        simulateTyping("⚠️ Failed to load initial message.");
      }
    };

    fetchInitialMessage();
  }, []);
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.warn("🛑 SpeechRecognition not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
      const speechResult = event.results[0][0].transcript;
      setInput(speechResult); // You can also call handleSubmit() here
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = (e) => {
      console.error("Speech recognition error:", e);
      setIsListening(false);
    };

    recognitionRef.current = recognition;
  }, []);

  const toggleMic = () => {
    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      recognitionRef.current?.start();
      setIsListening(true);
    }
  };

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
