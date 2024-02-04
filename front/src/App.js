import React, { useEffect, useState } from 'react';
import TankMap from './components/TankMap';

function App() {
  const [result, setResult] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/run-main');
        const data = await response.json();
        setResult(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData(); // Appel initial

    const interval = setInterval(() => {
      fetchData(); // Appel chaque seconde
    }, 1000);

    // Nettoyage de l'intervalle
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      {result ? (
        <div>
          <h2>Score : {result.evaluation}</h2>
          <h1>Résultat de la fonction main :</h1>
          <pre>{JSON.stringify(result.journey, null, 2)}</pre>
          <TankMap storehouse={result.storehouse} cycles={result.journey.cycles} />
        </div>
      ) : (
        <p>Chargement...</p>
      )}
    </div>
  );
}

export default App;
