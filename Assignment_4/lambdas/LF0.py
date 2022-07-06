import json
import boto3
import pandas as pd
import random
from datetime import datetime

def lambda_handler(event, context):
    # TODO implement
    id_num = random.randint(10000, 100000)
    now = datetime.now()
    str = event['q']
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('posts')
    
    response = table.put_item(
    Item={
        'id': id_num,
        'date': now.strftime("%d/%m/%Y %H:%M:%S"),
        'posts': str
    })
    
    print(id_num)
    print(now.strftime("%d/%m/%Y %H:%M:%S"))
    
    return {
        'statusCode': 200,
         'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': str
    }
