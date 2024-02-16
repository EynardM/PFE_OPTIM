// App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MapPageHC from './components/MapPageHC';
import MapPageSA from './components/MapPageSA';
import PlanningPage from './components/PlanningPage';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<MapPageHC />} />
          <Route path="/sa" element={<MapPageSA />} />
          <Route path="/planning" element={<PlanningPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
