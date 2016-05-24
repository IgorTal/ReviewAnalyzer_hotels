####
#****Functions to create job queue 
#******uses pika and rabbitmq


#
#create a queue
def createQueue(queue_name, message_data):
    """function to create a message queue. queue_name is name of the queue(string).
        message_data = actual review in json/dict.

        queue_name is important. queue listener function will look for queue_name. lets make
        queue_name = name of the hotel property.

         packages required : pika, json

    """
    #do connection stuff to pika
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True) # durable=True - makes queue persistent

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message_data), # message must be string. use json.dumps
        properties=pika.BasicProperties(
            delivery_mode=2, # makes persistent job
            priority=0, # default priority
            #timestamp=timestamp, # timestamp of job creation
            #expiration=str(expire), # job expiration (milliseconds from now), must be string, handled by rabbitmq
            #headers=headers
        ))

    return True

#consume a queue
