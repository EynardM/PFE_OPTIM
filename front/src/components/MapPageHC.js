import React, { useState } from 'react';
import TankMap from './TankMap';
import { useNavigate, useLocation } from 'react-router-dom';
import 'leaflet/dist/leaflet.css';

const MapPageHC = () => {
  const navigate = useNavigate();
  
  // Navigation handlers
  const handleNavigateToMapPageSA = () => {
    navigate('/sa', { state: { result } });
  };

  const handleNavigateToPlanningHC = () => {
    navigate('/hc_schedule', { state: { result } });
  };

  const handleNavigateToHomePage = () => {
    navigate('/', { state: { result } });
  };

  // Retrieve data from the location state
  const location = useLocation();
  const { result } = location.state || {};
  const [currentJourneyIndex, setCurrentJourneyIndex] = useState(0);
  const [currentJourneyIndexInList, setCurrentJourneyIndexInList] = useState(0);

  // Extracting journey information
  const journeys = result.hill_climbing_results;
  const journeyKeys = Object.keys(journeys);
  const currentJourney = journeys[journeyKeys[currentJourneyIndex]];

  // Journey navigation handlers
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

  // Extract numeric part from journey key
  const extractNumberFromJourney = (journeyKey) => {
    const numericPart = journeyKey.replace(/[^0-9]/g, '');
    return parseInt(numericPart, 10);
  };

  return (
    <div className="App">
      <div style={{position:"relative", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
        {/* Page title adn logo */}
        <div className='logo' style={{display:"flex", justifyContent:"flex-start"}}>
          <img style={{ width: '300px', height: 'auto', position: 'absolute',top: '20px', left: '20px'}} src="https://bincy.fr/_next/image?url=https%3A%2F%2Fadmin.bincy.fr%2Fuploads%2Fbincy_rvb_cc17b25177.png&w=1920&q=75" alt="Bincy Logo" />
        </div>
        <div className='title' style={{ display: 'flex', justifyContent: "space-around", flexDirection: 'row', marginTop: "10px" }}>
          <h1 style={{ marginBottom: '20px',fontSize: '40px' }}>Hill Climbing Map</h1>
        </div>

        {/* Map and Journey Details */}
        <div className='map-panel' style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <TankMap storehouse={result.storehouse} cycles={currentJourney[currentJourneyIndexInList].cycles} />

          {/* Journey Navigation and Details */}
          <div className='navigation-panel' style={{ display: 'flex', justifyContent: 'center', marginBottom: '30px', marginTop: "0px", height: "200px" }}>
            {/* Previous Journey Button */}
            <button onClick={handlePreviousJourney} style={{
              backgroundColor: '#FF6347',
              color: '#fff',
              padding: '20px 15px',
              border: 'none',
              borderRadius: '19px',
              cursor: 'pointer',
              fontSize: '22px',
              marginRight: '20px',
              marginTop: "30px",
              marginBottom: "100px"
              }}
              onMouseOver={(e) => (e.target.style.backgroundColor = '#FF4500')} 
              onMouseOut={(e) => (e.target.style.backgroundColor = '#FF6347')} 
            >Previous Journey</button>

            {/* Suboptimal Route Button */}
            <button onClick={handlePreviousJourneyInList} style={{
              backgroundColor: '#008080',
              color: '#fff',
              padding: '20px 15px',
              border: 'none',
              borderRadius: '19px',
              cursor: 'pointer',
              fontSize: '22px',
              marginLeft: "20px",
              marginTop: "30px",
              marginBottom: "100px",
              marginRight: "100px"
            }}
            onMouseOver={(e) => (e.target.style.backgroundColor = '#006666')} 
            onMouseOut={(e) => (e.target.style.backgroundColor = '#008080')} 
            >Suboptimal Route</button>

            {/* Journey Details Table */}
            <div className='data-and-button' style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
              <div className='data-table' style={{ display: "flex", flexDirection: "row",borderRadius: '19px', border: '2px solid grey', overflow: 'hidden' }}>
                <table style={{ borderCollapse: 'collapse', backgroundColor: "#E3E1D9" }}>
                  <thead>
                    <tr>
                      <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>Journey Number</th>
                      <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>Optimized Journey</th>
                      <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#539165" }}>Journey Score</th>
                      <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#3085C3" }}>Journey Time</th>
                      <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#3085C3" }}>Journey Volume</th>
                      <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#3085C3" }}>Journey Distance</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>{extractNumberFromJourney(journeyKeys[currentJourneyIndex])}</td>
                      <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle' }}>{currentJourneyIndexInList}</td>
                      <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#539165" }}>{currentJourney[currentJourneyIndexInList].journey_score.toFixed(2)}</td>
                      <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#3085C3" }}>{currentJourney[currentJourneyIndexInList].journey_time.toFixed(2)} min</td>
                      <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#3085C3" }}>{currentJourney[currentJourneyIndexInList].journey_volume.toFixed(2)} L</td>
                      <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#3085C3" }}>{currentJourney[currentJourneyIndexInList].journey_distance.toFixed(2)} km</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Navigation Buttons */}
              <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'flex-end' }}>
                {/* Hill Climbing Schedule Button */}
                <button onClick={handleNavigateToPlanningHC} style={{
                  backgroundColor: '#000000',
                  color: '#fff',
                  padding: '20px 15px',
                  border: 'none',
                  borderRadius: '19px',
                  cursor: 'pointer',
                  fontSize: '22px',
                  marginTop: '40px',
                  marginRight: "25px",
                  marginLeft: "25px"
                }}
                onMouseOver={(e) => (e.target.style.backgroundColor = '#333333')}
                onMouseOut={(e) => (e.target.style.backgroundColor = '#000000')}
                >Hill Climbing Schedule</button>

                {/* Simulated Annealing Map Button */}
                <button onClick={handleNavigateToMapPageSA} style={{
                  backgroundColor: '#000000',
                  color: '#fff',
                  padding: '20px 15px',
                  border: 'none',
                  borderRadius: '19px',
                  cursor: 'pointer',
                  fontSize: '22px',
                  marginRight: "25px",
                  marginLeft: "25px"
                }}
                onMouseOver={(e) => (e.target.style.backgroundColor = '#333333')}
                onMouseOut={(e) => (e.target.style.backgroundColor = '#000000')}
                >Simulated Annealing Map</button>

                {/* Home Page Button */}
                <button onClick={handleNavigateToHomePage} style={{
                  backgroundColor: '#000000',
                  color: '#fff',
                  padding: '20px 15px',
                  border: 'none',
                  borderRadius: '19px',
                  cursor: 'pointer',
                  fontSize: '22px',
                  marginRight: "25px",
                  marginLeft: "25px"
                }}
                  onMouseOver={(e) => (e.target.style.backgroundColor = '#333333')}
                  onMouseOut={(e) => (e.target.style.backgroundColor = '#000000')}
                >Home Page</button>
              </div>
            </div>

            {/* Optimal Route Button */}
            <button onClick={handleNextJourneyInList} style={{
              backgroundColor: '#008080',
              color: '#fff',
              padding: '20px 15px',
              border: 'none',
              borderRadius: '19px',
              cursor: 'pointer',
              fontSize: '22px',
              marginRight: '20px',
              marginLeft: "100px",
              marginTop: "30px",
              marginBottom: "100px",
            }}
            onMouseOver={(e) => (e.target.style.backgroundColor = '#006666')} 
            onMouseOut={(e) => (e.target.style.backgroundColor = '#008080')} 
            >Optimal Route</button>

            {/* Next Journey Button */}
            <button
              onClick={handleNextJourney}
              style={{
                backgroundColor: '#FF6347',
                color: '#fff',
                padding: '20px 15px',
                border: 'none',
                borderRadius: '19px',
                cursor: 'pointer',
                fontSize: '22px',
                marginLeft: '20px',
                marginTop: '30px',
                marginBottom: '100px',
                transition: 'background-color 0.3s ease', // Add transition for smooth effect
              }}
              onMouseOver={(e) => (e.target.style.backgroundColor = '#FF4500')} // Change color on hover
              onMouseOut={(e) => (e.target.style.backgroundColor = '#FF6347')} // Restore original color on mouse out
              >
              Next Journey
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MapPageHC;
