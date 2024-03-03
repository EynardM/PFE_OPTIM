import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const PlanningPageHC = () => {
  // React Router hook for navigation
  const navigate = useNavigate();

  // Navigation handlers to different pages
  const handleNavigateToMapPageHC = () => {
    navigate('/hc', { state: { result } });
  };

  const handleNavigateToMapPageSA = () => {
    navigate('/sa', { state: { result } });
  };

  const handleNavigateToSASchedule = () => {
    navigate('/sa_schedule', { state: { result } });
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

  // Convert minutes to time format
  const convertMinutesToTime = (minutes) => {
    const h = Math.floor(minutes / 60);
    const m = Math.floor(minutes % 60);
    const s = Math.floor((minutes * 60) % 60);
    const paddedM = m < 10 ? `0${m}` : m;
    return { h, paddedM, s };
  };

  // JSX structure for rendering the component
  return (
    <div className="page" style={{ display: "flex", justifyContent: "center", alignItems: "center", flexDirection: "column" }}>
      {/* Page title and logo*/}
      <div className='logo' style={{display:"flex", justifyContent:"flex-start"}}>
          <img style={{ width: '300px', height: 'auto', position: 'absolute',top: '20px', left: '20px'}} src="https://bincy.fr/_next/image?url=https%3A%2F%2Fadmin.bincy.fr%2Fuploads%2Fbincy_rvb_cc17b25177.png&w=1920&q=75" alt="Bincy Logo" />
        </div>
      <div className='titre' style={{ marginTop: '10px', textAlign: 'center' }}>
        <h1 style={{ color: 'black', fontSize: '40px', }}>Hill Climbing Schedule</h1>
      </div>

      {/* Planning block */}
      <div className="planning-block" style={{ backgroundColor: '#333', color: '#fff', padding: '20px', borderRadius: "19px" }}>
        <div className="planning-container">
          {/* Iterate over cycles and display cycle information */}
          {result.hill_climbing_results && (
            currentJourney[currentJourneyIndexInList].cycles.map((cycle, cycleIndex) => (
              <div className="cycle_containers" classnamekey={cycleIndex} style={{
                backgroundColor: '#888',
                border: '2px solid #777',
                margin: '10px',
                padding: '5px',
                borderRadius: '19px',
              }}>
                {/* Cycle header */}
                <div className='head-of-cycle' style={{ backgroundColor: "#444", display: "flex", flexDirection: "row", alignItems: "center", borderRadius: '19px 19px 0 0', }}>
                  <h3 className="starting-time" style={{
                    backgroundColor: '#444',
                    color: '#fff',
                    padding: "0px",
                    margin: "0px 600px 0px 5px",
                    borderRadius: '19px',
                  }}>{cycle.starting_time}</h3>
                  <h3 className="cycle-details" style={{
                    backgroundColor: '#444',
                    color: '#FFC069',
                    margin: '0',
                    padding: '5px',
                  }}>{`${convertMinutesToTime(cycle.cycle_time).h}h${convertMinutesToTime(cycle.cycle_time).paddedM}`}</h3>

                  <h3 className="cycle-details" style={{
                    backgroundColor: '#444',
                    color: '#FFC069',
                    margin: '0px 0px 0px 50px',
                    padding: '5px',
                  }}>{cycle.cycle_volume.toFixed(2)} L</h3>

                  <h3 className="cycle-details" style={{
                    backgroundColor: '#444',
                    color: '#FFC069',
                    margin: '0px 0px 0px 50px',
                    padding: '5px',
                  }}>{cycle.cycle_distance.toFixed(2)} km</h3>
                </div>

                {/* Display tanks in the cycle */}
                {cycle.selected_tanks_ids.map((tankId, tankIndex) => (
                  <h4 key={tankIndex} style={{
                    backgroundColor: '#666',
                    color: '#fff',
                    padding: '5px',
                    margin: '5px 0',
                    textAlign: 'center',
                  }}>{tankId}</h4>
                ))}

                {/* Display ending time of the cycle */}
                <h3 className="ending-time" style={{
                  backgroundColor: '#444',
                  borderRadius: '0 0 19px 19px ',
                  color: '#fff',
                  padding: '5px',
                  margin: '0',
                  textAlign: 'left',
                }}>{cycle.ending_time}</h3>
              </div>
            ))
          )}
        </div>

        {/* Planning buttons */}
        <div classname="planning-buttons" style={{ display: 'flex', justifyContent: 'center', alignItems: "center", padding: "10px 5px 15px 20px" }}>
          <button onClick={handlePreviousJourney} style={{
            backgroundColor: '#FF6347', 
            color: '#fff',
            padding: '20px 15px',
            border: 'none',
            borderRadius: '19px',
            cursor: 'pointer',
            fontSize: '22px',
            marginRight: '20px',
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#FF4500')} 
          onMouseOut={(e) => (e.target.style.backgroundColor = '#FF6347')} 
          >Previous Journey</button>

          <button onClick={handlePreviousJourneyInList} style={{
            backgroundColor: '#008080', 
            color: '#fff',
            padding: '20px 15px',
            border: 'none',
            borderRadius: '19px',
            cursor: 'pointer',
            fontSize: '22px',
            marginLeft: "20px",
            marginRight: "100px"
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#006666')} 
          onMouseOut={(e) => (e.target.style.backgroundColor = '#008080')} >Suboptimal Route</button>

          {/* Journey Details Table */}
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div style={{ display: "flex", flexDirection: "row" }}>
              <table style={{ borderCollapse: 'collapse', borderRadius: '19px', backgroundColor: "#B4B4B8" }}>
                <thead>
                  <tr>
                    <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#000000" }}>Journey Number</th>
                    <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#000000" }}>Optimized Journey</th>
                    <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#3E7C17" }}>Journey Score</th>
                    <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#0766AD" }}>Journey Time</th>
                    <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#0766AD" }}>Journey Volume</th>
                    <th style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#0766AD" }}>Journey Distance</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#000000" }}>{extractNumberFromJourney(journeyKeys[currentJourneyIndex])}</td>
                    <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#000000" }}>{currentJourneyIndexInList}</td>
                    <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#3E7C17" }}>{currentJourney[currentJourneyIndexInList].journey_score.toFixed(2)}</td>
                    <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#0766AD" }}>{currentJourney[currentJourneyIndexInList].journey_time.toFixed(2)} min</td>
                    <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#0766AD" }}>{currentJourney[currentJourneyIndexInList].journey_volume.toFixed(2)} L</td>
                    <td style={{ border: 'none', padding: '10px', textAlign: 'center', verticalAlign: 'middle', color: "#0766AD" }}>{currentJourney[currentJourneyIndexInList].journey_distance.toFixed(2)} km</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

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
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#006666')} 
          onMouseOut={(e) => (e.target.style.backgroundColor = '#008080')} 
          >Optimal Route</button>

          <button onClick={handleNextJourney} style={{
            backgroundColor: '#FF6347', 
            color: '#fff',
            padding: '20px 15px',
            border: 'none',
            borderRadius: '19px',
            cursor: 'pointer',
            fontSize: '22px',
            marginRight: '50px',
            marginLeft: "20px",
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#FF4500')} 
          onMouseOut={(e) => (e.target.style.backgroundColor = '#FF6347')} 
          >Next Journey </button>
        </div>
      </div>

      {/* Navigation buttons */}
      <div className='navigation-buttons' style={{ display: "flex", flexDirection: "row", justifyContent: "space-evenly", width: "50%", marginTop: "2%", marginBottom: "2%" }}>
        {/* Navigation buttons for different pages */}
        <button
          onClick={handleNavigateToMapPageHC}
          style={{
            backgroundColor: '#000000',
            color: '#fff',
            padding: '20px 15px',
            border: 'none',
            borderRadius: '19px',
            cursor: 'pointer',
            fontSize: '22px',
            display: 'block',
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#333333')}
          onMouseOut={(e) => (e.target.style.backgroundColor = '#000000')}
        >
          Hill Climbing Map
        </button>
        <button
          onClick={handleNavigateToMapPageSA}
          style={{
            backgroundColor: '#000000',
            color: '#fff',
            padding: '20px 15px',
            border: 'none',
            borderRadius: '19px',
            cursor: 'pointer',
            fontSize: '22px',
            display: 'block',
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#333333')}
          onMouseOut={(e) => (e.target.style.backgroundColor = '#000000')}
        >
          Simulated Annealing Map
        </button>

        <button
          onClick={handleNavigateToSASchedule}
          style={{
            backgroundColor: '#000000',
            color: '#fff',
            padding: '20px 15px',
            border: 'none',
            borderRadius: '19px',
            cursor: 'pointer',
            fontSize: '22px',
            display: 'block',
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#333333')}
          onMouseOut={(e) => (e.target.style.backgroundColor = '#000000')}
        >
          Simulated Annealing Schedule
        </button>
        <button
          onClick={handleNavigateToHomePage}
          style={{
            backgroundColor: '#000000',
            color: '#fff',
            padding: '20px 15px',
            border: 'none',
            borderRadius: '19px',
            cursor: 'pointer',
            fontSize: '22px',
            display: 'block',
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#333333')}
          onMouseOut={(e) => (e.target.style.backgroundColor = '#000000')}
        >
          Home Page
        </button>
      </div>
    </div>
  );
};

export default PlanningPageHC;
