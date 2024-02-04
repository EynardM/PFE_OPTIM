import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Icons
var Icon = L.Icon.extend({
options: {
    iconSize:     [64, 64],
    popupAnchor:  [0, -20]
}
});

var Icon = L.Icon.extend({
options: {
    iconSize:     [30, 30],
    popupAnchor:  [0, -20]
}
});

var storehouse_icon = new Icon({
iconUrl: "https://img.icons8.com/external-flatart-icons-flat-flatarticons/64/external-storehouse-agriculture-flatart-icons-flat-flatarticons.png",
});

var tank_icon = new Icon({
iconUrl:"https://img.icons8.com/arcade/64/marker.png"
})

  
function TankMap({ storehouse, cycles }) {
    const storehousePosition = [storehouse.latitude, storehouse.longitude];
  
    return (
      <MapContainer center={storehousePosition} zoom={13} style={{ height: "400px", width: "100%" }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={storehousePosition} icon={storehouse_icon}>
          <Popup>
            Dépôt
          </Popup>
        </Marker>
        {cycles.map((cycle, index) => (
          <React.Fragment key={index}>
            {cycle.selected_tanks.map((tank, tankIndex) => (
              <Marker key={tankIndex} position={[tank.maker.latitude, tank.maker.longitude]} icon={tank_icon}>
                <Popup>
                  Réservoir {tank.id} - Cycle {index + 1}
                </Popup>
              </Marker>
            ))}
          </React.Fragment>
        ))}
      </MapContainer>
    );
  }

export default TankMap