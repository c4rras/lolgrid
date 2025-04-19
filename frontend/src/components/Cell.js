import React, { useState } from 'react';
import './Cell.css';

const Cell = ({ rowIndex, colIndex, cellData, guesses, setGuesses, infiniteMode }) => {
  const [input, setInput] = useState('');
  const [status, setStatus] = useState('');

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    if (guesses <= 0 && !infiniteMode) return;
    const isCorrect = cellData.answer.some(answer => answer.toLowerCase() === input.toLowerCase());
    setStatus(isCorrect ? 'correct' : 'incorrect');
    if (!isCorrect && !infiniteMode) {
      setGuesses(guesses - 1);
    }
  };

  return (
    <div className={`cell ${status}`}>
      {status !== 'correct' ? (
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          disabled={guesses <= 0 && !infiniteMode}
        />
      ) : (
        <span>{input}</span>
      )}
    </div>
  );
};

export default Cell; 