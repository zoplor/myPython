import unittest
from unittest import TestCase

from myUtil import tips, header_str_to_dict, special_str_to_json, print_blank_line, json_to_special_str, strptime, strftime, \
    randint, range_list, jpath, content_chinese_char, sifer, count_cn_char, is_cn_char


class TestMyUtil(TestCase):

    @classmethod
    @print_blank_line
    @tips("测试场景", "测试结果")
    def setUpClass(cls) -> None:
        """测试用例"""
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    @tips("正常场景")
    def test_header_str_to_dict_true(self):
        """把str转成header，正常参数"""
        test_data = [
            'Accept:',
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding:', 'gzip, deflate', 'Accept-Language:', 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control:', 'no-cache', 'Cookie:',
            'Hm_lvt_a852cf951acb5ab555bcf768173f1bfc=1691221592; Hm_lpvt_a852cf951acb5ab555bcf768173f1bfc=1692105621; __gads=ID=3861192f528ed0b4-229d4728bae7009e:T=1691221592:RT=1692105616:S=ALNI_MbrBRs2gEWMCgKEOI-p6g9eYOXZ7w; __gpi=UID=00000c2740754a6e:T=1691221592:RT=1692105616:S=ALNI_MbRMoA5I9N1oTUbKkDZ-IDRFYsZdg; FCNEC=%5B%5B%22AKsRol9OQNojGb6w_B-84IzMuDsEZlt2veiDxPELKI84pScrHbkU1GC_a1zMWwm9Tak5KXq1VIsYTaCFwfED2daHNadH0uh1uNVhbW2Wf6kfDOvHKMGJja_JRDrEqzOpN0vaFNRbgzjLnsKnGg1F4CaB4Er2xqQ9fg%3D%3D%22%5D%2Cnull%2C%5B%5D%5D',
            'Host:', 'chengyu.kxue.com', 'Pragma:', 'no-cache', 'Proxy-Connection:', 'keep-alive', 'Referer:',
            'http://chengyu.kxue.com/pinyin/tie.html', 'Upgrade-Insecure-Requests:', '1', 'User-Agent:',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203']
        expected = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Cookie': 'Hm_lvt_a852cf951acb5ab555bcf768173f1bfc=1691221592; Hm_lpvt_a852cf951acb5ab555bcf768173f1bfc=1692105621; __gads=ID=3861192f528ed0b4-229d4728bae7009e:T=1691221592:RT=1692105616:S=ALNI_MbrBRs2gEWMCgKEOI-p6g9eYOXZ7w; __gpi=UID=00000c2740754a6e:T=1691221592:RT=1692105616:S=ALNI_MbRMoA5I9N1oTUbKkDZ-IDRFYsZdg; FCNEC=%5B%5B%22AKsRol9OQNojGb6w_B-84IzMuDsEZlt2veiDxPELKI84pScrHbkU1GC_a1zMWwm9Tak5KXq1VIsYTaCFwfED2daHNadH0uh1uNVhbW2Wf6kfDOvHKMGJja_JRDrEqzOpN0vaFNRbgzjLnsKnGg1F4CaB4Er2xqQ9fg%3D%3D%22%5D%2Cnull%2C%5B%5D%5D',
            'Host': 'chengyu.kxue.com', 'Pragma': 'no-cache', 'Proxy-Connection': 'keep-alive',
            'Referer': 'http://chengyu.kxue.com/pinyin/tie.html', 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203'}
        result = header_str_to_dict(test_data)
        self.assertEqual(expected, result)

    @tips("异常场景")
    def test_header_str_to_dict_false_singular(self):
        """把str转成header，异常参数：list的元素个数是单数"""
        test_data = ["eee:", "ffss", "rrrr:"]
        with self.assertRaisesRegex(Exception, "Wrong number of list elements!"):
            header_str_to_dict(test_data)

    @tips("异常场景")
    def test_header_str_to_dict_false_zero(self):
        """把str转成header，异常参数：list的元素个数是0"""
        test_data = []
        result = header_str_to_dict(test_data)
        self.assertEqual({}, result)

    @tips("正常场景")
    def test_special_str_to_json_true(self):
        """把kxue.com网的cookies转成dict"""
        test_data = "Hm_lvt_a852cf951acb5ab555bcf768173f1bfc=1691221592; Hm_lpvt_a852cf951acb5ab555bcf768173f1bfc=1692110534; " \
                    "__gads=ID=3861192f528ed0b4-229d4728bae7009e:T=1691221592:RT=1692110529:S=ALNI_MbrBRs2gEWMCgKEOI" \
                    "-p6g9eYOXZ7w; __gpi=UID=00000c2740754a6e:T=1691221592:RT=1692110529:S=ALNI_MbRMoA5I9N1oTUbKkDZ-IDRFYsZdg; " \
                    "FCNEC=%5B%5B%22AKsRol-WRjd4qU28L6z_M2mIhuoiKmpj2Br0C09ZxFeoITXRm8nfIo--UU2" \
                    "-3E15JFXRBt6T1yPzvM6qqYeXkvtx1W_8l9-bclDb-qJt5al47TNKAqQxpJ_jCqFknNsMiBWSpZVm0420LQr3-WTtJH4EJ-kWTRrX3w%3D" \
                    "%3D%22%5D%2Cnull%2C%5B%5D%5D"
        expected = {'Hm_lvt_a852cf951acb5ab555bcf768173f1bfc': '1691221592; Hm_lpvt_a852cf951acb5ab555bcf768173f1bfc',
                    'T': '1691221592', 'RT': '1692110529', 'S': 'ALNI_MbRMoA5I9N1oTUbKkDZ-IDRFYsZdg; FCNEC'}
        result = special_str_to_json(test_data)
        self.assertEqual(expected, result)

    @tips("正常场景")
    def test_json_to_special_str_true(self):
        """把dict转成cookies中的某一段字符"""
        expected = "UID=00000c2edf9c7269:T=1692370517:RT=1692370517:S=ALNI_MZgK_7MIHwIxVML8o3n5UQOFISCyg"
        test_data = {'UID': '00000c2edf9c7269', 'T': '1692370517', 'RT': '1692370517', 'S': 'ALNI_MZgK_7MIHwIxVML8o3n5UQOFISCyg'}
        result = json_to_special_str(test_data)
        self.assertEqual(expected, result)

    @tips("正常场景")
    def test_strptime_true(self):
        """日期字符串转时间戳"""
        test_data = "2023-08-19 18:25:30"
        result = strptime(_date=test_data, _format="%Y-%m-%d %H:%M:%S")
        expected = strftime(timestamp=result, _format="%Y-%m-%d %H:%M:%S")
        self.assertEqual(expected, test_data)

    @tips("正常场景")
    def test_strftime_true_second(self):
        """秒级时间戳转日期字符串"""
        test_data = 1692440730
        result = strftime(timestamp=test_data, _format="%Y-%m-%d %H:%M:%S")
        expected = strptime(_date=result, _format="%Y-%m-%d %H:%M:%S")
        self.assertEqual(expected, test_data)

    @tips("正常场景")
    def test_strftime_true_milli_second(self):
        """毫秒级时间戳转日期字符串"""
        test_data = 1692440730345
        result = strftime(timestamp=test_data, _format="%Y-%m-%d %H:%M:%S.%f", _class=1000.0)
        expected = strptime(_date=result, _format="%Y-%m-%d %H:%M:%S.%f", _class=1000.0)
        self.assertEqual(expected, test_data)

    @tips("正常场景")
    def test_strftime_true_micro_second(self):
        """微秒级时间戳转日期字符串"""
        test_data = 1692440730345789
        result = strftime(test_data, _format="%Y-%m-%d %H:%M:%S.%f", _class=1000000.0)
        expected = strptime(result, _format="%Y-%m-%d %H:%M:%S.%f", _class=1000000.0)
        self.assertEqual(expected, test_data)

    @tips("正常场景")
    def test_randint_true(self):
        """返回随机整数，范围：[a,b]"""
        a = 10
        b = 20
        result = randint(a, b)
        self.assertIn(result, range_list(a, b))

    @tips("正常场景")
    def test_jpath_true(self):
        """通过jsonpath从json中取值"""
        test_data = {"eee": [{"ttt": "qqq"}]}
        expected = ["qqq"]
        result = jpath(test_data, '$.eee[0].ttt')
        self.assertEqual(expected, result)

    @tips("正常场景")
    def test_content_chinese_char_true(self):
        """判断字符串是否包含中文，测试字符串中存在中文"""
        td = "好着呢个；hfjkjd"
        res = content_chinese_char(td)
        self.assertEqual(True, res)

    @tips("异常场景")
    def test_content_chinese_char_false(self):
        """判断字符串是否包含中文，测试字符串中不存在中文"""
        td = "9073890；‘；。'.；hfjkjd"
        res = content_chinese_char(td)
        self.assertEqual(False, res)

    @tips("正常场景")
    def test_sifer_true_in_str(self):
        """测试筛子，模式：in，输入值类型是str"""
        td = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"},
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        expected = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"}
        ]
        res = sifer(td, "in", False, idiom="打抱不平")
        self.assertEqual(expected, res)

    @tips("正常场景")
    def test_sifer_true_in_str_reverse(self):
        """测试筛子，模式：not in，输入值类型是str"""
        td = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"},
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        expected = [
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        res = sifer(td, "in", True, idiom="打抱不平")
        self.assertEqual(expected, res)

    @tips("正常场景")
    def test_sifer_true_in_list(self):
        """测试筛子，模式：in，输入值类型是list"""
        td = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"},
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        expected = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"},
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"}
        ]
        res = sifer(td, "in", False, idiom=["抱不平", "百世师"])
        self.assertEqual(expected, res)

    @tips("正常场景")
    def test_sifer_true_in_list_reverse(self):
        """测试筛子，模式：not in，输入值类型是list"""
        td = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"},
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        expected = [
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        res = sifer(td, "in", True, idiom=["抱不平", "百世师"])
        self.assertEqual(expected, res)

    @tips("正常场景")
    def test_sifer_true_contains(self):
        """测试筛子，模式：contains，输入值类型是str"""
        td = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"},
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        expected = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"}
        ]
        res = sifer(td, "contains", False, idiom="不")
        self.assertEqual(expected, res)

    @tips("正常场景")
    def test_sifer_true_contains_reverse(self):
        """测试筛子，模式：not contains，输入值类型是str"""
        td = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"},
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        expected = [
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        res = sifer(td, "contains", True, idiom="不")
        self.assertEqual(expected, res)

    @tips("正常场景")
    def test_sifer_true_equal(self):
        """测试筛子，模式：equal，输入值类型是str"""
        td = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"},
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        expected = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"}
        ]
        res = sifer(td, "equal", False, idiom="抱不平")
        self.assertEqual(expected, res)

    @tips("正常场景")
    def test_sifer_true_equal_reverse(self):
        """测试筛子，模式：not equal，输入值类型是str"""
        td = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"},
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        expected = [
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        res = sifer(td, "equal", True, idiom="抱不平")
        self.assertEqual(expected, res)

    @tips("异常场景")
    def test_sifer_false_unsupported_mode(self):
        """测试筛子，模式：不支持的模式"""
        td = [
            {"idiom": "抱不平", "paraphrase": "遇见不公平的事，挺身而出，帮助弱小的一方。…"},
            {"idiom": "百世师", "paraphrase": "品德学问可以做为百代的表率。…"},
            {"idiom": "安乐窝", "paraphrase": "泛指安静舒适的住处。…"}
        ]
        with self.assertRaisesRegex(Exception, "不支持的比较模式"):
            sifer(td, "unsupported", False, idiom="抱不平")

    @tips("正常场景")
    def test_count_cn_char_true(self):
        """统计字符串中有几个中文字符，N个"""
        td = "有五个中文。、；’‘；"
        self.assertEqual(5, count_cn_char(td))

    @tips("正常场景")
    def test_count_cn_char_true_zero(self):
        """统计字符串中有几个中文字符，0个"""
        td = "has zero cn char。、；’‘；"
        self.assertEqual(0, count_cn_char(td))

    @tips("正常场景")
    def test_count_cn_char_true_zero(self):
        """统计字符串中有几个中文字符，0个"""
        td = "has zero cn char。、；’‘；"
        self.assertEqual(0, count_cn_char(td))

    @tips("正常场景")
    def test_is_cn_char_true_cn(self):
        """判断字符是否为中文字符，测试中文字符"""
        td = "中"
        res = is_cn_char(td)
        self.assertEqual(True, res)

    @tips("正常场景")
    def test_is_cn_char_true_en(self):
        """判断字符是否为中文字符，测试英文字符"""
        td = "w"
        res = is_cn_char(td)
        self.assertEqual(False, res)

    @tips("异常场景")
    def test_is_cn_char_false_length(self):
        """判断字符是否为中文字符，异常入参长度"""
        td = "我w"
        with self.assertRaisesRegex(TypeError, "expected a character, but string of length 2 found"):
            res = is_cn_char(td)

    @tips("异常场景")
    def test_range_list_false_float(self):
        """返回[a,..,b]，每一个元素都是整数，异常类型入参"""
        a = 1.0
        b = 10.0
        with self.assertRaisesRegex(TypeError, "'float' object cannot be interpreted as an integer"):
            range_list(a, b)


if __name__ == "__main__":
    unittest.main()
