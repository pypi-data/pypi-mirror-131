#!/usr/bin/env python2

from __future__ import print_function
import sys
import re
if sys.version_info.major == 3:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse
try:
    from pydebugger.debug import debug
except:
    def debug(*args, **kwargs):
        return ''
from make_colors import make_colors
from pprint import pprint

def set_header(header_str = None, url = '', origin = '', cookies = None, user_agent = None, content_type = None, accept = None, content_length = '', **kwargs):
    """generate mediafire url to direct download url

    Args:
        header_str (str, optional): raw headers data/text from browser on development mode
        url (str, optional): for referer tag
        origin (str, optional): for origin tag

    Returns:
        TYPE: dict: headers data
    """
    user_agent = user_agent or "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"
    content_type = content_type or "application/x-www-form-urlencoded"
    accept = accept or "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    if content_length:
        content_length = "\n" + "content-length: {}".format(str(content_length))
    if url and origin:
        origin = urlparse(url)
        origin = "\n" + "origin: " + origin.scheme + "://" + origin.netloc

    elif not url and origin:
        origin = urlparse(origin)
        origin = "\n" + "origin: " + origin.scheme + "://" + origin.netloc

    if url:
        url = "\n" + "referer: {}".format(url)
    else:
        url = ''
    cookie = ''
    debug(origin = origin)
    if cookies:
        if isinstance(cookies, dict):
            cookie = ''
            for i in cookies:
                cookie += str(i) + "=" + cookies.get(i) + "; "
            debug(cookie = cookie)
        elif isinstance(cookies, str):
            debug(cookies = cookies)
            cookie_1 = filter(None, re.split(";", cookies))
            debug(cookie_1 = cookie_1)
            for i in cookie_1:
                key, value = i.split("=", 1)
                cookie += key.strip() + "=" + value.strip() + "; "
            debug(cookie = cookie)
        else:
            print(make_colors("warning:", 'lw', 'r') + " " + make_colors("cookies must be type dict or string with format 'key=value;' with must be end with ';'", 'y'))
    debug(cookie = cookie)
    if cookie:
        cookie = "\n" + "cookie: " + cookie.strip()[:-1]
        debug(cookie = cookie)
    if not header_str:
        header_str ="""cache-control:	max-age=0
    upgrade-insecure-requests:	1{}
    content-type:	{}
    user-agent:	{}
    accept:	{}
    sec-fetch-site:	same-origin
    sec-fetch-mode:	navigate
    sec-fetch-user:	?1
    sec-fetch-dest:	document{}
    accept-encoding:	gzip, deflate
    accept-language:	en-US,en;q=0.9,id;q=0.8,ru;q=0.7{}{}""".format(origin, content_type, user_agent, accept, url, cookie, content_length)

    if header_str:
        debug(cookie = cookie)
        header_str += origin + url + cookie

    debug(header_str = header_str)
    header_str = list(filter(None, re.split("\n|\r|\t\t", header_str)))
    debug(header_str = header_str)
    headers = {key.strip().lower():value.strip() for key,value in [re.split(": |:\t", i) for i in header_str]}
    debug(headers = headers)
    if kwargs:
        for key in kwargs:
            value = kwargs.get(key)
            key = re.sub(" |_", "-", key).lower()
            headers.update({key: value})
    debug(headers = headers)
    return headers

def headers(*args, **kwargs):
    return set_header(*args, **kwargs)

def usage():

    import argparse
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument('HEADERS', help = 'string of headers, usually copy from dev tool browser, or type "c" for get string from clipboard', action='store')
    parser.add_argument('-u', '--url', help = 'Add url referer to url', action = 'store')
    parser.add_argument('-o', '--origin', help = 'Add url origin to url', action = 'store')
    parser.add_argument('-c', '--cookies', help = 'Add cookie, format: "key=value;", must end with ";"')
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        debug(args_HEADERS = args.HEADERS)
        if args.HEADERS == 'c':
            try:
                import clipboard
                args.HEADERS = clipboard.paste()
            except:
                print(make_colors("Please install `clipboard` before (pip install clipboard) !", 'lw', 'r'))


        headers = set_header(args.HEADERS, args.url, args.origin, args.cookies)
        pprint(headers)

if __name__ == '__main__':
    usage()




