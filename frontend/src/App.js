import React, { useState, useEffect } from 'react';
import Grid from './components/Grid';
import Controls from './components/Controls';
import './App.css';

function App() {
  const [gridData, setGridData] = useState({ rows: [], columns: [], answers: {} });
  const [guesses, setGuesses] = useState(12);
  const [infiniteMode, setInfiniteMode] = useState(false);

  useEffect(() => {
    const today = new Intl.DateTimeFormat('en-CA', {
      timeZone: 'America/Sao_Paulo',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    }).format(new Date()).replace(/\//g, '-');

    console.log(`Fetching data for date: ${today}`);
  
    fetch(`http://localhost:8000/game/${today}`)
      .then(response => response.json())
      .then(data => {
        console.log(data); // Check the data structure
        setGridData(data);
      });
  }, []);

  return (
    <div className="App">
      <h1>LOL GRID</h1>
      <Grid gridData={gridData} guesses={guesses} setGuesses={setGuesses} infiniteMode={infiniteMode} />
      <Controls guesses={guesses} setInfiniteMode={setInfiniteMode} />
    </div>
  );
}

export default App;
