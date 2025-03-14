import React, { useState } from "react";
import axios from "axios";

function App() {
  const [news, setNews] = useState("");
  const [result, setResult] = useState("");

  const checkNews = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", {
        text: news,
      });
      setResult(response.data.prediction);
    } catch (error) {
      console.error("Error:", error);
      setResult("Error checking news");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Fake News Detection</h1>
      <input
        type="text"
        placeholder="Enter news headline"
        value={news}
        onChange={(e) => setNews(e.target.value)}
        style={{ padding: "10px", width: "300px" }}
      />
      <br />
      <button onClick={checkNews} style={{ marginTop: "10px", padding: "10px" }}>
        Check News
      </button>
      <h2>{result}</h2>
    </div>
  );
}

export default App;
