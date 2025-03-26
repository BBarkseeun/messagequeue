import logging
import pika
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# 무한 반복 메시지 전송
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('project_rabbitmq'))
        channel = connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body='Hello RabbitMQ!',
            properties=pika.BasicProperties(delivery_mode=2)
        )

        logging.info("[x] Sent 'Hello RabbitMQ!'")
        connection.close()

        time.sleep(5)  # 5초마다 메시지 반복 전송
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Connection failed: {e}, retrying in 5 seconds...")
        time.sleep(5)

