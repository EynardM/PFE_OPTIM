import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import WaitingPage from "./WaitingPage";

const HomePage = () => {
  const navigate = useNavigate();
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    // Fetch data when component mounts
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/get_results');
        const data = await response.json();
        setResult(data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setIsLoading(false);
      }
    };

    // Check if data is available in location state
    if (location.state) {
      setResult(location.state.result);
      setIsLoading(false);
    } else {
      // Fetch data if not available in location state
      fetchData();
    }
  }, [result, location.state]);

   // Render loading screen while fetching data
   if (isLoading) {
    return <WaitingPage />;
  }

  // Navigation functions
  const handleNavigateToMapPageHC = () => {
    navigate('/hc', { state: { result } });
  };

  const handleNavigateToMapPageSA = () => {
    navigate('/sa', { state: { result } });
  };

  return (
    <div className="App" style={{boxSizing: 'border-box',display:"flex", flexDirection:"column", justifyContent:"center", alignItems:"center" }}>
      <div className='title' style={{ display: 'flex', justifyContent: "space-around", flexDirection: 'row', marginTop: "10px" }}>
          <h1 style={{ marginBottom: '50px',fontSize: '40px'}}>Welcome To Your Journey Visualisation App</h1>
        </div>

        <div className='text-box' style={{ fontFamily: 'Arial, sans-serif', maxWidth: '1800px', textAlign: 'justify', marginBottom: '50px', width: '100%', boxSizing: 'border-box', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between' }}>
          <p style={{ fontSize: '24px', marginBottom: '15px', width: '30%' }}>
          Explore and visualize potential journeys with our interactive app. Whether you are optimizing delivery routes, planning service calls, or coordinating business trips, our app provides insights and tools to make your journey planning efficient.
          </p>
          <p style={{ fontSize: '24px', marginBottom: '15px', width: '30%' }}>
            Unlock the power of data with our advanced algorithms. Dive into the results of hill climbing and simulated annealing to discover optimal routes, travel times, and more. Make informed decisions for your journey based on data-driven insights.
          </p>
          <p style={{ fontSize: '24px', marginBottom: '15px', width: '30%' }}>
            Plan your itinerary with ease. Our app offers sophisticated planning features that take into account various factors such as opened clients, oil volume, and emergency. Those schedules are built on a complete workday.
          </p>
        </div>


      <div style={{ width: '100%', maxWidth: '1800px', marginBottom: '50px', boxSizing: 'border-box', display: 'flex', justifyContent: 'space-around' }}>
        <img style={{ width: '1000px', height: 'auto', borderRadius: '8px' }} src="https://bincy.fr/_next/image?url=https%3A%2F%2Fadmin.bincy.fr%2Fuploads%2Fbincy_rvb_cc17b25177.png&w=1920&q=75" alt="Bincy Logo" />
      </div>

      <h2 style={{ margin: 0, fontSize: '36px', marginBottom: '20px', textAlign: 'center', }}>
        Why Choose Our App?
      </h2>

      <div className='text-box' style={{ fontFamily: 'Arial, sans-serif', maxWidth: '1800px', textAlign: 'justify', marginBottom: '50px', width: '100%', boxSizing: 'border-box', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between' }}>
        <p style={{ fontSize: '24px', marginBottom: '15px', width: '30%' }}>
          1. Advanced Algorithm: Our application employs a sophisticated, in-house algorithm that efficiently handles various constraints. It optimizes journeys based on real-time data and analytics, providing detailed metrics to showcase the optimization process.
        </p>
        <p style={{ fontSize: '24px', marginBottom: '15px', width: '30%' }}>
          2. Intuitive User Interface: Experience a user-friendly design that ensures a seamless and enjoyable journey visualization. View the optimized path on the map and easily check the planning details to determine its suitability for your needs.
        </p>
        <p style={{ fontSize: '24px', marginBottom: '15px', width: '30%' }}>
          3. Personalization Options: Customize your journey according to your preferences with our versatile algorithms. Explore numerous possibilities and prioritize variables that matter most to you.
        </p>
      </div>


      <div className="nav-button" style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', width: '100%', boxSizing: 'border-box', marginBottom:"40px" }}>
        <button
          onClick={handleNavigateToMapPageHC}
          style={{
            backgroundColor:'#000000',
            color: '#fff',
            padding: '20px 15px',
            border: 'none',
            borderRadius: '19px',
            cursor: 'pointer',
            fontSize: '22px',
            marginRight: "25px",
            marginLeft: "25px",
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = '#333333')}
          onMouseOut={(e) => (e.target.style.backgroundColor = '#000000')}
          >
          Explore with Hill Climbing
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
          marginRight: "25px",
          marginLeft: "25px",
        }}
        onMouseOver={(e) => (e.target.style.backgroundColor = '#333333')}
        onMouseOut={(e) => (e.target.style.backgroundColor = '#000000')}
        >
          Discover with Simulated Annealing
        </button>
      </div>
    </div>
  );
};

export default HomePage;
