// App.js
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MapPageHC from './components/MapPageHC';
import MapPageSA from './components/MapPageSA';
import PlanningPageHC from './components/PlanningPageHC.js';
import PlanningPageSA from './components/PlanningPageSA';
import HomePage from './components/HomePage';

function App() {
  
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/hc" element={<MapPageHC />} />
          <Route path="/sa" element={<MapPageSA />} />
          <Route path="/hc_schedule" element={<PlanningPageHC />} />
          <Route path="/sa_schedule" element={<PlanningPageSA />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
