import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from mxnet import nd, image
from mxnet.gluon.data.vision import transforms
from gluoncv import utils
from gluoncv.model_zoo import get_model
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
    model = get_model('cifar_resnet110_v1', classes=10, pretrained=True)

    broker_url = sys.argv[1]
    topic = sys.argv[2]
    server_url = sys.argv[3] 

    stream = MQTTUtils.createStream(ssc, broker_url, topic, username=None, password=None)
    class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                  'dog', 'frog', 'horse', 'ship', 'truck']

    transform_fn = transforms.Compose([
        transforms.Resize(32),
        transforms.CenterCrop(32),
        transforms.ToTensor(),
        transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2023, 0.1994, 0.2010])
    ])

    def loadImgFromUrl(url):
      f_name = utils.download(url, 'to_classify.jpg', True)
      img = image.imread(f_name)
      return transform_fn(img)

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
        pred = model(x.expand_dims(axis=0))
        ind = nd.argmax(pred, axis=1).astype('int')
        classifications = []
        classifications.append({
          "confidence": float(nd.softmax(pred)[0][ind].asscalar()),
          "result": class_names[ind.asscalar()]
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