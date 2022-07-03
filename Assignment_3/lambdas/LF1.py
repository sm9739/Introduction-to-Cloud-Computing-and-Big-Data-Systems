import boto3
import json
import logging
from boto3.dynamodb.conditions import Key, Attr
import requests
from botocore.exceptions import ClientError
from requests_aws4auth import AWS4Auth  
import random


def lambda_handler(event, context):

    #dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
   
    host = 'http://sm9739hw1.s3-website-us-east-1.amazonaws.com'
    index = 'id'
    url = host + index + '/_search'
    query = {
        "size": 3,
        "query": {
            "multi_match": {
                "query": event['queryStringParameters']['q']
            }
        }
    }

    headers = { "Content-Type": "application/json" }
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    response = r.json()
    if response['hits'] == []:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': "No answers found for this category"
        }

    response['body'] = r.text
    response['body'] = json.loads(response['body'])
   
    matches = response['body']['hits']['hits']
    print(matches)
    ids= random.choices(matches,k=3)
    ids= [documents["_id"] for documents in matches]

    print(ids)
    
    dynamo = boto3.client('dynamodb')
    
    posts = { 'item': []}
    for id in ids:
        response = dynamo.get_item(
            TableName="posts",
            Key={
                "id" :{
                    "N":id
                }
            }
        )
        
        item.append(response['Item']['posts'])
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(posts)
       
        }
        




 ids = []
    for matches in response['hits']["hits"]:
        id_list.append(matches["_id"])
   
    print("ids: ",ids)
    
    #dynamo = boto3.client('dynamodb')
    
    posts = { 'item': []}
    for id in ids:
        response = dynamodb.get_item(
            TableName="posts",
            Key={
                "id" :{
                    "N":id
                }
            }
        )
        
        posts['item'].append(response['Item']['posts'])
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(posts)
       
        }