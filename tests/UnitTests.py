from __future__ import absolute_import
from pymer.session import session
import unittest


class sessionTests(unittest.TestCase):
    def setUp(self):
        self.testSesh = session()

    def test_truth(self):
        retName = self.testSesh.giveName()
        assert retName=="Potato"