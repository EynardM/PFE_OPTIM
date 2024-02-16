import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const PlanningPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { result } = location.state || {}; // récupérer le résultat depuis l'état de la location

  const [currentHillClimbingJourney, setCurrentHillClimbingJourney] = useState(0);
  const [currentSimulatedAnnealingJourney, setCurrentSimulatedAnnealingJourney] = useState(0);


  const handleNavigateToMapPageHC = () => {
    // Navigate to the page you want
    // For example, navigate('/another-page');
    navigate('/', { state: { result }});
  };

  const handleNavigateToMapPageSA = () => {
    // Navigate to the page you want
    // For example, navigate('/another-page');
    navigate('/sa', { state: { result }});
  };



  const goToPreviousHillClimbingJourney = () => {
    setCurrentHillClimbingJourney(prevIndex => Math.max(prevIndex - 1, 0));
  };

  const goToNextHillClimbingJourney = () => {
    setCurrentHillClimbingJourney(prevIndex =>
      Math.min(prevIndex + 1, result.hill_climbing_results.journey_1.length - 1)
    );
  };

  const goToPreviousSimulatedAnnealingJourney = () => {
    setCurrentSimulatedAnnealingJourney(prevIndex => Math.max(prevIndex - 1, 0));
  };

  const goToNextSimulatedAnnealingJourney = () => {
    setCurrentSimulatedAnnealingJourney(prevIndex =>
      Math.min(prevIndex + 1, result.simulated_annealing_results.journey_1.length - 1)
    );
  };

  return (
    <div className="container">
      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <h1 style={{ color: 'black', fontSize: '40px', }}>Schedule</h1>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', margin: '20px'}}>
        <div style={{ flex: 1}}>
          <h1 style={{ color: 'black', textAlign: 'center' }}>Hill Climbing</h1>
          <div style={{ backgroundColor: '#333', color: '#fff', padding: '20px',borderRadius : "19px"  }}>
            {result && result.hill_climbing_results && result.hill_climbing_results.journey_1 && (
              result.hill_climbing_results.journey_1[currentHillClimbingJourney].cycles.map((cycle, cycleIndex) => (
                <div key={cycleIndex} style={{
                  backgroundColor: '#888',
                  border: '2px solid #777',
                  margin: '10px',
                  padding: '10px',
                  borderRadius: '19px',
                }}>
                  <h3 className="starting-time" style={{
                    backgroundColor: '#444',
                    color: '#fff',
                    padding: '5px',
                    margin: '0',
                    textAlign: 'left',
                  }}>{cycle.starting_time}</h3>
                  {cycle.selected_tanks_ids.map((tankId, tankIndex) => (
                    <h4 key={tankIndex} style={{
                      backgroundColor: '#666',
                      color: '#fff',
                      padding: '5px',
                      margin: '5px 0',
                      textAlign: 'center',
                    }}>{tankId}</h4>
                  ))}
                  <h3 className="ending-time" style={{
                    backgroundColor: '#444',
                    color: '#fff',
                    padding: '5px',
                    margin: '0',
                    textAlign: 'left',
                  }}>{cycle.ending_time}</h3>
                </div>
              ))
            )}
            <div style={{ textAlign: 'center', marginTop: '10px' }}>
                <button
                    onClick={goToPreviousHillClimbingJourney}
                    style={{
                        backgroundColor: '#3498db',
                        color: '#fff',
                        padding: '10px 15px',
                        border: 'none',
                        borderRadius: '15px',
                        cursor: 'pointer',
                        margin: '0 10px',
                        fontSize: '22px',
                    }}
                >
                    Previous
                </button>
                <button
                    onClick={goToNextHillClimbingJourney}
                    style={{
                        backgroundColor: '#3498db',
                        color: '#fff',
                        padding: '10px 15px',
                        border: 'none',
                        borderRadius: '15px',
                        cursor: 'pointer',
                        margin: '0 10px',
                        fontSize: '22px',
                    }}
                >
                    Next
                </button>
            </div>

          </div>
        </div>

        <div style={{ flex: 1, marginLeft: '20px'   }}>
          <h1 style={{ color: 'black', textAlign: 'center' }}>Recuit Simulé</h1>
          <div style={{ backgroundColor: '#333', color: '#fff', padding: '20px',borderRadius : "19px"  }}>
            {result && result.simulated_annealing_results && result.simulated_annealing_results.journey_1 && (
              result.simulated_annealing_results.journey_1[currentSimulatedAnnealingJourney].cycles.map((cycle, cycleIndex) => (
                <div key={cycleIndex} style={{
                  backgroundColor: '#888',
                  border: '2px solid #777',
                  margin: '10px',
                  padding: '10px',
                  borderRadius: '19px',
                }}>
                  <h3 className="starting-time" style={{
                    backgroundColor: '#444',
                    color: '#fff',
                    padding: '5px',
                    margin: '0',
                    textAlign: 'left',
                  }}>{cycle.starting_time}</h3>
                  {cycle.selected_tanks_ids.map((tankId, tankIndex) => (
                    <h4 key={tankIndex} style={{
                      backgroundColor: '#666',
                      color: '#fff',
                      padding: '5px',
                      margin: '5px 0',
                      textAlign: 'center',
                    }}>{tankId}</h4>
                  ))}
                  <h3 className="ending-time" style={{
                    backgroundColor: '#444',
                    color: '#fff',
                    padding: '5px',
                    margin: '0',
                    textAlign: 'left',
                  }}>{cycle.ending_time}</h3>
                </div>
              ))
            )}
            <div style={{ textAlign: 'center', marginTop: '10px' }}>
                <button
                    onClick={goToPreviousSimulatedAnnealingJourney}
                    style={{
                        backgroundColor: '#3498db',
                        color: '#fff',
                        padding: '10px 15px',
                        border: 'none',
                        borderRadius: '15px',
                        cursor: 'pointer',
                        margin: '0 10px',
                        fontSize: '22px',
                    }}
                >
                    Previous
                </button>
                <button
                    onClick={goToNextSimulatedAnnealingJourney}
                    style={{
                        backgroundColor: '#3498db',
                        color: '#fff',
                        padding: '10px 15px',
                        border: 'none',
                        borderRadius: '15px',
                        cursor: 'pointer',
                        margin: '0 10px',
                        fontSize: '22px',
                    }}
                >
                    Next
                </button>
            </div>
          </div>
        </div>
      </div>

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
          marginTop: '50px',
          margin: '50px auto 0',  // Ajout de cette ligne pour centrer le bouton horizontalement
          display: 'block',
        }}
      >
        Go To Hill Climbing Results
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
          marginTop: '20px',  // Adjusted margin for the duplicated button
          margin: '20px auto 0',  // Ajout de cette ligne pour centrer le bouton horizontalement
          marginBottom : "20px",
          display: 'block',
      }}
    >
      Go To Simulated Annealing
    </button>
    </div>
  );
};

export default PlanningPage;