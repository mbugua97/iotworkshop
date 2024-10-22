import React from 'react';
import stop from './assets/stop.json'
import Lottie from 'lottie-react';

function Throtted() {
  return (
    <div className='throtted'>
      <h2>throtted</h2>
      <Lottie
        animationData={stop}
        loop={true}
        style={{ width: 100, height: 70 }}
      />
    </div>
  );
}
export default Throtted;
