import logging

logging.basicConfig(filename='GenerateFiles.log', level=logging.DEBUG,
                    format='%(asctime)s // %(levelname)s : %(message)s // line no. %(lineno)d',
                    filemode='a')


def save(filename, content):
    """
    :param filename: Filename with extension
    :param content: Data to be written in the file
    :return: None
    """
    file = ''
    try:
        file = open(filename, "w")
        file.write(content)
    except PermissionError:
        logging.error('Got permission error in save()')
    finally:
        file.close()
