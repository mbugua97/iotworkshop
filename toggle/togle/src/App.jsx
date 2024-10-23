import { useState, useEffect } from 'react';
import './App.css';

import MapMarkers from './on';

import Throtted from './throtted.component';
import Ready from './ready.component';
import OnMode from './on';
import OffMode from './off';

const url = "http://16.16.70.217:8200/"; 
const wss = "ws://16.16.70.217:8200/ws/bulbstate/";

function App() {
  const [bulbState, setBulbState] = useState('');
  const [errors, setError] = useState('');

  const fetchBulbState = async () => {
    try {
      const response = await fetch(url); 
      const data = await response.json();
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
      console.log(data.state);
      if (data.state ==true) {
        console.log("turned on");
        setBulbState("on");
      } else if (data.state== false) {
        setBulbState("off");
      }
      setError('');
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    fetchBulbState();

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
        <div>
          <h2>IOT Onboarding Workshop</h2>
        </div>
      </div>

      <div>
        {errors === "error" ? <Throtted /> : <Ready />}
      </div>

      <div className='buttons'>
        <div>
          <button className='onbutton' onClick={handleTurnOn}>Turn On</button>
        </div>
        <div>
          <button className='offbutton' onClick={handleTurnOff}>Turn Off</button>
        </div>
      </div>

      <div className='Bulbstate'>
        <p>Current Bulb State: {bulbState}</p>
      </div>
    </div>
  );
}

export default App;
