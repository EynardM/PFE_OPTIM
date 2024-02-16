import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Icons
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

var storehouse_icon = new Icon1({
  iconUrl: "https://img.icons8.com/external-flatart-icons-flat-flatarticons/64/external-storehouse-agriculture-flatart-icons-flat-flatarticons.png",
});

var tank_icon = new Icon2({
  iconUrl: "https://img.icons8.com/arcade/64/marker.png"
});

function TankMap({ storehouse, cycles }) {
  const storehousePosition = [storehouse.latitude, storehouse.longitude];
  const [routes, setRoutes] = useState([]);
  const colors = ['red','brown', 'green', 'purple' ,"black"];

  useEffect(() => {
    // console.log("in the tank map",cycles)
    const newRoutes = cycles.flatMap((cycle, cycleIndex) => {
      // if (!cycle) {
      //   console.log('Cycles is undefined or null.');
      //   return;
      // }
      // cycles est 
      // {console.log("i am in the tank map",result.hill_climbing_results.journey_366[0].cycles[0].selected_tanks_coodinates[0])}
      // console.log("in the tankmap",cycle.selected_tanks_coodinates)
      const tankPositions = cycle.selected_tanks_coodinates.map((tank) => [tank[0], tank[1]]);
  
      // Ajouter le trajet du dépôt à la première cuve
      const depotToFirstTank = [
        storehousePosition,
        [tankPositions[0][0], tankPositions[0][1]]
      ];
  
      const cycleRoutes = tankPositions.reduce((acc, currentPosition, index, array) => {
        if (index < array.length - 1) {
          const nextPosition = array[index + 1];
          return [...acc, [currentPosition, nextPosition]];
        }
        // Ajouter le trajet de la dernière cuve au dépôt
        return [...acc, [currentPosition, storehousePosition]];
      }, [depotToFirstTank]);
  
      return { cycleRoutes, cycleIndex };
    });
    setRoutes(newRoutes);
  }, [cycles, storehousePosition]);

  return (
    <MapContainer center={storehousePosition} zoom={13} style={{ height: "800px", width: "100%", margin: '30px 50px 30px 0px', justifiyContent:"center" ,borderRadius: '19px'}}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={storehousePosition} icon={storehouse_icon}>
        <Popup>
          Dépôt
        </Popup>
      </Marker>
      {cycles.map((cycle, cycleIndex) => (
        <React.Fragment key={cycleIndex}>
          {cycle.selected_tanks_coodinates.map((tank,tankIndex) => (
            <Marker key={tankIndex} position={[tank[0], tank[1]]} icon={tank_icon}>
              <Popup>
                Réservoir {cycle.selected_tanks_ids[tankIndex]} - Cycle {cycleIndex + 1}
                
              </Popup>
            
            </Marker>
          ))}
        </React.Fragment>
      ))}
      {routes.map(({ cycleRoutes, cycleIndex }) => (
        <Polyline key={cycleIndex} positions={cycleRoutes} color={colors[cycleIndex % colors.length]} />
      ))}
    </MapContainer>
  );
}

export default TankMap;
