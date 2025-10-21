import React from 'react';
import FaceTracker from '../../FaceTracker';
import './App.css';

/**
 * Example: Basic implementation of FaceTracker
 * 
 * This demonstrates the simplest way to use the face tracking component
 */
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Face Looker Demo</h1>
        <p>Move your mouse around the face below!</p>
      </header>

      <main className="App-main">
        {/* Basic usage - face in a container */}
        <div className="face-container">
          <FaceTracker basePath="/faces/" />
        </div>

        <div className="instructions">
          <h2>Try These:</h2>
          <ul>
            <li>Move your cursor around the screen</li>
            <li>Try on mobile with touch</li>
            <li>Move quickly vs slowly</li>
            <li>Go to the edges and corners</li>
          </ul>
        </div>

        {/* Debug mode enabled */}
        <div className="debug-container">
          <h3>Debug Mode</h3>
          <FaceTracker 
            basePath="/faces/" 
            showDebug={true}
            className="debug-face"
          />
        </div>
      </main>
    </div>
  );
}

export default App;

