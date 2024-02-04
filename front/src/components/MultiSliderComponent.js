import React, { useEffect, useState, useMemo } from 'react';

const MultiSliderComponent = () => {
  /* Sliders initialisation */
  const slidersData = [
    { id: 'slider1', label: 'Simulation Deep', min: 0, max: 100 },
    { id: 'slider2', label: 'Working Time', min: 0, max: 10 },
    { id: 'slider3', label: 'Mobile Tank Volume', min: 0, max: 400 },
    { id: 'slider4', label: 'Vehicle Speed', min: 0, max: 15 },
    { id: 'slider5', label: 'Loading Time', min: 0, max: 20 },
    { id: 'slider6', label: 'Pumping Speed', min: 0, max: 15 },
    { id: 'slider7', label: 'Draining Speed', min: 0, max: 15 },
    { id: 'slider8', label: 'Percentage Volume Threshold', min: 0, max: 100 },
    { id: 'slider9', label: 'Percentage Partial Collect Volume', min: 0, max: 100 },
    { id: 'slider10', label: 'Minimum Draining Volume', min: 0, max: 120 },
    { id: 'slider11', label: 'Average Cycle Time', min: 0, max: 5 },
  ];

  // Initialize sliders with their average values
  const initialSliderValues = slidersData.reduce((acc, slider) => {
    acc[slider.id] = (slider.min + slider.max) / 2;
    return acc;
  }, {});

  const [sliderValues, setSliderValues] = useState(initialSliderValues);

  const updateSliderValue = (sliderId, value) => {
    setSliderValues((prevValues) => ({
      ...prevValues,
      [sliderId]: value,
    }));

    // Sauvegarde de la valeur du slider dans le stockage local
    localStorage.setItem(sliderId, value);
  };

  // Include 'slidersData' in the dependency array for useMemo
  const memoizedSliders = useMemo(() => slidersData, [slidersData]);

  useEffect(() => {
    memoizedSliders.forEach((slider) => {
      const storedValue = localStorage.getItem(slider.id);
      if (storedValue !== null) {
        updateSliderValue(slider.id, storedValue);
      }
    });
  }, [memoizedSliders]);

  const handleButtonClick = async () => {
    try {
      const response = await fetch('http://localhost:8000/run-main');
      const data = await response.json();
      // Faire quelque chose avec les données retournées, si nécessaire
      console.log('Data after button click:', data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="slider-box" style={{
      border: '1px solid #000',
      margin: '10px 50px 50px 0px',
      padding: '10px 50px 10px 50px',
      backgroundColor: '#f0f0f0',
      borderRadius: '8px',
      boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
      textAlign: 'center', // Centrage des éléments dans la slider-box
    }}>
      <h2>Parameters</h2>
      {memoizedSliders.map((slider, index) => (
        <div key={slider.id} style={{ marginBottom: '15px' }}>
          <label htmlFor={slider.id}>{slider.label}</label>
          <input
            type="range"
            id={slider.id}
            className="slider"
            min={slider.min}
            max={slider.max}
            value={sliderValues[slider.id]}
            onChange={(e) => updateSliderValue(slider.id, e.target.value)}
            style={{
              width: '100%',
              marginBottom: '5px',
            }}
          />
          <p id={`sliderValue${slider.id}`} style={{ marginBottom: '20px', marginTop: '-10px', fontWeight: 'bold'}}>{sliderValues[slider.id]}</p>
        </div>
      ))}
      <button onClick={handleButtonClick} style={{
        backgroundColor: '#000000',
        color: '#fff',
        padding: '10px 15px',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        fontSize: '16px',
        marginTop: '15px', 
      }}>
        Launch Algorithm
      </button>
    </div>
  );
  
  
  
};

export default MultiSliderComponent;
