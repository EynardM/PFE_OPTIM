import React, { useEffect, useState } from 'react';

const MultiSliderComponent = () => {
  const sliders = [
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
    // Ajoutez d'autres sliders au besoin
  ];

  const [sliderValues, setSliderValues] = useState({});

  const updateSliderValue = (sliderId, value) => {
    setSliderValues((prevValues) => ({
      ...prevValues,
      [sliderId]: value,
    }));

    // Sauvegarde de la valeur du slider dans le stockage local
    localStorage.setItem(sliderId, value);
  };

  useEffect(() => {
    sliders.forEach((slider) => {
      const storedValue = localStorage.getItem(slider.id);
      if (storedValue !== null) {
        updateSliderValue(slider.id, storedValue);
      }
    });
  }, []);
  
  const handleButtonClick = () => {
    // Cette fonction sera appelée lorsqu'on cliquera sur le bouton
    // Vous pouvez ajouter le traitement spécifique ici
    console.log('Bouton cliqué!');
  };

  return (
    <div className="slider-box">
      <h2>Parameters</h2>
      {sliders.map((slider) => (
        <div key={slider.id}>
          <label htmlFor={slider.id}>{slider.label}</label>
          <input
            type="range"
            id={slider.id}
            className="slider"
            min={slider.min}
            max={slider.max}
            value={sliderValues[slider.id]}
            onChange={(e) => updateSliderValue(slider.id, e.target.value)}
          />
          <p id={`sliderValue${slider.id}`}>{sliderValues[slider.id] || 50}</p>
        </div>
      ))}
      <button onClick={handleButtonClick}>Launch Map</button>
    </div>
  );
};

export default MultiSliderComponent;
