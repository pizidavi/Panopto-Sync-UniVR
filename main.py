import utils.logger as logging
logging.set_level(20)

from utils import credentials
from utils.arguments import parser
from app import control

logger = logging.get_logger(__name__)


def main(args):

    if args.action == 'init':
        control.init()

    elif args.action == 'update':
        username, password = credentials.get_credential()
        control.update(username, password)

    elif args.action == 'sync':
        username, password = credentials.get_credential()
        if args.no_repeat:
            control.sync(username, password)
        else:
            import time
            while True:
                control.sync(username, password)
                time.sleep(args.every * 60)

    # elif ARGS.action == 'clean':
    #     control.clean()


if __name__ == '__main__':
    try:
        main(parser.parse_args())
    except KeyboardInterrupt:
        pass
    finally:
        control.close()
