import logging
import re
import requests

from myUtil import to_json, special_str_to_json, timestamp, json_to_special_str
from lxml import etree

logging.basicConfig(level=logging.INFO)


class KXue:
    _host = "http://chengyu.kxue.com"

    _pinyin = "/pinyin"

    _cookies = {
        "Hm_lvt_a852cf951acb5ab555bcf768173f1bfc": None,
        "Hm_lpvt_a852cf951acb5ab555bcf768173f1bfc": None,
        "__gads": None,
        "__gpi": None
    }

    _html_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Host": "chengyu.kxue.com",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://chengyu.kxue.com/pinyin/wei.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188"
    }

    def __init__(self):
        self.login()

    def _update_cookies(self):
        ts = timestamp()
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

    def _get(self, url=None, params=None, data=None, headers=None, cookies=None):
        self._update_cookies()

        logging.info("url:<" + str(url) + ">")
        # logging.info("params:<" + str(params) + ">")
        # logging.info("data:<" + str(data) + ">")
        # logging.info("headers:<" + str(headers) + ">")
        logging.info("cookies:<" + str(cookies) + ">")

        return requests.get(url=url, params=params, data=data, headers=headers, cookies=cookies)

    def _post(self, url=None, data=None, json=None, params=None, headers=None, cookies=None):
        self._update_cookies()

        logging.info("url:<" + str(url) + ">")
        # logging.info("params:<" + str(params) + ">")
        # logging.info("json:<" + str(json) + ">")
        # logging.info("data:<" + str(data) + ">")
        # logging.info("headers:<" + str(headers) + ">")
        logging.info("cookies:<" + str(cookies) + ">")

        return requests.post(url=url, data=data, json=json, params=params, headers=headers, cookies=cookies)

    def login(self, url=None, headers=None):
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
        coo = to_json(coo)
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

    def pinyin(self, py=None, headers=None, cookies=None):
        """
        根据拼音查询成语
        :param py: 拼音
        :param headers:
        :param cookies:
        :return: html页面
        """
        if py is None:
            py = ""
        else:
            py = "/" + py + ".html"
        if headers is None:
            headers = self._html_headers
        if cookies is None:
            cookies = self._cookies
        return self._get(url=self._host + self._pinyin + py, headers=headers, cookies=cookies).text


kx = KXue()

with open("../data/html/dddd.html", mode="w", encoding="utf-8") as f:
    f.write(kx.pinyin("weng"))
