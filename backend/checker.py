import json
import urllib3
import boto3
from datetime import datetime

# CONFIGURATION
URL_TO_CHECK = "https://www.google.com" 
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:WebsiteDownAlerts" # PASTE YOUR SNS ARN HERE
TABLE_NAME = "WebsiteHealth"
URL_ID = "my-site"

http = urllib3.PoolManager()
dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')

def lambda_handler(event, context):
    timestamp = datetime.utcnow().isoformat()
    
    try:
        start_time = datetime.now()
        response = http.request('GET', URL_TO_CHECK, timeout=5.0)
        end_time = datetime.now()
        latency = (end_time - start_time).total_seconds()
        status = response.status
        
        if status == 200:
            print(f"Success! Latency: {latency}")
            dynamodb.put_item(
                TableName=TABLE_NAME,
                Item={
                    'UrlID': {'S': URL_ID},
                    'Timestamp': {'S': timestamp},
                    'Latency': {'N': str(latency)},
                    'Status': {'S': str(status)}
                }
            )
        else:
            raise Exception(f"Status code: {status}")

    except Exception as e:
        print(f"Failed: {str(e)}")
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"URGENT: Your website {URL_TO_CHECK} is down! Error: {str(e)}",
            Subject="Website Down Alert"
        )
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                'UrlID': {'S': URL_ID},
                'Timestamp': {'S': timestamp},
                'Latency': {'N': "0"},
                'Status': {'S': "ERROR"}
            }
        )
