from http.cookies import SimpleCookie
from urllib import parse
from bs4 import BeautifulSoup


def cookie_parser(raw: str) -> dict:
    cookie = SimpleCookie(raw)
    return dict((k, v.value) for k, v in cookie.items())


def url_query_parser(raw: str) -> dict:
    return parse.parse_qs(parse.urlsplit(raw).query)


def html_parser(raw: str) -> BeautifulSoup:
    return BeautifulSoup(raw, 'html.parser')


def xml_parser(raw: str) -> BeautifulSoup:
    return BeautifulSoup(raw, 'xml')


def slugify(raw: str) -> str:
    raw = ''.join(i for i in raw.replace('/', '-') if i not in '\\:*?<>|')
    return ' '.join(raw.split())
