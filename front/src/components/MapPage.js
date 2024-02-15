// HelloWorld.js

import {React, useState, useEffect,useRef} from 'react';
import TankMap from './TankMap';
import MultiSliderComponent from './MultiSliderComponent';
import { useNavigate } from 'react-router-dom';

const MapPage = () => {
    const [result, setResult] = useState(null);
    const navigate = useNavigate();

    
  // Use a ref to track whether data has been fetched
  const hasFetchedDataRef = useRef(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/get_results');
        const data = await response.json();
        console.log("result in the fetch", data);
        setResult(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Fetch data only if it hasn't been fetched yet
    if (!hasFetchedDataRef.current) {
      fetchData();
      // Set the flag to true after the first successful fetch using the ref
      hasFetchedDataRef.current = true;
    }

  }, []); // Empty dependency array to ensure the effect runs only once
  
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
              {console.log("i am bedore the tankmap",result.hill_climbing_results.journey_200[2].cycles[0].selected_tanks_coodinates[0])}
                <TankMap storehouse={result.storehouse} cycles={result.hill_climbing_results.journey_200[2].cycles} />
              
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
