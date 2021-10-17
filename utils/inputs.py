import json
import os.path
import getpass


def input_not_empty(*args, message=None) -> str:
    data = None
    while not data:
        data = input(*args)
        if not data and message:
            print(message)
    return data


def input_password(prompt, message=None) -> str:
    pwd = None
    while not pwd:
        pwd = getpass.getpass(prompt=prompt)
        if not pwd and message:
            print(message)
    return pwd


def input_yesno(*args) -> bool:
    r = None
    while r not in ['Y', 'N']:
        r = input(*args).upper()
        if r == 'Y':
            return True
        elif r == 'N':
            return False
        else:
            print('Invalid. Use Y or N', end='\n\n')


def open_json_file(path: str, default: list or dict = []) -> list or dict:

    if os.path.isfile(path):
        fp = open(path, 'r')
        data = json.load(fp)
        fp.close()
        return data
    else:
        # folder = os.path.split(path)[0]
        # if not os.path.isdir(folder):
        #     os.makedirs(folder)

        fp = open(path, 'w')

        sample_file = f'{path}.sample'
        if os.path.isfile(sample_file):
            sample = open(sample_file, 'r')
            read = sample.read()
            fp.write(read)
            sample.close()
            
            data = json.loads(read)
        else:
            fp.write(str(default))
            data = default
        fp.close()
        return data

    # try:
    #     fp = open(path, 'r')
    # except FileNotFoundError:
    #     fp = open(path, 'w')
    #     
    #     try:
    #         sample = open(f'{path}.sample', 'r')
    #     except FileNotFoundError:
    #         fp.write(str(default))
    #     else:
    #         fp.write(sample.read())
    #         sample.close()
    #     fp.close()
    #     return default
    # else:
    #     data = json.load(fp)
    #     fp.close()
    #     return data
