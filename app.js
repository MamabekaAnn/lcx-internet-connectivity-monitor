import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [status, setStatus] = useState("loading");

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch(
          "http://localhost:5000/check_connectivity"
        );
        const data = await response.json();
        setStatus(data.status);
      } catch (error) {
        setStatus("error");
      }
    };

    fetchStatus();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Internet Connectivity Monitor</h1>
        <p className={status}>{`Status: ${status}`}</p>
      </header>
    </div>
  );
}

export default App;
