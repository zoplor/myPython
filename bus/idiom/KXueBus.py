import inspect
import logging

from lxml import etree

from idiom.IdiomInterface import IdiomInterface
from idiom.impl.KxueImpl import KXueImpl
from util.myUtil import *

logging.basicConfig(level=logging.ERROR)


def _get_all_idiom(func, param, page: int, idiom_jpath: str, paraphrase_jpath: str):
    logging.info("函数<%s>被调用" % inspect.stack()[0][3])

    li = []
    # 分页查出全部
    for i in range(1, page + 1):
        logging.info("当前是第%s页" % i)
        time.sleep(randint(100, 800) / 1000)  # 让访问间隔时间更加随机
        ete = etree.HTML(func(param + "_" + str(i)))
        idiom_list = ete.xpath(idiom_jpath % "*")
        for j in range(1, len(idiom_list) + 1):
            idiom_list_tmp = ete.xpath(idiom_jpath % j)
            paraphrase_list_tmp = ete.xpath(paraphrase_jpath % j)
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
        logging.debug("li的值：%s" % li)
    return li


def get_all_idiom_by_head(obj: IdiomInterface, pying: str) -> list[dict[str:str]]:
    """
    查找指定拼音开头的全部成语，和对应的成语解释
    :param obj: IdiomInterface对象
    :param pying: 汉语拼音
    :return: [{idiom:value,paraphrase:value}]
    """
    logging.info("函数<%s>被调用，pying：%s" % (inspect.stack()[0][3], pying))

    if isinstance(obj, KXueImpl):  # 爬取快学网
        try:
            ete = etree.HTML(obj.pinyin(pying))
            # 页数，总条数
            page, size = ete.xpath("/html/body/div[1]/div[4]/div[2]/div[5]/ul/li/span/strong/text()")
            logging.info("总页数：%s，总条数：%s" % (page, size))
            idiom_jpath = "/html/body/div[1]/div[4]/div[2]/div[5]/div[2]/li[%s]/span[1]/a/text()"
            paraphrase_jpath = "/html/body/div[1]/div[4]/div[2]/div[5]/div[2]/li[%s]/span[2]/text()"
            return _get_all_idiom(obj.pinyin, pying, int(page), idiom_jpath, paraphrase_jpath)
        except Exception as e:
            logging.warning(e)
    return []


def get_all_idiom_by_word_count(obj: IdiomInterface, word_count: int) -> list[dict[str:str]]:
    """
    按成语的字数查出全部符合条件的成语
    :param obj:
    :param word_count: 字数，例如查询四个字的成语，可以输入4
    :return: [{idiom:value,paraphrase:value}]
    """
    if isinstance(obj, KXueImpl):  # 爬取快学网
        try:
            ete = etree.HTML(obj.list_xzi(str(word_count) + "zi"))
            # 页数，总条数
            page, size = re.findall('(\d+)', ete.xpath("/html/body/div[1]/div[4]/div[2]/div[4]/ul/li[1]/span/text()")[0])
            logging.info("总页数：%s，总条数：%s" % (page, size))
            idiom_jpath = "/html/body/div[1]/div[4]/div[2]/div[4]/div[2]/li[%s]/span[1]/a/text()"
            paraphrase_jpath = "/html/body/div[1]/div[4]/div[2]/div[4]/div[2]/li[%s]/span[2]/text()"
            return _get_all_idiom(obj.list_xzi, str(word_count) + "zi", int(page), idiom_jpath, paraphrase_jpath)
        except Exception as e:
            logging.warning(e)
    return []


def get_all_idiom_by_shang_xia_ju(obj: IdiomInterface) -> list[dict[str:str]]:
    """
    获取所有有上下句的成语
    :param obj:
    :return:
    """
    if isinstance(obj, KXueImpl):  # 爬取快学网
        try:
            ete = etree.HTML(obj.list_shang_xia_ju())
            page, size = re.findall('(\d+)', ete.xpath("/html/body/div[1]/div[4]/div[2]/div[4]/ul/li[1]/span/text()")[0])
            logging.info("总页数：%s，总条数：%s" % (page, size))
            idiom_jpath = "/html/body/div[1]/div[4]/div[2]/div[4]/div[2]/li[%s]/span[1]/a/text()"
            paraphrase_jpath = "/html/body/div[1]/div[4]/div[2]/div[4]/div[2]/li[%s]/span[2]/text()"
            return _get_all_idiom(obj.list_shang_xia_ju, "shangxiaju", int(page), idiom_jpath, paraphrase_jpath)
        except Exception as e:
            logging.warning(e)
    return []


def get_all_idiom_by_word_count_list(obj: IdiomInterface, word_count_range: tuple[int, int]) -> list[dict[str:str]]:
    """
    获取在指定范围内的字数的全部成语，并生成json文件写入../data/json/目录下
    :param obj:
    :param word_count_range: (最小字数，最大字数)
    :return:
    """
    li = []
    # 获取有上下句的成语
    shang_xia_ju = []
    try:
        logging.info("正在抓取有上下句的成语")
        shang_xia_ju = get_all_idiom_by_shang_xia_ju(obj)
        logging.debug("抓取到有上下句的成语：%s" % shang_xia_ju)
    except Exception as e:
        logging.error(e)
        logging.warning("没有抓取到有上下句的成语")

    # 分别获取有x个字的成语，并把有上下句的成语合并进去
    for i in range(word_count_range[0], word_count_range[1] + 1):
        logging.info("当期处理字数为%s的成语" % i)
        shang_xia_ju_xzi = list(filter(lambda x: count_cn_char(x['idiom']) == i, shang_xia_ju))
        logging.debug("shang_xia_ju_xzi(%s字):%s" % (i, shang_xia_ju_xzi))

        idiom_list = []
        try:
            idiom_list = get_all_idiom_by_word_count(obj, i)
            li = li + idiom_list
            logging.info("抓取字数为%s个的成语" % i)
        except Exception as e:
            logging.error(e)
            logging.warning("没有抓取到字数为%s个的成语" % i)

        if shang_xia_ju_xzi:
            logging.warning("合并%s字成语和%s字的有上下句的成语，合并策略：set" % (i, i))
            for j in idiom_list:
                shang_xia_ju_xzi = sifer(shang_xia_ju_xzi, mode="equal", reverse=True, idiom=j['idiom'])
            logging.debug("过滤后的shang_xia_ju_xzi(%s字):%s" % (i, shang_xia_ju_xzi))
            idiom_list = idiom_list + shang_xia_ju_xzi

        if idiom_list:
            json_to_str(idiom_list, "../../data/json/all_%szi_idiom.json" % i)
            logging.info("写入了一个文件，文件名：all_%szi_idiom.json" % i)
    return li


