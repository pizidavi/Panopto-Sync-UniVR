import requests
from requests.exceptions import RequestException
from .exceptions import *

from utils import parsers


class Moodle:

    ORIGIN = 'https://moodledidattica.univr.it'
    SSO = 'https://aap.univr.it'

    def __init__(self):
        self.__session = None
        self.__sess_key = None

    @property
    def session(self) -> str or None:
        return self.__session

    @property
    def is_logged(self) -> bool:
        return self.__session and self.__sess_key

    def login(self, username: str, password: str) -> None:
        """
        :param username
        :param password
        """
        if not username:
            raise ValueError('Username is required')
        if not password:
            raise ValueError('Password is required')

        if self.__session is None and self.__sess_key is None:
            url = '{}/auth/shibboleth/index.php'.format(self.ORIGIN)
            cookies = None
        else:
            url = '{}/'.format(self.ORIGIN)
            cookies = {'MoodleSession': self.__session}

        r = requests.get(url, cookies=cookies)

        if 200 <= r.status_code < 300:
            if self.SSO in r.url:
                html = parsers.html_parser(r.text)
                form = html.find('form', attrs={'name': 'loginData'})
                if not form:
                    raise RuntimeError('Form not found')

                method = form.get('method')
                action = self.SSO + form.get('action')
                data = {
                    'form_username': username,
                    'form_password': password,
                    'request_id': form.find('input', attrs={'name': 'request_id'}).get('value'),
                    'form_spidprovider': 'nospid'
                }

                re = requests.request(method, action, data=data, cookies=r.cookies,
                                      headers={'Content-Type': 'application/x-www-form-urlencoded'})
                if 200 <= re.status_code < 300:
                    _html = parsers.html_parser(re.text)
                    _form = _html.find('form')
                    if not _form:
                        raise RuntimeError('_Form not found')

                    login_failed = _form.find('p', attrs={'class': 'loginFailed'})
                    if login_failed:
                        raise RuntimeError('Authentication failed')

                    _method = _form.get('method')
                    _action = _form.get('action')
                    _cookie = {
                        **r.cookies.get_dict(),
                        **re.cookies.get_dict()
                    }
                    _data = {
                        'SAMLResponse': _form.find('input', attrs={'name': 'SAMLResponse'}).get('value'),
                        'RelayState': _form.find('input', attrs={'name': 'RelayState'}).get('value')
                    }
                    req = requests.request(_method, _action, data=_data, cookies=_cookie,
                                           headers={'Content-Type': 'application/x-www-form-urlencoded'})
                    if 200 <= req.status_code < 300:
                        if len(req.history):
                            self.__session = req.history[-1].cookies.get('MoodleSession')
                        else:
                            raise SessionMissing('Session cannot be found')

                        page = parsers.html_parser(req.text)
                        i = page.find('input', attrs={'name': 'sesskey'})
                        if i:
                            self.__sess_key = i.get('value')
                        else:
                            raise SessKeyMissing('Sesskey cannot be found')
                    else:
                        raise RequestException('RequestException')
                else:
                    raise RequestException('RequestException')
            elif self.ORIGIN in r.url:  # Already logged
                pass
            else:
                raise RequestException('RequestException')
        else:
            raise RequestException('RequestException')

    def login_with_session(self, session: str) -> None:
        """
        Login using given MoodleSession
        :param session: MoodleSession cookie
        """
        if not session:
            raise ValueError('Session is required')

        url = '{}/'.format(self.ORIGIN)
        r = requests.get(url, cookies={'MoodleSession': session})

        if 200 <= r.status_code < 300:
            if self.ORIGIN in r.url:
                page = parsers.html_parser(r.text)
                i = page.find('input', attrs={'name': 'sesskey'})
                if i:
                    self.__session = session
                    self.__sess_key = i.get('value')
                else:
                    raise LoginFail('Login failed')
            else:
                raise LoginFail('Login failed')
        else:
            raise RequestException('RequestException')

    def get_courses_yield(self) -> dict:
        """
        :return: Courses
        """
        if not self.__session or not self.__sess_key:
            raise ValueError('Login required')

        url = '{}/my/'.format(self.ORIGIN)
        r = requests.get(url, cookies={'MoodleSession': self.__session})

        if 200 <= r.status_code < 300:
            html = parsers.html_parser(r.text)
            for a in html.find_all('a', attrs={'data-parent-key': 'mycourses'}):
                _id = int(a.get('data-key') or '0')
                name = a.find('span', class_='media-body').text
                yield {
                    'id': _id,
                    'name': name
                }
        elif 302 <= r.status_code <= 303:
            raise LoginFail('Login failed')
        else:
            raise RequestException('RequestException')

    def get_courses(self) -> list[dict]:
        return list(self.get_courses_yield())

    def get_video_lessons_yield(self, course_id: int) -> dict:
        """
        :param course_id: Course ID (ID parameter in URL: moodledidattica.univr.it/[...]?id=* )
        :return: Lessons
        """
        if not self.__session or not self.__sess_key:
            raise ValueError('Login required')
        if not course_id:
            raise ValueError('CourseID is required')

        url = '{}/blocks/panopto/panopto_content.php'.format(self.ORIGIN)
        data = {
            'sesskey': self.__sess_key,
            'courseid': course_id
        }
        r = requests.post(url, data, cookies={'MoodleSession': self.__session})

        if 200 <= r.status_code < 300:
            html = parsers.html_parser(r.text)
            for div in html.find_all('div', class_='listItem'):
                a = div.find('a')
                if a:
                    _id = parsers.url_query_parser(a.get('href'))
                    name = a.text
                    yield {
                        'id': _id['id'][0] if 'id' in _id else None,
                        'name': name
                    }
        elif r.status_code == 400:
            raise LoginFail('Login failed')
        else:
            raise RequestException('RequestException')

    def get_video_lessons(self, course_id: int) -> list[dict]:
        return list(self.get_video_lessons_yield(course_id))

    def logout(self) -> None:
        if not self.__session or not self.__sess_key:
            raise ValueError('Login required')

        url = '{}/login/logout.php?sesskey={}'.format(self.ORIGIN, self.__sess_key)
        r = requests.post(url, cookies={'MoodleSession': self.__session})

        if 200 <= r.status_code < 300:
            self.__session = None
            self.__sess_key = None
        else:
            raise RequestException('RequestException')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
