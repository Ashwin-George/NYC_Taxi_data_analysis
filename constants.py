from datetime import datetime

EC2_PUBLIC_IP='3.111.34.142'
LOCALHOST_PORT='9092'
AWS_REGION='ap-south-1'
BOOTSTRAP_SERVER=EC2_PUBLIC_IP+':'+LOCALHOST_PORT
S3_BUCKET_FOR_REALTIME_DATA_STORAGE= 'nyc.realtime.data.buffer.storage'
S3_STORAGE_FILENAME='logs_{}.json'
S3_FILE_PATH=f's3://{S3_BUCKET_FOR_REALTIME_DATA_STORAGE}/{S3_STORAGE_FILENAME}'
TOPIC_NAME='log_queue_topic'
KAFKA_TOPIC_NAME='log_queue_topic'
BUCKET_DATA_SUBFOLDER='data'
BUCKET_INSIGHTS_SUBFOLDER='insights'

def get_bucket_path(location):

    if location=='data' :
        path= f's3://{S3_BUCKET_FOR_REALTIME_DATA_STORAGE}/{BUCKET_DATA_SUBFOLDER}/{datetime.now().timestamp()}_{S3_STORAGE_FILENAME}'
        return path
    elif location=='insights':
        path= f's3://{S3_BUCKET_FOR_REALTIME_DATA_STORAGE}/{BUCKET_INSIGHTS_SUBFOLDER}'
        return path


    return None