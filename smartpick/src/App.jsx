import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSearch = async () => {
    if (!query.trim()) return;

    // Add the user's query to the chat
    setMessages((prev) => [...prev, { type: "user", text: query }]);

    try {
      const response = await axios.post("http://127.0.0.1:5000/recommend", {
        query,
        top_n: 5,
      });

      // Add the response to the chat
      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: response.data.map((phone) => (
            <div key={phone.model} className="phone-card">
              <h3>
                {phone.brand_name} {phone.model}
              </h3>
              <p>Price: ₹{phone.price}</p>
              <p>RAM: {phone.ram_capacity}GB</p>
              <p>Battery: {phone.battery_capacity}mAh</p>
              <p>Camera: {phone.primary_camera_rear}MP</p>
              <p>Rating: {phone.avg_rating}</p>
            </div>
          )),
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          type: "bot",
          text: err.response?.data?.message || "An error occurred",
        },
      ]);
    }

    setQuery(""); // Clear the input field
  };

  return (
    <div className="App">
      <h1>SmartPick.ai</h1>
      <div className="chat-container">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`chat-message ${
              message.type === "user" ? "user" : "bot"
            }`}
          >
            {message.type === "bot" && Array.isArray(message.text) ? (
              message.text
            ) : (
              <p>{message.text}</p>
            )}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          placeholder="Ask about phones (e.g., 'best phone under 20000')"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />
        <button onClick={handleSearch}>Send</button>
      </div>
    </div>
  );
}

export default App;
