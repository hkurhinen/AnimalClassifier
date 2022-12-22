import fetch from "node-fetch";
import mqtt from "mqtt";
import fs from "fs";

async function sleep(ms) {
  return new Promise((resolve, reject) => {
    setTimeout(() => resolve(), ms)
  })
};

async function loadData(mqttClient) {
  const res = await fetch("https://tie.digitraffic.fi/api/weathercam/v1/stations")
  const data = await res.json();
  const features = data.features;
  for(let i = 0; i < features.length; i++) {
    const feature = features[i];
    const coordinates = {
      latitude: feature.geometry.coordinates[1],
      longitude: feature.geometry.coordinates[0]
    }
    const presets = (feature.properties.presets || []).filter(p => p.inCollection);
    for (let n = 0; n < presets.length; n++) {
      const msg = {...coordinates, image: `https://weathercam.digitraffic.fi/${presets[n].id}.jpg`}
      console.log(msg);
      mqttClient.publish("base", JSON.stringify(msg));
      await sleep(30 * 1000);
    }
  } 
}

async function main() {
  const config = JSON.parse(fs.readFileSync("config.json").toString("utf-8"));
  const options = {
    host: config.mqttHost,
    port: 8883,
    protocol: 'mqtts',
    username: config.mqttUser,
    password: config.mqttPass
  }

  const client = mqtt.connect(options);
  client.on('connect', async () => {
    while(true) {
      await loadData(client);
      sleep(1000 * 60 * 60);
    }
  });
}

main();