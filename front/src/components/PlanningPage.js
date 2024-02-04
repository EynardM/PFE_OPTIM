// HelloWorld.js

import React from 'react';
import { useNavigate } from 'react-router-dom';


const PlanningPage = () => {
    const navigate = useNavigate();

    const handleNavigate = () => {
        // Utilisez history.push pour naviguer vers la page Planning
        navigate('/');
    };

return (
    <div>
        <button  onClick={handleNavigate} style= {{
            backgroundColor: '#000000',
            color: '#fff',
            padding: '20px 15px',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            fontSize: '16px',
            marginTop: ' 50px',
            marginLeft: '30%',
            display: 'block'
            }}>
            Map
        </button>
    </div>
  );
};

export default PlanningPage;
