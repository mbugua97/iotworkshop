import { useState, useEffect } from 'react';
import './App.css';

import Throtted from './throtted.component';
import Ready from './ready.component';
import OnMode from './on';
import OffMode from './off';

const url = "http://16.16.70.217:8200/"; 
const wss = "ws://16.16.70.217:8200/ws/bulbstate/"; 

function App() {
  const [bulbState, setBulbState] = useState('');
  const [errors, setError] = useState('');
  const [socket, setSocket] = useState(null);
  const fetchBulbState = async () => {
    try {
      const response = await fetch(url); 
      const data = await response.json();
      if (data.state.state==true){
        setBulbState("on"); 
      }
      else{
        setBulbState("off"); 
      }
      setError('')
      
    } catch (error) {
      setError(error);
    }
  };


  useEffect(() => {
    const ws = new WebSocket(wss); 
    ws.onopen = () => {
      console.log('WebSocket connection established');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.state.state==true){
        setBulbState("on"); 
      }
      else{
        setBulbState("off"); 
      }
      setError('')
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    setSocket(ws);

    fetchBulbState();

    return () => {
      ws.close();
    };
  }, []);

  const handleTurnOn = async () => {
    try {
      const response = await fetch(`${url}`, { 
        method: 'POST',
        data: { "state":"true" } // Send action data
      });
      console.log(response);

      if (response.ok) {
        setBulbState('on'); 
      } else {
        setError("error");
      }
    } catch (error) {
      console.error('Error turning on the bulb:', error);
    }
  };

  const handleTurnOff = async () => {
    try {
      const response = await fetch(`${url}`, { 
        method: 'POST',
        data: { "state":"false" } 
      });

      if (response.ok) {
        setBulbState('off');
      } else {
        setError("error");
      }
    } catch (error) {
      console.log(error.data);
      setError(error);
    }
  };


console.log(bulbState);
console.log(errors);
  return (
    <div>
      <div className='header'>
        <div>
       <h2>IOT Onboarding Workshop</h2>
       </div>
       <div>
    </div>
      </div>
      <div>
        {errors=="error"?<Throtted/>:<Ready/>}
      </div>

      <div className='buttons'>

        <div>
          <button className='onbutton' onClick={handleTurnOn}>Turn On</button>
        </div>
        <div >
          <button className='offbutton' onClick={handleTurnOff}>Turn Off</button>
        </div>        
      </div>

      <div className='Bulbstate'>
        <p>Current Bulb State: {bulbState=="on"?<OnMode/>:<OffMode/>}</p>
      </div>
    </div>
  );
}
export default App;
