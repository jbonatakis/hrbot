import json
import datetime
import boto3
import urllib

def lambda_handler(event, context):
    
    now = datetime.datetime.now()
    violationTime = now.strftime("%Y-%m-%d %H:%M:%S")
    
    body = list(json.dumps(event['body']).split("&"))
    d = dict(s.split('=') for s in body)
    text = urllib.parse.unquote(d["text"])
    givenBy = urllib.parse.unquote(d["user_name"])
    textList = list(text.split('+', 1))
    name = textList[0]
    
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
        dynamodb.put_item(TableName='hrViolations',
                Item={ 
                    'violationTime':{'S':violationTime},
                    'name':{'S':name.capitalize()},
                    'givenBy':{'S':givenBy.capitalize()}
                })
    else:
        dynamodb.put_item(TableName='hrViolations',
                Item={
                    'violationTime':{'S':violationTime},
                    'name':{'S':name.capitalize()},
                    'reason':{'S':reason},
                    'givenBy':{'S':givenBy.capitalize()}
                })
        
    
    if reason is None:
        responseText = "{} has received an HR Violation!".format(name.capitalize())
    else:
        responseText = "{} has received an HR Violation! \nReason: {}".format(name.capitalize(), reason.capitalize())
        
    
    body = {
        "text": responseText,
        "response_type": "in_channel"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
