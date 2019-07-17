import pika
from Utils import load_rabbit_config
from ImageConverter import ImageConverter, FileFormat
from Model.OcrTask import OcrTaskModel, TaskState
import logging
import threading
import functools

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

def akk_message(channel, delivery_tag):
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        pass

def handle_task(connection, channel, delivery_tag, body):
    task_id = body.decode("utf-8")
    OcrTaskModel.change_status(task_id, TaskState.PENDING.value)
    
    print("Getting a new task!")
    thread_id = threading.get_ident()
    fmt1 = 'Thread id: {} Delivery tag: {} Message body: {}'
    LOGGER.info(fmt1.format(thread_id, delivery_tag, body))
    
    converter = ImageConverter(task_id , input_format=FileFormat.PDF)
    print("Initializing Converter")
    text = converter.read_text_from_image()
    print("Text converted")
    converter.save_to_txt(text)
    print("Text saved")
    OcrTaskModel.change_status(task_id, TaskState.DONE.value)
    print("Status changed")
    
def on_message(channel, method_frame, header_frame, body, args):
    (connection, threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=handle_task, args=(connection, channel, delivery_tag, body))
    t.start()
    threads.append(t)
    

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
        
        threads = []
        on_message_callback = functools.partial(on_message, args=(connection, threads))
        channel.basic_consume(queue=queue, on_message_callback=on_message_callback)
        
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()

        # Wait for all to complete
        for thread in threads:
            thread.join()

        connection.close()
        

    

