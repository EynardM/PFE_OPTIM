import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const PlanningPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { result } = location.state || {}; // récupérer le résultat depuis l'état de la location

  const [currentHillClimbingJourney, setCurrentHillClimbingJourney] = useState(0);
  const [currentSimulatedAnnealingJourney, setCurrentSimulatedAnnealingJourney] = useState(0);

  const handleNavigate = () => {
    // Utilisez history.push pour naviguer vers la page MapPage
    navigate('/');
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
        <h1 style={{ color: '#fff' }}>Emplois du temps</h1>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', margin: '20px'}}>
        <div style={{ flex: 1}}>
          <h2 style={{ color: 'black', textAlign: 'center' }}>Hill Climbing</h2>
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
                        fontSize: '16px',
                    }}
                >
                    Précédent
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
                        fontSize: '16px',
                    }}
                >
                    Suivant
                </button>
            </div>

          </div>
        </div>

        <div style={{ flex: 1, marginLeft: '20px'   }}>
          <h2 style={{ color: 'black', textAlign: 'center' }}>Recuit Simulé</h2>
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
                        fontSize: '16px',
                    }}
                >
                    Précédent
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
                        fontSize: '16px',
                    }}
                >
                    Suivant
                </button>
            </div>
          </div>
        </div>
      </div>

      <button
        onClick={handleNavigate}
        style={{
          backgroundColor: '#000000',
          color: '#fff',
          padding: '20px 15px',
          border: 'none',
          borderRadius: '19px',
          cursor: 'pointer',
          fontSize: '16px',
          marginTop: '50px',
          margin: '50px auto 0',  // Ajout de cette ligne pour centrer le bouton horizontalement
          display: 'block',
        }}
      >
        Retour à la carte
      </button>
    </div>
  );
};

export default PlanningPage;