import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from keras.applications import ResNet50
from keras.utils import load_img, img_to_array
from keras.applications.resnet import preprocess_input, decode_predictions
from urllib.request import urlopen
from io import BytesIO
from datetime import datetime, timezone

import numpy as np
import requests

from mqtt import MQTTUtils

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print >> sys.stderr, "Usage: base_classifier.py <broker url> <topic> <server url>"
        exit(-1)

    sc = SparkContext(appName="AnimalClassifier")
    spark = SparkSession(sc)
    ssc = StreamingContext(sc, 1)
    model = ResNet50(weights='imagenet')

    broker_url = sys.argv[1]
    topic = sys.argv[2]
    server_url = sys.argv[3] 

    stream = MQTTUtils.createStream(ssc, broker_url, topic, username=None, password=None)

    def loadImgFromUrl(url):
      with urlopen(url) as image:
        img = load_img(BytesIO(image.read()), target_size=(224, 224))

      return img_to_array(img)


    def readStream(rdd):
      if not rdd.isEmpty():
        df = spark.read.json(rdd)
        print('Started the Process')
        print('Selection of Columns')
        df = df.select(
          'image',
          'latitude',
          'longitude').where(
            col("image").isNotNull()
          )
        data = df.collect()
        url = data[0][0]
        latitude = data[0][1]
        longitude = data[0][2]
        x = loadImgFromUrl(url)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        cs = decode_predictions(preds, top=3)[0]
        classifications = []
        for c in cs:
          (r, desc, prob) = c
          classifications.append({
            "confidence": float(prob),
            "result": desc
          })

        #print("Classification")
        #print(classification)
        #print("Description")
        #print(description)
        #print("Probability")
        #print(probablity)
        utc_dt = datetime.now(timezone.utc)
        iso_date = utc_dt.astimezone().isoformat()

        obj = { 
          "image": url,
          "latitude": latitude,
          "longitude": longitude,
          "created": iso_date,
          "modified": iso_date,
          "classifications": classifications
        }

        x = requests.post(server_url + "/events", json = obj)
        print(x.text)

    stream.foreachRDD( lambda rdd: readStream(rdd) )
    ssc.start()
    ssc.awaitTermination()