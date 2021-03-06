#!/usr/bin/env python
import pika
import json
import os
import time
import sys
import traceback

# from utils import parse_log, is_get_request
# not working, include 2 functions inline
import datetime

def parse_log(msg):
    # Retrieves relevant information from GET request
    decomposed_message = msg.split(" ")
    if len(decomposed_message) > 7:
        source = decomposed_message[0]
        status = decomposed_message[-2]
        time = decomposed_message[3][1:]
        day = datetime.datetime.strptime(time, "%d/%b/%Y:%X").date()
        return day, status, source
    else:
        return None

def is_get_request(msg):
    # Determines is msg is a GET request
    decomposed_message = msg.split(" ")
    return len(decomposed_message) >= 6 and decomposed_message[5] == "\"GET"


#Connect  to RabbitMQ
credentials = pika.PlainCredentials(os.environ['RABBITMQ_DEFAULT_USER'], os.environ['RABBITMQ_DEFAULT_PASS'])
parameters = pika.ConnectionParameters(host='rabbit',
                                       port=5672,
                                       credentials=credentials)

while True:
    try:
        connection = pika.BlockingConnection(parameters)
        break
    except pika.exceptions.ConnectionClosed:
        print('[ *** Ingestion/WARN] RabbitMQ not up yet.')
        time.sleep(2)

print('[ *** Ingestion/INFO] Connection to RabbitMQ established')


# Start queue

channel = connection.channel()
channel.queue_declare(queue='log-analysis')

# Read weblogs

# using smaller file for testing
#filename_log = 'weblogs-test.log'

filename_log = 'weblogs.log'
f = open(filename_log, 'r')

while True:
    try:
        msg = f.readline()

        if not msg:
            break
        #If message is GET request, ingest it into the queue
        if is_get_request(msg):
            # Parse GET request for relevant information
            tmp = parse_log(msg)
            if len(tmp) == 3:
                day, status, source = tmp

            # Store in RabbitMQ
            body = json.dumps({'day': str(day), 'status': status, 'source': source})
            channel.basic_publish(exchange='',
                                  routing_key='log-analysis',
                                  body=body)

    except:
        print("[ *** Ingestion/ERROR] msg = \n" +  msg)
        print("[ *** Ingestion/ERROR] " +  traceback.format_exc())
        #print("[ *** Ingestion/ERROR] " +  sys.exc_info()[0])

connection.close()
