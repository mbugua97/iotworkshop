import React from 'react';
import Lottie from 'lottie-react';
import bulb from './assets/bulb.json'
function Ready() {
  return (
    <div className='throtted'>
      <h2>smart energy systems</h2>
      <Lottie
        animationData={bulb}
        loop={true}
        style={{ width: 100, height: 70 }}
      />
    </div>
  );
}

export default Ready;
