import pika
from OCR_Shared.Utils import load_rabbit_config
from ImageConverter import ImageConverter, FileFormat
from OCR_Shared.OcrTask import OcrTaskModel, TaskState
import logging
import threading
import functools
import time

MAX_NUM_OF_THREADS = 3



LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

def ack_message(channel, delivery_tag):
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        pass

def handle_task(connection, channel, delivery_tag, body):
    task_id = body.decode("utf-8")

    thread_id = threading.get_ident()
    fmt1 = 'Thread id: {} Delivery tag: {} Message body: {}'
    LOGGER.info(fmt1.format(thread_id, delivery_tag, body))
    
    OcrTaskModel.change_status(task_id, TaskState.PENDING.value)
    
    try:
        converter = ImageConverter(task_id +".pdf", input_format=FileFormat.PDF)
        text = converter.read_text_from_image()
        converter.save_to_txt(text)
        OcrTaskModel.change_status(task_id, TaskState.DONE.value)
    except Exception as e:
        fmt2 = "ERROR: Convertion of the task {} failed."
        print("#"*30)
        print(e)
        LOGGER.info(fmt2.format(task_id))
        OcrTaskModel.change_status(task_id, TaskState.FAILED.value)
    
    ack_message(channel, delivery_tag)
    
def on_message(channel, method_frame, header_frame, body, args):
    (connection) = args
    delivery_tag = method_frame.delivery_tag
    handle_task(connection, channel, delivery_tag, body)

class Worker():
    def __init__(self):
        pass

    def _update_database(self):
        pass

    def consume(self):
        host, queue, user, port, pw = load_rabbit_config()
        credentials = pika.PlainCredentials(user, pw)
        parameters = pika.ConnectionParameters(heartbeat=1200,
                                        host=host,
                                        port=port,
                                        virtual_host='/',
                                        credentials=credentials)

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        
        on_message_callback = functools.partial(on_message, args=(connection))
        channel.basic_consume(queue=queue, on_message_callback=on_message_callback)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()

        connection.close()
        

    

