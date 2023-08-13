import json
import random
import re
import sys
import time
from datetime import datetime
from enum import Enum, unique
from typing import Any

import jsonpath as jsonpath


@unique
class TimeClass(Enum):
    SECOND = 1.0
    MILLI_SECOND = 1000.0
    MICRO_SECOND = 1000000.0


def std_input() -> list:
    """
    从控制台获取多行输入
    :return: list<line>
    """
    line = []
    try:
        for i in sys.stdin:
            line.append(i.strip())
    except KeyError:
        pass
    return line


def header_str_to_dict(lines: list) -> dict:
    """
    把str转成header
    :param lines: list
    :return: dict
    """
    if len(lines) % 2 != 0:
        raise Exception("Wrong number of list elements!")
    headers = {}
    for i in range(0, int(len(lines) / 2)):
        headers[lines[2 * i][0:-1]] = lines[2 * i + 1]
    return headers


def print_json(js, indent=4, ensure_ascii=False, sort_keys=False) -> None:
    """
    美化输出json
    :param js:要输入的数据
    :param indent:
    :param ensure_ascii:
    :param sort_keys:
    :return:
    """
    try:
        if type(js) == str:
            print(json.dumps(json.loads(js), indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys))
        elif type(js) in (dict, list, tuple):
            print(json.dumps(js, indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys))
        elif type(js) == set:
            print(json.dumps(list(js), indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys))
        else:
            print(js)
    except Exception as e:
        print(js)


def str_to_json(s, _type="string", cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None,
                object_pairs_hook=None, **kw) -> Any:
    """
    字符串或者文件转python数据类型
    :param s:字符串
    :param _type:数据来源，string：来源于python对象，file：从文件中读取
    :param cls:
    :param object_hook:
    :param parse_float:
    :param parse_int:
    :param parse_constant:
    :param object_pairs_hook:
    :param kw:
    :return:
    """
    if _type == "string":
        return json.loads(s, cls=cls, object_hook=object_hook, parse_float=parse_float, parse_int=parse_int,
                          parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)
    elif _type == "file":
        with open(s, "r", encoding="utf-8") as f:
            return json.load(f, cls=cls, object_hook=object_hook, parse_float=parse_float, parse_int=parse_int,
                             parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)
    else:
        raise Exception("Invalid type!")


def json_to_str(obj, fp=None, skipkeys=False, ensure_ascii=False, check_circular=True, allow_nan=True, cls=None, indent=4,
                separators=None, default=None, sort_keys=False, **kw) -> str | None:
    """
    把python类型转字符串，或者转换后并写入文件
    :param obj:要转换的对象
    :param fp:为空：返回转换后的字符串，不为空：把数据转化为文件写入fp路径
    :param skipkeys:
    :param ensure_ascii:
    :param check_circular:
    :param allow_nan:
    :param cls:
    :param indent:
    :param separators:
    :param default:
    :param sort_keys:
    :param kw:
    :return:
    """
    if fp is None:
        return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                          allow_nan=allow_nan, cls=cls, indent=indent, separators=separators, default=default,
                          sort_keys=sort_keys, **kw)
    else:
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(obj, f, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                      allow_nan=allow_nan, cls=cls, indent=indent, separators=separators, default=default,
                      sort_keys=sort_keys, **kw)
        return None


def special_str_to_json(sp: str) -> dict:
    di = {}
    for i in sp.split(":"):
        di[i.split("=")[0]] = i.split("=")[1]
    return di


def json_to_special_str(js: dict) -> str:
    sp = ""
    for k, v in js.items():
        sp = sp + k + "=" + v + ":"
    sp = sp[0:-1]
    return sp


def strptime(_date=None, _format="%Y-%m-%d %H:%M:%S", _class=TimeClass.SECOND.value) -> int:
    """
    日期转时间戳，默认返回当前时间戳
    :param _date: 日期字符串
    :param _format: 日期格式
    :param _class: 时间戳精度等级，秒/毫秒/微妙，s/ms/μs
    :return: 时间戳
    """
    if _date is None:
        return int(time.time() * _class)
    dt = datetime.strptime(_date, _format)
    return int((time.mktime(dt.timetuple()) + (dt.microsecond / _class)) * _class)


def strftime(timestamp=None, _format='%Y-%m-%d %H:%M:%S', _class=TimeClass.SECOND.value) -> str:
    """
    时间戳转日期，默认返回当前日期
    :param timestamp: 时间戳
    :param _format: 日期格式
    :param _class: 时间戳精度等级，秒/毫秒/微妙，s/ms/μs
    :return: 日期字符串
    """
    if timestamp is None:
        timestamp = time.time()
    return datetime.fromtimestamp(timestamp / _class).strftime(_format)


def randint(a: int, b: int) -> int:
    """
    返回随机整数，范围：[a,b]
    :param a: 最小值
    :param b: 最大值
    :return:
    """
    return random.randint(a, b)


def jpath(a, path: str) -> list | bool:
    return jsonpath.jsonpath(a, path)


def content_chinese_char(s):
    """
    判断字符串是否包含中文
    :param s:
    :return:
    """
    if s is None:
        return False
    return bool(re.compile(u'[\u4e00-\u9fa5]').search(s))


def _compare(x, mode="in", reverse=False, **kwargs):
    for k, v in kwargs.items():
        if mode == "in":
            return (x[k] not in v) if reverse else (x[k] in v)
        elif mode == "contains":
            return (v not in x[k]) if reverse else (v in x[k])
        elif mode == "equal":
            return (x[k] != v) if reverse else (x[k] == v)
        else:
            raise Exception("不支持的比较模式")


def sifer(li: list, mode="in", reverse=False, **kwargs):
    """
    从list[dict]中筛选满足条件的元素，输入值是右值，被筛选的数据是左值
    :param li: 要筛选的数据
    :param mode: 模式
    :param reverse: 是否反转筛选模式，False不反转，例如mode=in时，如果reverse=True，那么mode的实际效果是not in
    :param kwargs: 键值对，筛选数据中的key=输入值
    :return:
    """
    return list(filter(lambda x: _compare(x=x, mode=mode, reverse=reverse, **kwargs), li))


def count_cn_char(char) -> int:
    """
    计算字符串中，中文的个数
    :param char: 字符串
    :return:
    """
    count = 0
    for item in char:
        if 0x4E00 <= ord(item) <= 0x9FA5:
            count += 1
    return count
