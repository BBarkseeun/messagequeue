import pika
import time

def main():
    # RabbitMQ 연결
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # 큐 선언
    channel.queue_declare(queue='task_queue', durable=True)

    # 메시지 발행
    for i in range(10):
        message = f"Message {i+1}"
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # 메시지 영속성 설정
            )
        )
        print(f" [x] Sent {message}")
        time.sleep(1)  # 메시지 간에 1초 딜레이

    connection.close()

if __name__ == "__main__":
    main()

