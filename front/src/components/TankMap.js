import React, { useState, useEffect, useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Define custom icons for markers
var Icon1 = L.Icon.extend({
  options: {
    iconSize: [64, 64],
    popupAnchor: [0, -20],
  }
});

var Icon2 = L.Icon.extend({
  options: {
    iconSize: [30, 30],
    popupAnchor: [0, -20],
  }
});

// Create instances of custom icons
var storehouse_icon = new Icon1({
  iconUrl: "https://img.icons8.com/external-flatart-icons-flat-flatarticons/104/external-storehouse-agriculture-flatart-icons-flat-flatarticons.png",
});

var tank_icon = new Icon2({
  iconUrl: "https://img.icons8.com/arcade/64/marker.png"
});

function TankMap({ storehouse, cycles }) {
  // Get storehouse position
  const storehousePosition = useMemo(() => {
    return [storehouse.latitude, storehouse.longitude];
  }, [storehouse.latitude, storehouse.longitude]);

  useEffect(() => {
    // Your existing useEffect logic
  }, [storehousePosition]);
  // State to store routes for each cycle
  const [routes, setRoutes] = useState([]);
  // Define colors for cycle routes
  const colors = ['red', 'brown', 'green', 'purple', "black"];

  useEffect(() => {
    // Generate routes for each cycle based on tank coordinates
    const newRoutes = cycles.flatMap((cycle, cycleIndex) => {
      const tankPositions = cycle.selected_tanks_coodinates.map((tank) => [tank[0], tank[1]]);
      const depotToFirstTank = [
        storehousePosition,
        [tankPositions[0][0], tankPositions[0][1]]
      ];
  
      const cycleRoutes = tankPositions.reduce((acc, currentPosition, index, array) => {
        if (index < array.length - 1) {
          const nextPosition = array[index + 1];
          return [...acc, [currentPosition, nextPosition]];
        }
        // Add the route from the last tank to the depot
        return [...acc, [currentPosition, storehousePosition]];
      }, [depotToFirstTank]);
  
      return { cycleRoutes, cycleIndex };
    });
    setRoutes(newRoutes);
  }, [cycles, storehousePosition]);

  return (
    <MapContainer center={storehousePosition} zoom={13} style={{ height: "780px", width: "100%", margin: '10px 0px 30px 0px', justifiyContent: "center",border:"3px solid grey", borderRadius: '19px'}}>
      {/* Display the map with OpenStreetMap tiles */}
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {/* Display the storehouse marker with a popup */}
      <Marker position={storehousePosition} icon={storehouse_icon}>
        <Popup>
          Depot
        </Popup>
      </Marker>
      {/* Display markers for each tank and popups with tank information */}
      {cycles.map((cycle, cycleIndex) => (
        <React.Fragment key={cycleIndex}>
          {cycle.selected_tanks_coodinates.map((tank, tankIndex) => (
            <Marker key={tankIndex} position={[tank[0], tank[1]]} icon={tank_icon}>
              <Popup>
                <p>Tank: {cycle.selected_tanks_ids[tankIndex]} </p>
                <p>Cycle: {cycleIndex + 1}</p>
                <p>Coordinates: {cycle.selected_tanks_coodinates[tankIndex][0]}, {cycle.selected_tanks_coodinates[tankIndex][1]}</p>
              </Popup>
            </Marker>
          ))}
        </React.Fragment>
      ))}
      {/* Display polylines for each cycle route */}
      {routes.map(({ cycleRoutes, cycleIndex }) => (
        <Polyline key={cycleIndex} positions={cycleRoutes} color={colors[cycleIndex % colors.length]} />
      ))}
    </MapContainer>
  );
}

export default TankMap;
