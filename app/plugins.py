import os
import inspect

from utils.logger import get_logger
from utils import inputs

logger = get_logger(__name__)

BASE = './'
FOLDER = 'plugins'
FILE = 'plugins.json'
PLUGINS = []


def insert() -> None:
    path = os.path.join(BASE, FILE)
    data = inputs.open_json_file(path)

    for plugin in data:
        if 'module' not in plugin:
            logger.error('Module name is missing')
            continue
        if 'disable' in plugin and plugin['disable']:
            continue

        _class = _get_class(plugin['module'])
        if not _class:
            logger.warning('No plugin found for "%s" in ./plugins folder', plugin['module'])
            continue

        PLUGINS.append(_class(plugin['options'] if 'options' in plugin else {}))
        logger.debug('%s imported', plugin['module'])


def event(method: str, *args) -> None:
    run(f'on_{method}', *args)


def run(method: str, *args) -> None:
    for plugin in PLUGINS:
        if hasattr(plugin, method):
            try:
                getattr(plugin, method)(*args)
            except Exception as e:
                logger.error('%s', str(e))


def _get_class(name: str) -> classmethod or None:
    for element in os.listdir(FOLDER):
        path = os.path.join(BASE, FOLDER, element)
        if not os.path.isdir(path):
            continue
        try:
            module = getattr(__import__(f'{FOLDER}.{element}', fromlist=['main']), 'main')
        except AttributeError:
            continue
        else:
            def is_class_member(member: classmethod):
                return inspect.isclass(member) and member.__module__ == module.__name__
            classes = inspect.getmembers(module, is_class_member)
            if not len(classes):
                continue

            for _class in classes:
                if _class[0] == name:
                    return _class[1]
    return None
