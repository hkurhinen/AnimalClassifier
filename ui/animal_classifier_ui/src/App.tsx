import './App.css';
import { MapContainer } from 'react-leaflet';
import MapContents from './MapContents';

function App() {

  return (
    <div className="App">
      <MapContainer style={{height: "100vh", width: "100%"}}  center={[61.687308, 27.259664]} zoom={7} >
        <MapContents></MapContents>
      </MapContainer>
    </div>
  );
}

export default App;
