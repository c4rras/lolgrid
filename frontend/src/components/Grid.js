import React, { useState } from 'react';
import Cell from './Cell';
import './Grid.css';

const Grid = ({ gridData, guesses, setGuesses, infiniteMode }) => {
  const { rows = [], columns = [], answers = {} } = gridData;

  return (
    <div className="grid">
      <div className="grid-row">
        <div className="cell label"></div>
        {columns.map((col, colIndex) => (
          <div key={colIndex} className="cell label">{col.label}</div>
        ))}
      </div>
      {rows.map((row, rowIndex) => (
        <div key={rowIndex} className="grid-row">
          <div className="cell label">{row.label}</div>
          {columns.map((col, colIndex) => (
            <Cell
              key={colIndex}
              rowIndex={rowIndex}
              colIndex={colIndex}
              cellData={{ row, col, answer: answers[`${rowIndex}-${colIndex}`] }}
              guesses={guesses}
              setGuesses={setGuesses}
              infiniteMode={infiniteMode}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default Grid; 