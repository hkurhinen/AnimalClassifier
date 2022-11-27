import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';



function App() {

  var [events, setEvents] = useState([]);

  useEffect(() => {
    const interval =   setInterval(() => {
      fetch("http://localhost:8080/events")
        .then(res => res.json())
        .then(events => setEvents(events));
    }, 3000);
  
    return () => {
      clearInterval(interval);
    };
  }, []);

  /*
  {
    "_id": {
      "$oid": "637e03328e0af3a7ab6112ac"
    },
    "classifications": [
      {
        "confidence": 1.0,
        "result": "Cat"
      }
    ],
    "created": {
      "$date": "2000-01-23T04:56:07Z"
    },
    "id": 1,
    "image": "image.jpg",
    "latitude": 61.687308,
    "longitude": 27.259664,
    "modified": {
      "$date": "2000-01-23T04:56:07Z"
    }
  },
*/
  var markers = events.map((event: any) => {
    var text = event.classifications.map((c: any) => `${c.result} (${c.confidence})`);
    return (
      <Marker key={event["_id"]["$oid"]} position={[event.latitude, event.longitude]}>
        <Popup>
          {text.join(", ")}
        </Popup>
      </Marker>
    );
  })

  return (
    <div className="App">
      <MapContainer style={{height: "100vh", width: "100%"}}  center={[61.687308, 27.259664]} zoom={7} >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {markers}
      </MapContainer>
    </div>
  );
}

export default App;
