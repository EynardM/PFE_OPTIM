import React, { useState, useEffect } from 'react';
import TankMap from './TankMap';
import { useNavigate } from 'react-router-dom';
import 'leaflet/dist/leaflet.css'; 

const extractNumberFromJourney = (journeyKey) => {
  const numericPart = journeyKey.replace(/[^0-9]/g, ''); // Replace non-numeric characters with an empty string
  return parseInt(numericPart, 10); // Parse the numeric part as an integer
};

const WaitingPage = () => (
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Waiting Page</title>
      <style>
        {`
          body {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
          }
          
          .loading-container {
            text-align: center;
          }
          
          .loading-spinner {
            border: 8px solid #f3f3f3;
            border-top: 8px solid #3498db;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
          }
          
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>
    </head>
    <body>
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    </body>
  </html>
);

const MapPageSA = () => {
  const [result, setResult] = useState(null);
  const [currentJourneyIndex, setCurrentJourneyIndex] = useState(0);
  const [currentJourneyIndexInList, setCurrentJourneyIndexInList] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/get_results');
        const data = await response.json();
        setResult(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();

  }, []); 

  const handleNavigate = () => {
    // Utilisez history.push pour naviguer vers la page Planning
    navigate('/planning', { state: { result }});

  };

  const handleNavigateToAnotherPage = () => {
    // Navigate to the page you want
    // For example, navigate('/another-page');
    navigate('/', { state: { result }});
  };

  if (!result || !result.hill_climbing_results) {
    // we should put here something interesting to watch for the people to use this
    return <WaitingPage />;
  }

  const journeys = result.simulated_annealing_results;
  const journeyKeys = Object.keys(journeys);
  const currentJourney = journeys[journeyKeys[currentJourneyIndex]];

  const handleNextJourney = () => {
    setCurrentJourneyIndex((prevIndex) => (prevIndex + 1) % journeyKeys.length);
    setCurrentJourneyIndexInList(0); 
  };

  const handlePreviousJourney = () => {
    setCurrentJourneyIndex((prevIndex) => (prevIndex - 1 + journeyKeys.length) % journeyKeys.length);
    setCurrentJourneyIndexInList(0); 
  };

  const handleNextJourneyInList = () => {
    setCurrentJourneyIndexInList((prevIndex) => (prevIndex + 1) % currentJourney.length);

  };
  
  const handlePreviousJourneyInList = () => {
    setCurrentJourneyIndexInList((prevIndex) => (prevIndex - 1 + currentJourney.length) % currentJourney.length);
  };  

 

  return (
    <div className="App">
      <style>
        {`
          body {
            overflow: hidden;
          }
        `}
      </style>
      <div style={{display: "flex", flexDirection: "column",  justifyContent: "center", alignItems:"center"}}>
        <div style={{ display: 'flex', justifyContent:"space-around",flexDirection: 'row' , marginTop:"20px"}}> 
          <h1 style={{ marginBottom: '20px', marginRight: "100px"}}>Simulated Annealing Results</h1>
          <button onClick={handleNavigateToAnotherPage} style={{
            backgroundColor: '#000000', // Green color for the button
            color: '#fff',
            padding: '20px 15px',
            border: 'none',
            borderRadius: '19px',
            cursor: 'pointer',
            fontSize: '22px',
          }}>Go To Hill Climbing Results</button>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
          <TankMap storehouse={result.storehouse} cycles={currentJourney[currentJourneyIndexInList].cycles} />
    
          <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '30px', marginTop : "0px", height:"200px" }}>
            <button onClick={handlePreviousJourney} style={{
              backgroundColor: '#FF6347', // Color for "Journey Précédente"
              color: '#fff',
              padding: '20px 15px',
              border: 'none',
              borderRadius: '19px',
              cursor: 'pointer',
              fontSize: '22px',
              marginRight: '20px', // Increased margin
              marginTop: "30px",
              marginBottom: "100px"
            }}>Previous Journey</button>
    
            <button onClick={handlePreviousJourneyInList} style={{
              backgroundColor: '#008080', // Color for "Previous Journey"
              color: '#fff',
              padding: '20px 15px',
              border: 'none',
              borderRadius: '19px',
              cursor: 'pointer',
              fontSize: '22px',
              marginRight: '20px', // Increased margin
              marginLeft : "20px",
              marginTop: "30px",
              marginBottom: "100px",
              marginRight: "100px"
            }}>Suboptimal Route</button>
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
              <div style={{ display:"flex",flexDirection: "row"}}>
                {/* <div>
                  <div style={{ marginBottom: '10px',fontSize: '22px' }}>Opimized Journey : {currentJourneyIndexInList}</div>
                  <div style={{fontSize: '22px'}}>Journey Number: {extractNumberFromJourney(journeyKeys[currentJourneyIndex])}</div>
                </div> */}
                <table style={{ borderCollapse: 'collapse', borderRadius: '19px', backgroundColor: "#f2f2f2" }}>
                  <thead>
                    <tr>
                      <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>Journey Number</th>
                      <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>Optimized Journey</th>
                      <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>Journey Time</th>
                      <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>Journey Volume</th>
                      <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>Journey Distance</th>
                      {/* Add more headers as needed */}
                    </tr>
                  </thead>
                  <tbody>
                    {/* Add rows with empty cells */}
                    <tr>
                      <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>{extractNumberFromJourney(journeyKeys[currentJourneyIndex])}</td>
                      <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>{currentJourneyIndexInList}</td>
                      <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>{currentJourney[currentJourneyIndexInList].journey_time.toFixed(2)}</td>
                      <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>{currentJourney[currentJourneyIndexInList].journey_volume.toFixed(2)}</td>
                      <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>{currentJourney[currentJourneyIndexInList].journey_distance.toFixed(2)}</td>
                      {/* Add more cells as needed */}
                    </tr>
                  </tbody>
                </table>


              </div>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
                <button onClick={handleNavigate} style={{
                  backgroundColor: '#000000',
                  color: '#fff',
                  padding: '20px 15px',
                  border: 'none',
                  borderRadius: '19px',
                  cursor: 'pointer',
                  fontSize: '22px',
                  marginTop: '40px', // Align to the bottom
                  

                  
                }}>Schedule</button>
              </div>

            </div>
            
    
            <button onClick={handleNextJourneyInList} style={{
              backgroundColor: '#008080', // Color for "Next Journey"
              color: '#fff',
              padding: '20px 15px',
              border: 'none',
              borderRadius: '19px',
              cursor: 'pointer',
              fontSize: '22px',
              marginRight: '20px', // Increased margin
              marginLeft : "100px",
              marginTop: "30px",
              marginBottom: "100px",

            }}>Optimal Route</button>
    
            <button onClick={handleNextJourney} style={{
              backgroundColor: '#FF6347', // Color for "Journey Suivante"
              color: '#fff',
              padding: '20px 15px',
              border: 'none',
              borderRadius: '19px',
              cursor: 'pointer',
              fontSize: '22px',
              marginRight: '50px', // Increased margin
              marginLeft : "20px",
              marginTop: "30px",
              marginBottom: "100px"
            }}>Next Journey </button>
          </div>
    
          
        </div>
      </div>
    </div>
  );
  
  
}
export default MapPageSA;
