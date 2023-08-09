from abc import ABC, abstractmethod


class IdiomInterface(ABC):

    @abstractmethod
    def _get(self, url=None, params=None, data=None, headers=None, cookies=None):
        pass

    @abstractmethod
    def _post(self, url=None, data=None, json=None, params=None, headers=None, cookies=None):
        pass

    @abstractmethod
    def login(self, url=None, headers=None):
        pass

    @abstractmethod
    def pinyin(self, py=None, headers=None, cookies=None):
        pass
