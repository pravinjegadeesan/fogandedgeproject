import json
import os
import uuid
from decimal import Decimal

import boto3

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'SmartHomeEnergyData')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['body'])
        
        item = {
            'id': str(uuid.uuid4()),
            'timestamp': payload['timestamp'],
            'temperature': Decimal(str(payload['temperature'])),
            'humidity': Decimal(str(payload['humidity'])),
            'voltage': Decimal(str(payload['voltage'])),
            'current': Decimal(str(payload['current'])),
            'power': Decimal(str(payload['power'])),
            'status': payload['status']
        }
        
        table.put_item(Item=item)
        
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data ingested successfully'})
    }
