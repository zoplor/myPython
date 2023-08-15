import logging
import textwrap
from functools import wraps

import requests
from lxml import etree
from requests import Response

from idiom.IdiomInterface import IdiomInterface
from util.myUtil import *

logging.basicConfig(level=logging.ERROR)


def print_roundtrip(response, *args, **kwargs):
    """
    打印http报文
    :param response:
    :param args:
    :param kwargs:
    :return:
    """
    format_headers = lambda d: '\n'.join(f'{k}: {v}' for k, v in d.items())
    logging.debug(textwrap.dedent('''
        --------------------------------------------------- request ------------------------------------------------
        {req.method} {req.url}
        {request_headers}

        --------------------------------------------------- response -----------------------------------------------
        {res.status_code} {res.reason} {res.url}
        {response_headers}
    ''').format(
        req=response.request,
        res=response,
        request_headers=format_headers(response.request.headers),
        response_headers=format_headers(response.headers),
    ))


def set_encoding(_type="text"):
    """
    一个装饰器，实现给response对象设置encoding，并返回对应的返回值
    :param _type: 返回值类型，text/json/content
    :return:
    """

    def encoding(func):
        @wraps(func)
        def encod(*args):
            r = func(*args)
            try:
                et = etree.HTML(r.text)
                tmp = et.xpath("/html/head/meta[1]/@content")
                tmp = tmp[0].split("=")
                tmp = tmp[-1]
                r.encoding = tmp
            except Exception as e:
                logging.warning(e)

            if _type == "json":
                return r.json()
            elif _type == "content":
                return r.content
            else:
                return r.text

        return encod

    return encoding


class KXueImpl(IdiomInterface):
    _host = "http://chengyu.kxue.com"

    _cookies = {
        "Hm_lvt_a852cf951acb5ab555bcf768173f1bfc": None,
        "Hm_lpvt_a852cf951acb5ab555bcf768173f1bfc": None,
        "__gads": None,
        "__gpi": None
    }

    _headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Host": "chengyu.kxue.com",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://chengyu.kxue.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"
    }

    def __init__(self):
        self.login()

    def _update_cookies(self):
        ts = str(strptime(_class=TimeClass.SECOND.value))
        if self._cookies['__gads']:
            __gads = special_str_to_json(self._cookies['__gads'])
            __gads['RT'] = ts
            self._cookies['__gads'] = json_to_special_str(__gads)
        if self._cookies['__gpi']:
            __gpi = special_str_to_json(self._cookies['__gpi'])
            __gpi['RT'] = ts
            self._cookies['__gpi'] = json_to_special_str(__gpi)
        if self._cookies['Hm_lpvt_a852cf951acb5ab555bcf768173f1bfc']:
            self._cookies['Hm_lpvt_a852cf951acb5ab555bcf768173f1bfc'] = ts

    def _get(self, url=None, params=None, data=None, headers=None, cookies=None) -> Response:
        self._update_cookies()
        return requests.get(url=url, params=params, data=data, headers=headers, cookies=cookies,
                            hooks={'response': print_roundtrip})

    def _post(self, url=None, data=None, json=None, params=None, headers=None, cookies=None) -> Response:
        self._update_cookies()
        return requests.post(url=url, data=data, json=json, params=params, headers=headers, cookies=cookies,
                             hooks={'response': print_roundtrip})

    def login(self, url=None, headers=None) -> dict[str:str]:
        """
        获取cookies，并设置cookies
        :param url: 登录的url
        :param headers: 请求头
        :return:
        """
        if url is None:
            url = "https://partner.googleadservices.com/gampad/cookie.js"
        if headers is None:
            headers = {
                'authority': 'partner.googleadservices.com',
                'method': 'GET',
                'path': '/gampad/cookie.js?domain=chengyu.kxue.com&callback=_gfp_s_&client=ca-pub-2803462541247190',
                'scheme': 'https',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Referer': 'http://chengyu.kxue.com/',
                'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'script',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188'
            }
        params = {
            "domain": "chengyu.kxue.com",
            "callback": "_gfp_s_",
            "client": "ca-pub-2803462541247190"
        }
        if self._cookies['__gads']:
            params['cookie'] = self._cookies['__gads']
        if self._cookies['__gpi']:
            params['gpic'] = self._cookies['__gpi']

        res = self._get(url=url, headers=headers, params=params).text
        # 拿到cookies json
        coo = re.findall('%s\((.*?)\);' % (params['callback']), res)[0]
        coo = str_to_json(coo)
        # 从json中取出__gads、__gpi
        __gads = coo['_cookies_'][0]['_value_']
        __gpi = coo['_cookies_'][1]['_value_']
        # 从__gads中取出RT、T
        di = special_str_to_json(__gads)
        self._cookies['Hm_lvt_a852cf951acb5ab555bcf768173f1bfc'] = di["T"]
        self._cookies['Hm_lpvt_a852cf951acb5ab555bcf768173f1bfc'] = di["RT"]
        self._cookies['__gads'] = __gads
        self._cookies['__gpi'] = __gpi

        return self._cookies

    @set_encoding(_type="text")
    def pinyin(self, py, headers=None):
        """
        根据拼音查询以该拼音开头的成语，可以查出全部符合条件的成语
        :param py: 拼音或者单独的一个字母
        :param headers:
        :return: html
        """
        if headers is None:
            headers = self._headers
        path = "/pinyin/%s.html" % py
        return self._get(url=self._host + path, headers=headers, cookies=self._cookies)

    @set_encoding(_type="text")
    def plus_search(self, title, path=None, headers=None):
        """
        通过汉字或者拼音搜索成语，可以在前面使用%来查询非title开头的成语，不使用%时是查询该拼音或者汉字开头的成语。最多只能查到200个
        :param title: 搜索条件，汉字或者拼音，可以包含%符号
        :param path:
        :param headers:
        :return: html
        """
        if headers is None:
            headers = self._headers

        if path is None:
            path = "/plus/search.php"
        if content_chinese_char(title):
            # 如果包含中文使用gbk编码
            title = bytes(title, 'gbk')
        return self._get(self._host + path, params={'type': 'view', 'title': title, 'x': randint(1, 100), 'y': randint(1, 100)},
                         headers=headers, cookies=self._cookies)

    @set_encoding(_type="text")
    def list_xzi(self, xzi: str, headers=None):
        """
        通过字数来查找满足条件的成语，可以查出全部符合条件的成语
        :param xzi: 成语字数，例如想找四个字的成语，就输入4zi
        :param headers:
        :return:
        """
        if headers is None:
            headers = self._headers
        return self._get(url=self._host + "/list/%s.html" % xzi, headers=headers, cookies=self._cookies)

    @set_encoding(_type="text")
    def list_shang_xia_ju(self, path=None, headers=None):
        """
        返回有上下句的成语
        :param path:
        :param headers:
        :return:
        """
        if headers is None:
            headers = self._headers
        if path is None:
            path = "/list/shangxiaju.html"
        else:
            path = "/list/%s.html" % path
        return self._get(url=self._host + path, headers=headers, cookies=self._cookies)
