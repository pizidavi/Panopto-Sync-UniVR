import os

from lib.AESCipher import AESCipher
from utils.arguments import parser
from utils.inputs import input_password


# Variables
ARGS = parser.parse_known_args()[0]

CONFIG_DIR = './configs'
CREDENTIALS = 'credential.encrypt'


def get_credential() -> tuple[str, str]:
    path = os.path.join(CONFIG_DIR, CREDENTIALS)
    # try:
    #     fp = open(path, 'r')
    # except FileNotFoundError:
    #     raise FileNotFoundError('Login is required')
    if os.path.isfile(path):
        fp = open(path, 'r')
        enc = fp.read()
        while True:
            key = input_password('Master Password: ', message='Master Password is required.\n')
            try:
                data = AESCipher(key).decrypt_text(enc)
            except ValueError:
                print('Wrong password.')
            else:
                print('Accepted.')
                break
        c = data.splitlines()
        fp.close()
        return c[0], c[1]
    else:
        raise FileNotFoundError('Login is required')


def write_credential(username: str, password: str) -> None:
    path = os.path.join(CONFIG_DIR, CREDENTIALS)

    key = input_password('Master Password: ', message='Master Password is required.\n')
    data = '\n'.join([username, password])
    enc = AESCipher(key).encrypt_text(data)

    fp = open(path, 'w')
    fp.write(enc)
    fp.close()
