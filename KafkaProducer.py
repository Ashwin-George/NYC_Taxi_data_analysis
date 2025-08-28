from kafka import KafkaConsumer, KafkaProducer
from time import sleep
import  datetime
from json import dumps
import pandas as pd
import json


import constants
# S3_FILE_PATH=f's3://{S3_BUCKET}/{S3_STORAGE_FILENAME}'
producer = KafkaProducer(bootstrap_servers=[constants.BOOTSTRAP_SERVER],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


df=pd.read_csv('dataset/yellow_tripdata_2016-01.csv')
df.head()

import time

start_time = time.time()
while time.time() - start_time < 20:
    dict_stock = df.sample(1).to_dict(orient='records')[0]
    producer.send(constants.KAFKA_TOPIC_NAME, value=dict_stock)
    time.sleep(1)
