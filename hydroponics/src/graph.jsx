import {CartesianGrid, Line, LineChart, XAxis, YAxis, Text} from "recharts";
import { useState, useEffect } from 'react';

function getWindowDimensions() {
  const { innerWidth: width, innerHeight: height } = window;
  return {
    width,
    height
  };
}

function useWindowDimensions() {
  const [windowDimensions, setWindowDimensions] = useState(getWindowDimensions());

  useEffect(() => {
    function handleResize() {
      setWindowDimensions(getWindowDimensions());
    }

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowDimensions;
}



function GraphComponent(props) {
  const {width } = useWindowDimensions();
  return (
      <LineChart
          width={width}
          height={props.height}
          data={props.data}
      >
        <XAxis dataKey="name"/>
        <YAxis/>
        <Text>{props.data_key}</Text>
        <CartesianGrid stroke="#eee" strokeDasharray="5 5"/>
        <Line type="monotone" dataKey={props.data_key} stroke="#8884d8" />
      </LineChart>
  )
}

export default GraphComponent;