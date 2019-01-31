import json
import datetime
import boto3

def lambda_handler(event, context):
    
    now = datetime.datetime.now()
    violationTime = now.strftime("%Y-%m-%d %H:%M:%S")
    
    body = list(json.dumps(event['body']).split("&"))
    d = dict(s.split('=') for s in body)
    text = d["text"]
    textList = list(text.split('+', 1))
    name = textList[0].replace('%40', '').replace("%E2%80%99", "'")
    
    try:
        reason = textList[1]
    except IndexError:
        reason = None
        
    if reason is None:
        pass
    else:
        reason = reason.replace('+', ' ')
    
    dynamodb = boto3.client('dynamodb')
    
    if reason is None:
        dynamodb.put_item(TableName='hrViolations', Item={'violationTime':{'S':violationTime},'name':{'S':name}})
    else:
        dynamodb.put_item(TableName='hrViolations', Item={'violationTime':{'S':violationTime},'name':{'S':name}, 'reason':{'S':reason}})
        
    
    if reason is None:
        responseText = "{} has received an HR Violation!".format(name)
    else:
        responseText = "{} has received an HR Violation! Reason: {}!".format(name, reason)
        
    
    body = {
        "text": responseText,
        "response_type": "in_channel"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response