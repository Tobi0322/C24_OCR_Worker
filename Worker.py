import pika
from Utils import load_rabbit_config
from ImageConverter import ImageConverter, FileFormat
from Model.OcrTask import OcrTaskModel, TaskState

def handle_task(ch, method, properties, body):
    task_id = body.decode("utf-8")
    converter = ImageConverter(body.decode("utf-8") , input_format=FileFormat.PDF)
    text = converter.read_text_from_image()
    converter.save_to_txt(text)
    OcrTaskModel.change_status(task_id, TaskState.DONE.value)



class Worker():
    def __init__(self):
        pass

    def _update_database(self):
        pass

    def consume(self):
        host, queue, user, port, pw = load_rabbit_config()
        credentials = pika.PlainCredentials(user, pw)
        parameters = pika.ConnectionParameters(host,
                                        port,
                                        '/',
                                        credentials)
        print('#'*30)
        print(parameters)
        print(credentials.username)
        print(credentials.password)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        print("Ready to consume")
        channel.basic_consume(queue=queue, on_message_callback=handle_task, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    

