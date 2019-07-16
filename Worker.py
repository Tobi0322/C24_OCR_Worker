import pika
from Utils import load_rabbit_config
from ImageConverter import ImageConverter, FileFormat
from Model.OcrTask import OcrTaskModel, TaskState
import logging

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


def handle_task(ch, method, properties, body):
    print("Getting a new task!")
    task_id = body.decode("utf-8")
    converter = ImageConverter(task_id , input_format=FileFormat.PDF)
    print("Initializing Converter")
    text = converter.read_text_from_image()
    print("Text converted")
    converter.save_to_txt(text)
    print("Text saved")
    OcrTaskModel.change_status(task_id, TaskState.DONE.value)
    print("Status changed")

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

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_consume(queue=queue, on_message_callback=handle_task, auto_ack=True)
        channel.start_consuming()
        
        

    

