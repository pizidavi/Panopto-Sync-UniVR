import requests
from requests.exceptions import RequestException
from .exceptions import *

from utils import parsers


class Panopto:

    ORIGIN = 'https://univr.cloud.panopto.eu'

    def __init__(self):
        self.__auth = None

    def login_with_moodle(self, moodle: tuple[str, str]) -> None:
        """
        :param moodle: (MoodleSession, MoodleReferer)
        """
        if not moodle[0]:
            raise ValueError('Moodle-Session is required')
        if not moodle[1]:
            raise ValueError('Moodle-Referer is required')

        url = '{}/Panopto/Pages/Auth/Login.aspx'.format(self.ORIGIN)
        r = requests.get(url, cookies={'MoodleSession': moodle[0]}, headers={'referer': moodle[1]})

        if 200 <= r.status_code < 300:
            c = parsers.cookie_parser(r.request.headers['Cookie'])
            if '.ASPXAUTH' in c:
                self.__auth = c['.ASPXAUTH']
            else:
                raise LoginFail('Login failed')
        else:
            raise RequestException('RequestException')

    def get_video_lesson_stream_url(self, lesson_id) -> str:
        """
        :param lesson_id: Lesson ID (ID parameter in URL https://univr.cloud.panopto.eu/[...]?id=* )
        :return: master.m3u8 URL
        """
        if not self.__auth:
            raise ValueError('Login required')
        if not lesson_id:
            raise ValueError('LessonID is required')

        url = '{}/Panopto/Pages/Viewer/DeliveryInfo.aspx'.format(self.ORIGIN)
        data = {
            'deliveryId': lesson_id
        }
        r = requests.post(url, data, cookies={'.ASPXAUTH': self.__auth})

        if 200 <= r.status_code < 300:
            xml = parsers.xml_parser(r.text)

            error = xml.find('ErrorCode')
            if error is None:
                try:
                    # stream = xml.find('Delivery').find('Streams').find('StreamUrl').text
                    stream = xml.find('Delivery').find('PodcastStreams').find('StreamUrl').text
                    return stream.split('?')[0]
                except Exception:
                    return None
            else:
                raise Exception(error.text)
        else:
            raise RequestException('RequestException')
