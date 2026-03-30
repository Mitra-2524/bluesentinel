import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    alert("Uploaded: " + data.filename);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>🌊 BlueSentinel</h1>
      <p>Illegal Fishing Detection System</p>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />

      <button onClick={uploadFile}>Upload</button>
    </div>
  );
}

export default App;