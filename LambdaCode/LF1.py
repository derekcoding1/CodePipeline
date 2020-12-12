import os
import math
import dateutil.parser
import datetime
import json
import boto3
import requests
import time
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.aws_auth import AWSRequestsAuth

def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    name = event['Records'][0]['s3']['object']['key']
    print(name)
    print(bucket)
    client = boto3.client('lex-runtime')
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    client = boto3.client('lex-runtime')
    service = 'es'
    region = 'us-east-1'
    host = "search-photos-h6zoqq64jz26jdum4eoo2lqjya.us-east-1.es.amazonaws.com"
    credentials = boto3.Session().get_credentials()
    awsauth = AWSRequestsAuth(aws_access_key=credentials.access_key,
                             aws_secret_access_key=credentials.secret_key,
                             aws_region=region,
                             aws_service=service,
                             aws_token=credentials.token,
                             aws_host=host)
    
    print(name)
    print(bucket)
    rek = boto3.client('rekognition')
    response = rek.detect_labels(
        #name,bucket
        Image={
            'S3Object' :{
                'Bucket' :bucket,
                'Name' :name
            }
        },
        MaxLabels=4
    )
    print(response)
    timestamp =time.time()
    labels = []
    for i in range(len(response['Labels'])):
        labels.append(response['Labels'][i]['Name'])
    print(labels)
    message = {'objectKey':name,'bucket':bucket,'createdTimestamp':timestamp,'labels':labels}
    #url = "https://search-photos-h6zoqq64jz26jdum4eoo2lqjya.us-east-1.es.amazonaws.com/photos"
    headers = {"Content-Type": "application/json"}
    #r = requests.put(url, auth=awsauth,json = message)
    #r = requests.post(url, data=json.dumps(message).encode("utf-8"), headers=headers)
    
    
    #awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    host = 'search-photos-h6zoqq64jz26jdum4eoo2lqjya.us-east-1.es.amazonaws.com'
    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    # document = { 
    #         'name': 'Luis'
    #     }
    print('start')
    res = es.index(index='photos', doc_type = '_doc', body = message)
    print('done')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }