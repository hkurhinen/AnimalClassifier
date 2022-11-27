import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from keras.applications import ResNet50
from keras.utils import load_img, img_to_array
from keras.applications.resnet import preprocess_input, decode_predictions
import numpy as np
import requests

from mqtt import MQTTUtils

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print >> sys.stderr, "Usage: base_classifier.py <broker url> <topic>"
        exit(-1)

    sc = SparkContext(appName="AnimalClassifier")
    spark = SparkSession(sc)
    ssc = StreamingContext(sc, 1)
    model = ResNet50(weights='imagenet')

    broker_url = sys.argv[1]
    topic = sys.argv[2]

    stream = MQTTUtils.createStream(ssc, broker_url, topic, username=None, password=None)

    def readStream(rdd):
      if not rdd.isEmpty():
        df = spark.read.json(rdd)
        print('Started the Process')
        print('Selection of Columns')
        df = df.select('image').where(col("image").isNotNull())
        path = df.collect()[0][0]
        img = load_img(path, target_size=(224, 224))
        x = img_to_array(img)
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

        obj = { 
          "id": 1,
          "image": path,
          "latitude": 61.667308,
          "longitude": 27.359664,
          "created": "2000-01-23T04:56:07.000+00:00",
          "modified": "2000-01-23T04:56:07.000+00:00",
          "classifications": classifications
        }

        x = requests.post("http://localhost:8080/events", json = obj)
        print(x.text)

    stream.foreachRDD( lambda rdd: readStream(rdd) )
    ssc.start()
    ssc.awaitTermination()