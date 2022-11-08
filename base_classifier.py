import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from keras.applications import ResNet50
from keras.utils import load_img, img_to_array
from keras.applications.resnet import preprocess_input, decode_predictions
import numpy as np

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
        # decode the results into a list of tuples (class, description, probability)
        # (one such list for each sample in the batch)
        print('Predicted:', decode_predictions(preds, top=3)[0])
        

    stream.foreachRDD( lambda rdd: readStream(rdd) )
    ssc.start()
    ssc.awaitTermination()