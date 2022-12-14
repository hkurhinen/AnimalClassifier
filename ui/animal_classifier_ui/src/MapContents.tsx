import { useEffect, useState } from 'react';
import './App.css';
import { Marker, Popup, TileLayer, useMap } from 'react-leaflet';
import Noty from 'noty';
import moment from 'moment';
import MarkerClusterGroup from '@changey/react-leaflet-markercluster';

//This function takes in latitude and longitude of two location and returns the distance between them as the crow flies (in km)
function calcDistance(lat1: number, lon1: number, lat2: number, lon2: number) {
  var R = 6371; // km
  var dLat = toRad(lat2-lat1);
  var dLon = toRad(lon2-lon1);
  var lat1 = toRad(lat1);
  var lat2 = toRad(lat2);

  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2); 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = R * c;
  return d;
}

// Converts numeric degrees to radians
function toRad(val: number) {
  return val * Math.PI / 180;
}


function MapContents() {

  const [events, setEvents] = useState([]);
  const [drivingMode, setDrivingMode] = useState(false);
  const [currentPos, setCurrentPos] = useState([0, 0]);
  const [historyTime, setHistoryTime] = useState("15");
  const map = useMap();

  useEffect(() => {
    const interval = setInterval(() => {
      const after = moment().subtract(Number(historyTime), "minutes");
      fetch(`${process.env.REACT_APP_API_URL}/events?createdAfter=${after.toISOString()}&createdBefore=${moment().toISOString()}`)
        .then(res => res.json())
        .then(newEvents => {
          newEvents.forEach((newEvent: any) => {
            const existing = events.find(e => e["_id"]["$oid"] == newEvent["_id"]["$oid"])
            if (!existing) {
              const [lat, lng] = currentPos;
              if (calcDistance(lat, lng, newEvent.latitude, newEvent.longitude) < 10) {
                new Noty({
                  layout: "topCenter",
                  text: "WARNING! Animal detected near you!",
                  theme: "metroui",
                  type: "warning",
                  timeout: 5000
                }).show();
              }
            }
          })
          setEvents(newEvents);
        });
    }, 3000);

    return () => {
      clearInterval(interval);
    };
  }, [events, currentPos, historyTime]);

  useEffect(() => {
    let watch: any = null;
    if (drivingMode) {
      watch = navigator.geolocation.watchPosition(
        (pos) => {
          if (drivingMode) {
            setCurrentPos([pos.coords.latitude, pos.coords.longitude]);
            map.setView([pos.coords.latitude, pos.coords.longitude]);
          }
        }, (err) => {
          console.error(`ERROR(${err.code}): ${err.message}`);
        }
      )
    }

    return () => {
      navigator.geolocation.clearWatch(watch);
    };
  }, [drivingMode]);

  const markers = events.map((event: any) => {
    const key = event["_id"]["$oid"]
    const classifications = event.classifications.map((c: any) =>
      <div key={key+c.result}>
        <b>{c.result}: </b>
        {Math.round(c.confidence * 100)}%
      </div>
    );
    return (
      <Marker key={key} position={[event.latitude, event.longitude]}>
        <Popup>
          {classifications}
          <a target="_blank" href={event.image}>
            <img style={{maxWidth: "150px"}} src={event.image} />
          </a>
        </Popup>
      </Marker>
    );
  })

  return (
    <>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MarkerClusterGroup>
          {markers}
        </MarkerClusterGroup>
        <div className="leaflet-top leaflet-right">
          <div className="leaflet-control leaflet-bar">
            <a href="#" onClick={() => setDrivingMode(!drivingMode)} style={{width: "110px"}}>{ drivingMode ? "Stop driving mode" : "Start driving mode" }</a>
          </div>
        </div>
        <div className="leaflet-bottom leaflet-left">
          <div style={{padding: 5, backgroundColor: "rgb(244, 244, 244)"}} className="leaflet-control leaflet-bar">
            <label>Show history: </label>
            <select 
              onChange={(event) => setHistoryTime(event.currentTarget.value)}
              value={historyTime} 
              id="history-retention">
                <option value="1">1 minutes</option>
                <option value="5">5 minutes</option>
                <option value="15">15 minutes</option>
                <option value="60">1 hour</option>
                <option value="120">2 hour</option>
                <option value="360">6 hour</option>
                <option value="1440">24 hour</option>
            </select>
          </div>
        </div>
    </>
  );
}

export default MapContents;
