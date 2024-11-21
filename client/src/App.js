import React, { useState, useEffect } from "react"

function App() {

  const [data, setData] = useState([{}])


  useEffect(() => {
    fetch("/data")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  }, []);

  return (
    
    <div>
      <h1>Data from the Server</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>

  )
}

export default App