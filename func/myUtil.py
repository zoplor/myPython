import json
import random
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
    :param js:
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


def to_json(s, _type="string", cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None,
            object_pairs_hook=None, **kw) -> Any:
    """
    字符串或者文件转python数据类型
    :param s:
    :param _type:
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
        return json.load(s, cls=cls, object_hook=object_hook, parse_float=parse_float, parse_int=parse_int,
                         parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)
    else:
        raise Exception("Invalid type!")


def to_string(obj, fp=None, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None,
              separators=None, default=None, sort_keys=False, **kw) -> str | None:
    """
    把python类型转字符串，或者转换后并写入文件
    :param obj:
    :param fp:
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
        return json.dump(obj, fp, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                         allow_nan=allow_nan, cls=cls, indent=indent, separators=separators, default=default,
                         sort_keys=sort_keys, **kw)


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


