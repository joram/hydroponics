import './App.css';
import GraphComponent from "./graph";
import {useEffect, useState} from "react";


function App() {
  const [isLoaded, setIsLoaded] = useState(false);
  const [data, setData] = useState([]);

  useEffect(() => {
  fetch("/api/v0/data")
    .then(res => res.json())
    .then((result) => {
        setIsLoaded(true);
        setData(result["data"]);
      }
    )
  }, [])

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  return (
    <div className="App">
      <h2>PH levels</h2>
      <GraphComponent data={data} data_key="PH" height={500}/>

      <h2>Conductivity</h2>
      <GraphComponent data={data} data_key="Conductivity" height={500}/>
    </div>
  );
}

export default App;
