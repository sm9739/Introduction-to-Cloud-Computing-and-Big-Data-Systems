import boto3
import pandas as pd
df = pd.read_csv('DynamoDB.CSV')
df['id'] = df['id'].astype(int)
df.dropna(inplace=True)
df = df.rename({' date': 'date', ' posts': 'posts'}, axis=1)
df['json'] = df.apply(lambda x: x.to_dict(), axis=1)
payloads = df['json'].to_list()

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
dynamodb_res = boto3.resource('dynamodb', region_name='us-east-1')
try:
    table = dynamodb.create_table (
        TableName = 'posts',
           KeySchema = [
               {
                   'AttributeName': 'id',
                   'KeyType': 'HASH'
               },
               ],
               AttributeDefinitions = [
                   {
                       'AttributeName': 'id',
                       'AttributeType': 'N'
                   },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits':1,
                    'WriteCapacityUnits':1
                }

        )
finally:
    table = dynamodb_res.Table('posts')
    count = 0
    for payload in payloads:
        count += 1
        print(payload)
        table.put_item(Item=payload)
        print("count is:", count)
print(table)