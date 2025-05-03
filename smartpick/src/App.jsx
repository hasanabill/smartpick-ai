import { useState, useRef, useEffect } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!query.trim()) return;

    setMessages((prev) => [...prev, { sender: "user", text: query }]);
    setQuery("");

    try {
      const res = await axios.post("http://localhost:5000/api/recommend", {
        query,
      });

      if (res.data.data.length === 0) {
        setMessages((prev) => [
          ...prev,
          { sender: "bot", type: "text", text: res.data.message },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          { sender: "bot", type: "table", data: res.data.data },
        ]);
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", type: "text", text: "Something went wrong." },
      ]);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <header className="bg-white shadow p-4 text-xl font-semibold text-center">
        📱 SmartPick Chat
      </header>

      <div className="flex-1 overflow-hidden">
        <div className="h-full overflow-y-auto p-4 space-y-6">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${
                msg.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-lg w-fit px-4 py-3 rounded-xl shadow ${
                  msg.sender === "user"
                    ? "bg-blue-600 text-white rounded-br-none"
                    : "bg-white text-black rounded-bl-none"
                }`}
              >
                {msg.type === "table" ? (
                  <div className="overflow-x-auto">
                    <table className="text-sm text-left border border-gray-300 w-full">
                      <thead className="bg-gray-200 text-gray-700">
                        <tr>
                          <th className="px-2 py-1 border">Brand</th>
                          <th className="px-2 py-1 border">Model</th>
                          <th className="px-2 py-1 border">Price</th>
                          <th className="px-2 py-1 border">RAM</th>
                          <th className="px-2 py-1 border">Battery</th>
                          <th className="px-2 py-1 border">Camera</th>
                          <th className="px-2 py-1 border">⭐</th>
                        </tr>
                      </thead>
                      <tbody>
                        {msg.data.map((phone, index) => (
                          <tr key={index} className="odd:bg-gray-50">
                            <td className="px-2 py-1 border">
                              {phone.brand_name}
                            </td>
                            <td className="px-2 py-1 border">{phone.model}</td>
                            <td className="px-2 py-1 border">₹{phone.price}</td>
                            <td className="px-2 py-1 border">
                              {phone.ram_capacity}GB
                            </td>
                            <td className="px-2 py-1 border">
                              {phone.battery_capacity}mAh
                            </td>
                            <td className="px-2 py-1 border">
                              {phone.primary_camera_rear}MP
                            </td>
                            <td className="px-2 py-1 border">
                              {phone.avg_rating}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <pre className="whitespace-pre-wrap">{msg.text}</pre>
                )}
              </div>
            </div>
          ))}
          <div ref={chatRef} />
        </div>
      </div>

      <div className="p-4 bg-white border-t flex gap-2 sticky bottom-0 z-10">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask about phones…"
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleSend}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
