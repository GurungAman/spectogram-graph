import React, { useState } from "react";
import Plot from "react-plotly.js";
import axios from "axios";

function App() {
  const [data, setData] = useState({ loading: true, data: [] });
  const [file, setFile] = useState();
  const handleOnClick = (e) => {
    e.preventDefault();
    const fileName = file.name;
    if (fileName.endsWith(".wav")) {
      fetchData();
      return
    }
    alert("Please upload a .wav file");
  };
  const fetchData = () => {
    axios({
      method: "post",
      url: "http://localhost:8000/process-spectogram/",
      data: file,
      headers: {
        "Content-Type": "audio/wave",
        Accept: "*/*",
        "Content-Disposition": `attachment; filename='${file.name}'`,
      },
    })
      .then((response) => {
        setData({ data: response.data.data, loading: false });
      })
      .catch((error) => {
        console.log(error.data);
      });
  };
  const layout = {
    title: "Spectogram",
    yaxis: { title: "Frequency (Hz)" },
    xaxis: { title: "Time" },
    width: 1200,
    height: 700,
  };
  return (
    <div>
      <div style={{ textAlign: "center" }}>
        <h4>Upload file here.</h4>
        <input type='file' onChange={(e) => setFile(e.target.files[0])} />

        <br />
        <button onClick={(e) => handleOnClick(e)}>Upload</button>
        <br />
        {data["loading"] ? (
          ""
        ) : (
          <Plot
            layout={layout}
            data={[
              {
                x: data.data.time,
                y: data.data.frequency,
                z: data.data.spectogram,
                type: "heatmap",
                colorscale: "Jet",
              },
            ]}
          />
        )}
      </div>
    </div>
  );
}

export default App;
