import logging
import pika
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def callback(ch, method, properties, body):
    logging.info(f" [x] Received {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

for attempt in range(5):
    try:
        logging.info("Connecting to RabbitMQ...")
        # 서비스명 주의 (project_rabbitmq로 수정!)
        connection = pika.BlockingConnection(pika.ConnectionParameters('project_rabbitmq'))
        channel = connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='task_queue', on_message_callback=callback)

        logging.info(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Connection failed (Attempt {attempt+1}/5), retrying in 5 seconds... Error: {e}")
        time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Consumer stopped by user.")
        break
else:
    logging.critical("Unable to connect to RabbitMQ after 5 attempts.")

