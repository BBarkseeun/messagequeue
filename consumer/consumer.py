import pika
import json
import time

# ✅ RabbitMQ 연결 재시도 로직
MAX_RETRIES = 10
for i in range(MAX_RETRIES):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        break  # 연결 성공 시 반복 종료
    except pika.exceptions.AMQPConnectionError:
        print(f"[!] RabbitMQ 연결 실패, 재시도 {i+1}/{MAX_RETRIES}...")
        time.sleep(3)
else:
    raise Exception("RabbitMQ 연결 실패: 모든 재시도 실패")

channel = connection.channel()
channel.queue_declare(queue='hello', durable=True)

def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode())
        print(f"[x] Received JSON:")
        print(f"Event: {message['event']}")
        print(f"Timestamp: {message['timestamp']}")
        print(f"Order ID: {message['payload']['order_id']}")
        print(f"User: {message['payload']['user']}")
        print(f"Amount: {message['payload']['amount']} USD")
    except json.JSONDecodeError:
        print(f"[!] Invalid JSON: {body.decode()}")

channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

print('[*] Waiting for JSON messages. To exit press CTRL+C')
channel.start_consuming()

