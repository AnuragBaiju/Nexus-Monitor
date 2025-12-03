import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WebsiteHealth')

def lambda_handler(event, context):
    try:
        response = table.query(
            KeyConditionExpression=Key('UrlID').eq('my-site'),
            ScanIndexForward=False,
            Limit=1500 
        )
        items = response.get('Items', [])
    except Exception as e:
        print(f"Error reading DB: {str(e)}")
        items = []

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(items, default=str)
    }
