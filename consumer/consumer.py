import pika
import time

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    # 메시지 처리 (2초간 처리 시뮬레이션)
    time.sleep(2)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 메시지 처리 완료 후 ack 전송

def main():
    # RabbitMQ 연결
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # 큐 선언
    channel.queue_declare(queue='task_queue', durable=True)

    # 한 번에 하나의 메시지만 처리하도록 설정
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()

