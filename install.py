import os
import subprocess

from utils.logger import get_logger

# Variables
logger = get_logger(__name__)

FILE = 'requirements.txt'
FOLDER = './plugins'
COMMAND = ['python', '-m', 'pip', 'install', '-r']


def install(file: str):
    process = subprocess.Popen(COMMAND + [file],
                               shell=True)
    process.wait()


if __name__ == '__main__':
    logger.info('Install global requirements')
    install(FILE)

    for element in os.listdir(FOLDER):
        path = os.path.join(FOLDER, element)
        if not os.path.isdir(path):
            continue

        filepath = os.path.join(path, FILE)
        if os.path.isfile(filepath):
            logger.info('Install %s\'s requirements', element)
            install(filepath)

    logger.info('Completed')
