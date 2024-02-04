// App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MapPage from './components/MapPage';
import PlanningPage from './components/PlanningPage';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<MapPage />} />
          <Route path="/planning" element={<PlanningPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
