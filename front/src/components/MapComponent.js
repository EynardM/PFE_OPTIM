// Imports
import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import '../App.css';

// Icons
var Icon = L.Icon.extend({
  options: {
    iconSize:     [64, 64],
    popupAnchor:  [0, -20]
  }
});

var storeHouse = new Icon({
  iconUrl: "https://img.icons8.com/external-flatart-icons-flat-flatarticons/64/external-storehouse-agriculture-flatart-icons-flat-flatarticons.png",
});

var tank = new Icon({
  iconUrl: "https://img.icons8.com/ios-filled/50/oil-storage-tank.png"
})

// Component
const MapComponent = ({ data }) => {
  // State variables
  const [markerPositions, setMarkerPositions] = useState({});
  const [pathLines, setPathLines] = useState({});
  const center = [43.6047, 1.4442 ];
  const sth = [43.6088647, 1.4494968];

  return (
    <div className="background">
      <h2 style={{ textAlign: "center", fontFamily: "Soin Sans Pro, sans-serif", fontSize: "30px", fontWeight: "bold", color: "#084B8A"}}>Visualisation</h2>
      
      <MapContainer center={center} zoom={13} className="map-container">
        <TileLayer 
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" 
          className="glacial-tile-layer" 
        />
        
          <Marker position={sth} icon={storeHouse}>
            <Popup>
              Hello
            </Popup>
          </Marker>
        
        
      </MapContainer>
    </div>
  );
};

// Export
export default MapComponent;
