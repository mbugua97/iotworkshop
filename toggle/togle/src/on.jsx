import React from 'react';
import glowingBlueMarker from './assets/red.json';

const MapMarkers = () => {
  const renderMarker = (markerData) => {
    const { type, shape, style, position, videoUrl } = markerData.marker;
    return (
      <div
        key={position.latitude + position.longitude} 
        style={{
          width: '50px',
          height: '50px',
          borderRadius: shape === 'round' ? '50%' : '0',
          backgroundColor: style.backgroundColor,
          boxShadow: style.glow ? `0 0 10px ${style.glowColor}` : 'none',
          position: 'absolute',
          top: `${position.latitude}px`, 
          left: `${position.longitude}px`, 
        }}
      >
        <video width="100%" height="100%" controls>
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>
    );
  };

  return (
    <div>
      <h1>Map Markers</h1>
      <div style={{ position: 'relative', height: '400px', width: '600px' }}>
        {renderMarker(glowingBlueMarker)}
      </div>
    </div>
  );
};

export default MapMarkers;

