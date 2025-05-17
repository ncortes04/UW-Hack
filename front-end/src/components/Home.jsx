import React, { useState } from "react";
import "./Home.css";
import { sendUserInput } from "../utils/apiroutes";

const Home = () => {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    try {
      const result = await sendUserInput(input);
      setResponse(result.reply || "No response received.");
    } catch (error) {
      setResponse("Error talking to server.");
    }
  };

  return (
    <div className="home-container">
      <h1 className="home-title">🤖 Welcome to Your AI Bot</h1>
      <p className="home-description">
        Enter your request and let the bot assist you!
      </p>

      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your request..."
        className="home-input"
      />

      <button className="home-button" onClick={handleSubmit}>
        Submit
      </button>

      {response && <p className="home-response">Bot says: {response}</p>}
    </div>
  );
};

export default Home;
