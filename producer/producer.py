import pika
import time
import json
from datetime import datetime
import random
from uuid import uuid4

# ✅ RabbitMQ 연결 재시도
MAX_RETRIES = 10
for i in range(MAX_RETRIES):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq')  # Swarm 서비스 이름 사용
        )
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"[!] RabbitMQ 연결 실패, 재시도 {i+1}/{MAX_RETRIES}...")
        time.sleep(3)
else:
    raise Exception("RabbitMQ 연결 실패: 모든 재시도 실패")

channel = connection.channel()
channel.queue_declare(queue='hello', durable=True)

while True:
    data = {
        "event": "order_created",
        "timestamp": datetime.now().isoformat(),
        "payload": {
            "order_id": str(uuid4()),
            "user": random.choice(["박세은", "박세련", "황예솔", "이우현"]),
            "amount": round(random.uniform(10, 500), 2)
        }
    }

    message = json.dumps(data, ensure_ascii=False)
    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # 메시지 영속성 보장
    )
    print(f"[x] Sent JSON: {message}")
    time.sleep(5)

