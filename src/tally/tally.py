import json
import boto3
import urllib

def lambda_handler(event, context):
    
    body = list(json.dumps(event['body']).split("&"))
    d = dict(s.split('=') for s in body)
    
    maxNumShow = 10
    
    try:
        if int(urllib.parse.unquote(d["text"])) < 1:
            numShow = 3
        else:
            numShow = int(urllib.parse.unquote(d["text"]))
        
    except ValueError:
        numShow = 3
    
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
    
    text = ["Top {} HR Violators:\n".format(min(numShow, maxNumShow))]
    
    for num in range(min(numShow, maxNumShow)):
        user = uniqueNameList[num]
        cnt = nameList.count(user)
        text.append("Name: {} Violations: {}\n".format(user, cnt))
        
    violators = "".join(text)
    
    body = {
        "text": violators,
        "response_type": "in_channel"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

