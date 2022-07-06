import boto3
import json
import logging
from boto3.dynamodb.conditions import Key, Attr
import requests
from botocore.exceptions import ClientError
from requests_aws4auth import AWS4Auth  
import logging

def lambda_handler(event, context):

    print(event)
    query = event['q']

    client = boto3.client('lex-runtime')
    query = event['q']
    
    # Post user query to Lex & get response
    lex_response = client.post_text(
        botName='quesnans',
        botAlias="QnAalias",
        userId="ccsm9739",
        inputText=query
    )

    if 'slots' in lex_response:
        keys = [lex_response['slots']['TagNames'],lex_response['slots']['TagNamesTwo']]
        print(keys)
    
    print(lex_response)
    
    EndPost = []
    
    print("keys: ", keys)
    
    for key in keys: 
        if key is not None:
            region = 'us-east-1'
            service = 'es'
            credentials = boto3.Session().get_credentials()
            #awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
   
            host = 'https://search-qna-d6orix2thharyekbg22f5lw64y.us-east-1.es.amazonaws.com'
            index = '/posts'
            url = host + index + '/_search'
            query = {
                "size": 3,
                "query": {
                    "multi_match": {
                        "query": key
                    }
                }
            }

            print(url)
            headers = { "Content-Type": "application/json" }
            r = requests.get(url, auth=("ccsm9739","Siri&118"), headers=headers, data=json.dumps(query))
            print(r)
            
            response = r.json()
            
            print("Response", response)
            
            ids = []
            for matches in response['hits']["hits"]:
                ids.append(matches["_id"])
        
            print("ids: ",ids)
    
            dynamodb = boto3.client('dynamodb')
            
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
            
            EndPost.append(posts)
            
            if ids == []:
                posts = "No answers found for this category !"
            
    text = EndPost

    logging.basicConfig(format="[%(levelname)s] [%(name)s] [%(asctime)s]: %(message)s",
    level="INFO")
    logger = logging.getLogger(__name__)

    sns_client = boto3.client('sns' , 'us-east-1')
        
    response = sns_client.publish(
            TopicArn='arn:aws:sns:us-east-1:287413882253:sns_ques_ans',
            Message=json.dumps(text)
        )

    print("Final output", text)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps("Email Sent")
    }
