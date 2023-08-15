import unittest
from unittest import TestCase

from idiom.KXueBus import get_all_idiom_by_head, get_all_idiom_by_word_count, get_all_idiom_by_shang_xia_ju
from idiom.impl.KxueImpl import KXueImpl
from myUtil import tips


class TestKXueBus(TestCase):
    """接口测试"""
    _kx = KXueImpl()

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    @tips("正常场景")
    def test_get_all_idiom_by_head_true(self):
        """查找指定拼音开头的全部成语，和对应的成语解释，正确的拼音：tie"""
        result = get_all_idiom_by_head(obj=self._kx, pying="tie")
        self.assertNotEqual(result, [])
        self.assertTrue(type(result) == list)

    @tips("异常场景")
    def test_get_all_idiom_by_head_false(self):
        """查找指定拼音开头的全部成语，和对应的成语解释，错误的拼音：tttsdds"""
        result = get_all_idiom_by_head(obj=self._kx, pying="tttsdds")
        self.assertEqual(result, [])
        self.assertTrue(type(result) == list)

    @tips("异常场景")
    def test_get_all_idiom_by_word_count_false(self):
        """按成语的字数查出全部符合条件的成语，错误的字数：0"""
        result = get_all_idiom_by_word_count(obj=self._kx, word_count=0)
        self.assertEqual(result, [])
        self.assertTrue(type(result) == list)

    @tips("正常场景")
    def test_get_all_idiom_by_word_count_true(self):
        """按成语的字数查出全部符合条件的成语，正确的字数：5"""
        result = get_all_idiom_by_word_count(obj=self._kx, word_count=5)
        self.assertNotEqual(result, [])
        self.assertTrue(type(result) == list)

    @tips("正常场景")
    def test_get_all_idiom_by_shang_xia_ju_true(self):
        """获取所有有上下句的成语"""
        result = get_all_idiom_by_shang_xia_ju(self._kx)
        self.assertNotEqual(result, [])
        self.assertTrue(type(result) == list)


if __name__ == "__main__":
    unittest.main()
