import { useState, useEffect } from 'react';
import './App.css';

import environment from './assets/environment.json'

import Throtted from './throtted.component';
import Ready from './ready.component';
import Lottie from 'lottie-react';

const url = "http://16.16.70.217:8200/";
const wss = "ws://16.16.70.217:8200/ws/bulbstate/";


function App() {
  const [bulbState, setBulbState] = useState('');
  const [Temp, setTemp] = useState('');
  const [Hum, setHum] = useState('');
  const [voltage, setvolt] = useState('');
  const [current, setamp] = useState('');
  const [Pressure, setPres] = useState('');
  const [moisture, setMois] = useState('');
  const [freq, setfreq] = useState('');
  const [errors, setError] = useState('');

  const fetchTemp = async () => {
    try {
      const response = await fetch(`${url}temp/`); 
      const data = await response.json();
      
      // Assuming API returns the values like this
      setTemp(data.state.temprature);
      setHum(data.state.humidity); 
      setPres(data.state.pressure); 
      setMois(1023-data.state.moisture ); // Adjusted as per your logic
      setfreq(data.state.frequency);  
    } catch (error) {
      console.log("Error fetching temperature data:", error);
      setError("error");
    }
  };

  const fetchBulbState = async () => {
    try {
      const response = await fetch(url); 
      const data = await response.json();
      
      // Check the state and set accordingly
      if (data.state.state === true) {
        setBulbState("on");
      } else {
        setBulbState("off");
      }
      setError('');
    } catch (error) {
      setError("error");
    }
  };

  useEffect(() => {
    const ws = new WebSocket(wss);
    
    ws.onopen = () => {
      console.log('WebSocket connection established');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log(data);
      const countProperties = (obj) => {
        return Object.keys(obj).length;
      };

      const propert=countProperties(data);

      if (propert==2) {
        if (data.state === true) {
          console.log("Bulb turned on");
          setBulbState("on");
        } else if (data.state === false) {
          setBulbState("off");
        }
      }
      if(propert==6){
        console.log(data);
        setTemp(data.temprature);
        setHum(data.humidity); 
        setPres(data.pressure); 
        setMois(1023-data.moisture); // Adjusted as per your logic
        setfreq(data.frequency);  
      }
    
      setError('');
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    fetchBulbState();
    fetchTemp();

    return () => {
      ws.close();
    };
  }, []);

  const handleTurnOn = async () => {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: true }),
      });

      if (response.ok) {
        setBulbState('on');
      } else {
        setError("error");
      }
    } catch (error) {
      console.error('Error turning on the bulb:', error);
      setError("error");
    }
  };

  const handleTurnOff = async () => {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: false }),
      });

      if (response.ok) {
        setBulbState('off');
      } else {
        setError("error");
      }
    } catch (error) {
      console.error('Error turning off the bulb:', error);
      setError("error");
    }
  };

  return (
    <div>
      <div className='header'>
        <h2>IOT Onboarding Workshop</h2>
      </div>

<div className='bulb'>
      <div>
        {errors === "error" ? <Throtted /> : <Ready />}
      </div>

<div className='butonsbulb'>
<div className='buttons'>
  <button 
    className='onbutton' 
    style={bulbState === "on" ? {} : { backgroundColor: 'grey', color: 'white' }} 
    onClick={handleTurnOn}>
    Turn On
  </button>
  
  <button 
    className='offbutton' 
    style={bulbState === "off" ? {} : { backgroundColor: 'gray', color: 'white' }} 
    onClick={handleTurnOff}>
    Turn Off
  </button>
</div>

      <div className='Bulbstate'>
        <p>Current Bulb State: {bulbState}</p>
      </div>

</div>
      <div className='voltsamps'>
        <div>voltage:{voltage}</div>
        <div>current:{current}</div>
      </div>



  </div>

<div className='sensor-data'>
        <div>
        <Lottie
        animationData={environment}
        loop={true}
        style={{ width: 100, height: 70 }}
      />
        </div>
        <div className='Termprature'>
      
<div><p>Temperature: {Temp} °C</p></div>      
<div><p>Humidity: {Hum} %</p></div>
<div><p>Pressure: {Pressure} hPa</p></div>
<div> <p>Moisture: {moisture}</p></div>
      </div>
      </div>
      </div>
 
  );
}

export default App;
