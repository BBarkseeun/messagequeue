import pika
import time
import json
from datetime import datetime
import random

# ✅ RabbitMQ 연결 재시도
MAX_RETRIES = 10
for i in range(MAX_RETRIES):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"[!] RabbitMQ 연결 실패, 재시도 {i+1}/{MAX_RETRIES}...")
        time.sleep(3)
else:
    raise Exception("RabbitMQ 연결 실패: 모든 재시도 실패")

channel = connection.channel()
channel.queue_declare(queue='hello')

count = 1
while True:
    data = {
        "event": "order_created",
        "timestamp": datetime.now().isoformat(),
        "payload": {
            "order_id": count,
            "user": random.choice(["박세은", "박세련", "황예솔", "이우현"]),
            "amount": round(random.uniform(10, 500), 2)
        }
    }

    message = json.dumps(data)
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=message)
    print(f"[x] Sent JSON: {json.dumps(data, ensure_ascii=False)}")  # ������ 요기!
    count += 1
    time.sleep(5)

