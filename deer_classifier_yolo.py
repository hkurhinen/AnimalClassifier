import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from gluoncv import utils
from datetime import datetime, timezone
import torch
import cv2

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
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='custom_weights.pt', force_reload=True)

    broker_url = sys.argv[1]
    topic = sys.argv[2]
    server_url = sys.argv[3] 

    stream = MQTTUtils.createStream(ssc, broker_url, topic, username=None, password=None)

    def loadImgFromUrl(url):
      f_name = utils.download(url, 'to_classify_deer_classifier_yolo.jpg', True)
      img = cv2.imread(f_name)
      return img

    def readStream(rdd):
      if not rdd.isEmpty():
        df = spark.read.json(rdd)
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
        pred = model(x)
        n = pred.pandas().xyxy[0]
        if n.empty:
          return
        conf = n['confidence'].values[0]
        res = n['name'].values[0] + '_2'
        classifications = []
        classifications.append({
          "confidence": float(conf),
          "result": res
        })

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