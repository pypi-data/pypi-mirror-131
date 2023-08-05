import unittest
import pandas as pd
from rarefaction.rarefaction import  add
import pytest


class TestRarefaction(object):

    @pytest.mark.parametrize('name', ["LILI", "Tank", "Zhangsan"])
    def test_sum(self,name):
        self.name = name
        assert(add(2, 3) == 5)
        assert(name != "Tom")


if __name__ == '__main__':
    unittest.main()