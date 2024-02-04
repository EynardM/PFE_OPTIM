// HelloWorld.js

import {React, useState, useEffect} from 'react';
import TankMap from './TankMap';
import MultiSliderComponent from './MultiSliderComponent';
import { useNavigate } from 'react-router-dom';

const MapPage = () => {
    const [result, setResult] = useState(null);
    const navigate = useNavigate();

    // utile pour récupérer que la première itération
    const [hasFetchedData, setHasFetchedData] = useState(false);
  
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch('http://localhost:8000/run-main');
          const data = await response.json();
          setResult(data);
          // utile pour récupérer que la première itération
          setHasFetchedData(true);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      };
  
      if (!hasFetchedData) {
        fetchData(); // Appel initial
      }
  
      if (!hasFetchedData) {
        const interval = setInterval(() => {
          fetchData(); // Appel chaque seconde
        }, 1000);
  
        // Nettoyage de l'intervalle
        return () => clearInterval(interval);
      }
    
    }, [hasFetchedData]);
  
    const handleNavigate = () => {
        // Utilisez history.push pour naviguer vers la page Planning
        navigate('/planning');
      };


    return (
      <div className="App">
        {result ? (
          <div>
            <div style={{ display: 'flex'}}>
              {/* <div>
                <h1>Result:</h1>
                <pre>{JSON.stringify(result, null, 2)}</pre>
              </div> */}
                <TankMap storehouse={result.storehouse} cycles={result.journey.cycles} />
              
                <MultiSliderComponent />
                
            </div>
  
            <div>
              <button  onClick={handleNavigate} style= {{
                backgroundColor: '#000000',
                color: '#fff',
                padding: '20px 15px',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
                fontSize: '16px',
                marginTop: ' -155px',
                marginLeft: '30%',
                display: 'block'
                }}>
                  Emploi du Temps
              </button>
            </div>
          </div>
  
        ) : (
          <p>Chargement...</p>
        )}
      </div>
    );
  }

export default MapPage;
