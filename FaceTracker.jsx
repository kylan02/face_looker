import React, { useRef, useState } from 'react';
import useGazeTracking from './useGazeTracking';
import './FaceTracker.css'; // Optional styling

/**
 * FaceTracker Component
 * Displays a face that follows mouse/touch movement
 */
export default function FaceTracker({ 
  className = '', 
  basePath = '/faces/',
  showDebug = false 
}) {
  const containerRef = useRef(null);
  const { currentImage, isLoading, error } = useGazeTracking(containerRef, basePath);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e) => {
    if (!containerRef.current) return;
    
    const rect = containerRef.current.getBoundingClientRect();
    setMousePos({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    });
  };

  if (error) {
    return (
      <div className="face-tracker-error">
        Error loading face images: {error.message}
      </div>
    );
  }

  return (
    <div 
      ref={containerRef}
      className={`face-tracker ${className}`}
      onMouseMove={handleMouseMove}
    >
      {currentImage && (
        <img
          src={currentImage}
          alt="Face following gaze"
          className="face-image"
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            transition: 'opacity 0.1s ease-out'
          }}
        />
      )}
      
      {isLoading && (
        <div className="face-loading">
          Loading face...
        </div>
      )}

      {showDebug && (
        <div className="face-debug">
          <div>Mouse: ({Math.round(mousePos.x)}, {Math.round(mousePos.y)})</div>
          <div>Image: {currentImage?.split('/').pop()}</div>
        </div>
      )}
    </div>
  );
}
