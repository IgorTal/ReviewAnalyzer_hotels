#!/usr/bin/python2.7
#read queue

"""usage: filename.py myhotel_name (run from command line)
purpose: monitor the reviews in the queue and process.
#current design is that we will run this file for each "property name". May refactor as we go along.
"""
import sys
import pika
import json

if len(sys.argv) < 2:
    queue_to_read = raw_input("you must provide a queue name:")
else:
    queue_to_read = sys.argv[1]


"""
queue_to_read(string) is the name of the queue to read.
for example name of the hotel property.

required libraries: Pika, json

"""
#create connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
#not needed but good practice. note we used persistent before so use 'durable=True' here.
channel.queue_declare(queue=queue_to_read,durable=True)


#create the callback function (to process the message)
def callback(ch, method, properties, body):
    review = json.loads(body) # encode back to json

    #do whatever with the message now.
    print(" [x] Received %r" % review)

#consume the queue using the callback function.

channel.basic_consume(callback,queue=queue_to_read,no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
