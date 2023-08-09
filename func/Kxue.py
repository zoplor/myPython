import inspect
import logging
import re
import textwrap

import requests
from lxml import etree
from requests import Response

from idiom.idiom import IdiomInterface
from myUtil import *

logging.basicConfig(level=logging.INFO)


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


class KXue(IdiomInterface):
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

    def pinyin(self, py=None, headers=None, cookies=None) -> str:
        """
        根据拼音查询成语
        :param py: 拼音
        :param headers:
        :param cookies:
        :return: html
        """
        if py is None:
            py = ""
        else:
            py = "/" + py + ".html"
        if headers is None:
            headers = self._html_headers
        if cookies is None:
            cookies = self._cookies
        r = self._get(url=self._host + self._pinyin + py, headers=headers, cookies=cookies)
        r.encoding = etree.HTML(r.text).xpath("/html/head/meta[1]/@content")[0].split("=")[-1]
        return r.text

    def plus_search(self, title, path=None) -> str:
        """
        通过汉字搜索成语
        :param title: 汉字
        :param path:
        :return: html
        """
        if path is None:
            path = "/plus/search.php"
        return self._get(self._host + path,
                         params={'type': 'view', 'title': bytes(title, 'gbk'), 'x': randint(1, 100), 'y': randint(1, 100)}).text


def get_all_idiom(obj: IdiomInterface, pying: str) -> list[dict[str:str]]:
    """
    根据首字的拼音，查找全部成语，和对应的成语解释
    :param obj: IdiomInterface对象
    :param pying: 汉语拼音
    :return: [{idiom:value,paraphrase:value}]
    """
    logging.info("函数<%s>被调用，pying：%s" % (inspect.stack()[0][3], pying))
    li = []
    if isinstance(obj, KXue):  # 爬取快学网
        ete = etree.HTML(obj.pinyin(pying))
        # 页数，总条数
        page, page_size = ete.xpath("/html/body/div[1]/div[4]/div[2]/div[5]/ul/li/span/strong/text()")
        logging.info("总页数：%s，总条数：%s" % (page, page_size))
        logging.info("当前是第1页")
        # 第一页
        idiom_list = ete.xpath("/html/body/div[1]/div[4]/div[2]/div[5]/div[2]/li[*]/span[1]/a/text()")
        paraphrase_list = ete.xpath("/html/body/div[1]/div[4]/div[2]/div[5]/div[2]/li[*]/span[2]/text()")
        if len(idiom_list) >= len(paraphrase_list):
            # 有一些成语的释义是空的，需要特殊处理
            for i in range(1, len(idiom_list) + 1):
                idiom_list_tmp = ete.xpath("/html/body/div[1]/div[4]/div[2]/div[5]/div[2]/li[%s]/span[1]/a/text()" % i)
                paraphrase_list_tmp = ete.xpath("/html/body/div[1]/div[4]/div[2]/div[5]/div[2]/li[%s]/span[2]/text()" % i)
                if idiom_list_tmp:
                    if paraphrase_list_tmp:
                        li.append({"idiom": idiom_list_tmp[0], "paraphrase": paraphrase_list_tmp[0]})
                    else:
                        logging.warning("成语的释义为空，成语为<%s>" % idiom_list_tmp[0])
                        li.append({"idiom": idiom_list_tmp[0], "paraphrase": ''})
                else:
                    raise Exception("意料之外的错误，没有从html中找到成语")
        else:
            raise Exception("意料之外的错误，释义的数量比成语多")

        # 处理后续的页
        for i in range(2, int(page) + 1):
            logging.info("当前是第%s页" % i)
            time.sleep(randint(100, 200) / 1000)  # 让访问间隔时间更加随机
            ete = etree.HTML(obj.pinyin(pying + "_" + str(i)))
            idiom_list = ete.xpath("/html/body/div[1]/div[4]/div[2]/div[5]/div[2]/li[*]/span[1]/a/text()")
            paraphrase_list = ete.xpath("/html/body/div[1]/div[4]/div[2]/div[5]/div[2]/li[*]/span[2]/text()")
            if len(idiom_list) >= len(paraphrase_list):
                # 有一些成语的释义是空的，需要特殊处理
                for j in range(1, len(idiom_list) + 1):
                    idiom_list_tmp = ete.xpath("/html/body/div[1]/div[4]/div[2]/div[5]/div[2]/li[%s]/span[1]/a/text()" % j)
                    paraphrase_list_tmp = ete.xpath("/html/body/div[1]/div[4]/div[2]/div[5]/div[2]/li[%s]/span[2]/text()" % j)
                    if idiom_list_tmp:
                        if paraphrase_list_tmp:
                            li.append({"idiom": idiom_list_tmp[0], "paraphrase": paraphrase_list_tmp[0]})
                        else:
                            logging.warning("成语的释义为空，成语为<%s>" % idiom_list_tmp[0])
                            li.append({"idiom": idiom_list_tmp[0], "paraphrase": ''})
                    else:
                        logging.warning("idiom_list_tmp:" + str(idiom_list_tmp))
                        logging.warning("paraphrase_list_tmp:" + str(paraphrase_list_tmp))
                        raise Exception("意料之外的错误，没有从html中找到成语")
            else:
                logging.warning("idiom_list长度:%s" % len(idiom_list))
                logging.warning("paraphrase_list长度:%s" % len(paraphrase_list))
                raise Exception("意料之外的错误，释义的数量比成语多")
    return li


kx = KXue()
