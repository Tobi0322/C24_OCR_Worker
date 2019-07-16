import yaml

def get_config_file_name():
    return 'config.yaml'

def load_ocr_config():
    """ Load the configuration of the ocr module.

    :param file:
    :return:
    """
    filename = get_config_file_name()
    with open(filename, 'r') as stream:
        config = yaml.safe_load(stream)
        ocr_config = config['ocr']
        return ocr_config['source_path'], ocr_config['destination_path']


def load_rabbit_config():
    filename = get_config_file_name()
    with open(filename, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            rabbit_config = config['rabbitmq']
            user = rabbit_config['rb_user']
            host = rabbit_config['rb_host']
            queue = rabbit_config['rb_queue']
            port = rabbit_config['rb_port']
            pw = rabbit_config['rb_pw']
        except yaml.YAMLError as exc:
            print(exc)

    return host, queue, user, port, pw





