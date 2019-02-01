import json
import boto3
import pandas as pd


def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('hrViolations')
    fullTable = table.scan()
    itemCount = fullTable['Count']
    data = json.dumps(fullTable, indent=4)

    nameList = []
    reasonList = []

    indexList = []

    for count, i in enumerate(range(num)):
        name = data[count]['name']
        nameList.append(name)

        reason = data[count]['reason']
        reasonList.append(reason)

    violations = pd.DataFrame({'Name':nameList, 'Violations':reasonList}).groupby('Name').agg('count')
    violations.reset_index(inplace=True)

    uniqueName = []
    violationCount = []

    for index, row in violations.iterrows():
        uniqueName.append(row['Name']) 
        violationCount.append(row['Violations'])
    
    body = {
        "text": uniqueName,
        "response_type": "in_channel"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response