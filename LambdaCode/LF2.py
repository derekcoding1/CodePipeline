import json
import os
import math
import dateutil.parser
import datetime
import time
import logging
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.aws_auth import AWSRequestsAuth

def lambda_handler(event, context):
    #TODO implement
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
    
    host = 'search-photos-h6zoqq64jz26jdum4eoo2lqjya.us-east-1.es.amazonaws.com'
    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    #document = { 
     #       'name': 'Derek'
      #  }
    #print('start')
    #res = es.index(index='name', doc_type = '_doc', id = 1, body = document)
    #print('done')
    print(event["queryStringParameters"]['q'])
    res = client.post_text(
        botName = 'query_handler',
        botAlias = 'hw',
        userId = 'Sambit',
        inputText = event["queryStringParameters"]['q']
        )
    #res = es.search(index = "photos", body = {"from" : 0, "size" : 100, "query": { "match_all": {}}})
    print(res)
    #print(res)
    if 'slots' in res:
        labels = [res['slots']['LabelOne'],res['slots']['LabelTwo']]
        print(labels)
    #     url = 'https://search-photos-h6zoqq64jz26jdum4eoo2lqjya.us-east-1.es.amazonaws.com/photos'
        #resp = []
        resp = es.search(index = "photos", body = {"from" : 0, "size" : 100, "query": { "match_all": {}}})
        print(resp)
    #     response = es.search(index="photos", body={
    #                             "query": {
    #                                 "match_all" : {}
    #                             }
    #                         }, size=100)
    #     print(response)                   
    #     for label in labels:
    #         if (label is not None) and label != '':
    #             print(label)
    #             #url2 = url+label
    #             #url2 = url
    #             #resp.append(requests.get(url2,auth=awsauth).json())
    #     #print(resp)
        pictures = []
        if 'hits' in resp:
             for val in resp['hits']['hits']:
                for label in val['_source']['labels']:
                    if label.lower() in labels:
                        key = val['_source']['objectKey']
                        if key not in pictures:
                            pictures.append(key)
        print(pictures)
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": json.dumps(pictures),
            "isBase64Encoded": False
        }
    else:
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": [],
            "isBase64Encoded": False}
    return response