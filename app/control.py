import os
import PanoptoDownloader
import PanoptoDownloader.exceptions

from lib.Moodle import Moodle
from lib.Panopto import Panopto

from utils import inputs, credentials, parsers
from utils.logger import get_logger
from utils.arguments import parser
from app import core
from app import plugins


plugins.insert()
logger = get_logger(__name__)

# Variables
ARGS = parser.parse_known_args()[0]

moodle = Moodle()
panopto = Panopto()


def init() -> None:
    username = inputs.input_not_empty('Username: ', message='Username is required.\n')
    password = inputs.input_password('Password: ', message='Password is required.\n')

    try:
        moodle.login(username, password)
    except Exception as e:
        logger.error('LOGIN ERROR: %s', str(e))
    else:
        logger.info('Login successful\n')
        credentials.write_credential(username, password)

        logger.info('INIT completed')
        if inputs.input_yesno('Get courses now [Y, n]? '):
            update(username, password)


def update(username, password) -> None:
    try:
        moodle.login(username, password)
    except Exception as e:
        logger.error('LOGIN ERROR: %s', str(e))
    else:
        logger.info('UPDATE started')

        try:
            courses = moodle.get_courses()
        except Exception as e:
            logger.error('GET_COURSES ERROR: %s', str(e))
        else:
            core.write_courses(courses)
            logger.info('UPDATE completed')


def sync(username, password) -> None:
    try:
        moodle.login(username, password)
        panopto.login_with_moodle((moodle.session, moodle.ORIGIN))
    except Exception as e:
        logger.error('LOGIN ERROR: %s', str(e))
    else:
        logger.info('SYNC started')

        if not os.path.isdir(ARGS.sync_dir):
            os.makedirs(ARGS.sync_dir)

        courses = core.get_courses()
        for course in courses:
            lessons = moodle.get_video_lessons(course['id'])
            new_lessons = core.get_new_lessons(lessons)

            if not len(new_lessons):
                logger.info('No new lessons found in "%s"', course['name'])
                continue
            logger.info('%s new lessons found in "%s"', len(new_lessons), course['name'])

            for lesson in new_lessons:
                lesson['course'] = course['id']  # Add CourseID to lesson

                if not ARGS.skip_download:
                    folder = '{id}_{name}'.format(id=course['id'],
                                                  name=parsers.slugify(course['name']))
                    path = os.path.join(ARGS.sync_dir, folder)
                    if not os.path.isdir(path):
                        os.mkdir(path)

                    url = panopto.get_video_lesson_stream_url(lesson['id'])
                    if not url:
                        logger.warning('"%s" stream URL not ready yet', lesson['name'])
                        continue

                    filename = '{name}_{id}.{extension}'.format(id=lesson['id'],
                                                                name=parsers.slugify(lesson['name']),
                                                                extension=ARGS.video_format)
                    output = os.path.join(path, filename)

                    if not os.path.exists(output):
                        logger.info('Download "%s"', lesson['name'])
                        plugins.event('download_started', course, lesson)

                        def callback(progress: int) -> None:
                            plugins.event('download', course, lesson, progress)
                        try:
                            PanoptoDownloader.download(url, output, callback)

                        except KeyboardInterrupt as interrupt:
                            plugins.event('download_error', course, lesson, interrupt)
                            if os.path.exists(output):
                                logger.debug('File "%s" removed', output)
                                os.remove(output)
                            raise interrupt
                        except Exception as e:
                            plugins.event('download_error', course, lesson, e)
                            logger.error('%s', str(e))
                            if os.path.exists(output):
                                logger.debug('File "%s" removed', output)
                                os.remove(output)
                        else:
                            plugins.event('download_completed', course, lesson, output)
                            logger.debug('Download completed')
                            core.write_new_lessons(lesson)

                            plugins.event('download_done', course, lesson, output)
                    else:
                        logger.info('Lesson "%s" already downloaded', lesson['name'])
                        core.write_new_lessons(lesson)
                        plugins.event('download_done', course, lesson, output)
                else:
                    core.write_new_lessons(lesson)
        logger.info('SYNC completed')


def clean() -> None:
    pass


def close() -> None:
    if moodle.is_logged:
        logger.info('Logout')
        moodle.logout()
