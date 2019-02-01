import json
import boto3

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('hrViolations')
    
    fullTable = table.scan()
    
    itemCount = int(fullTable['Count'])
    
    data = fullTable['Items']
    
    nameList = []
    uniqueNameList = []
    uniqueNameCount = []
    
    for i in range(itemCount):
        name = data[i]['name']
        nameList.append(name)
    
    for name in nameList:
        if name not in uniqueNameList:
            uniqueNameList.append(name)
    
    for name in uniqueNameList:
        ct = nameList.count(name)
        uniqueNameCount.append(ct)
        
    
    uniqueNameCount, uniqueNameList = (list(t) for t in zip(*sorted(zip(uniqueNameCount, uniqueNameList), reverse=True)))
    
    name1 = uniqueNameList[0]
    name2 = uniqueNameList[1]
    name3 = uniqueNameList[2]
    
    name1Count = nameList.count(name1)
    name2Count = nameList.count(name2)
    name3Count = nameList.count(name3)
    
    
    text = "Top HR Violators:\nName: {} Violations: {}\nName: {} Violations: {}\nName: {} Violations: {}".format(name1, name1Count, name2, name2Count, name3, name3Count)
            
    
    
    
    
    body = {
        "text": text,
        "response_type": "in_channel"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
