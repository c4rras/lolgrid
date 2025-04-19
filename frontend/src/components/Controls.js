import React from 'react';
import './Controls.css';

const Controls = ({ guesses, setInfiniteMode }) => {
  const toggleInfiniteMode = () => {
    setInfiniteMode((prevMode) => !prevMode);
  };

  return (
    <div className="controls">
      <button onClick={toggleInfiniteMode}>Toggle Infinite Mode</button>
      <p>Guesses Left: {guesses}</p>
    </div>
  );
};

export default Controls; 