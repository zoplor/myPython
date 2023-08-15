import unittest
from unittest import TestCase

from myUtil import tips, header_str_to_dict


class TestMyUtil(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
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


if __name__ == "__main__":
    unittest.main()
