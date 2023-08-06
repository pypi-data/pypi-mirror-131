from __future__ import absolute_import

from nose.tools import *

from tests import testit


class TestExport(testit.LocalCase):
    def test_all(self):
        # with assert_raises(SystemExit) as r:
        #     testit.sciunit('export')
        # assert_equal(r.exception.code, 2)
        testit.sciunit('create', 'ok')
        testit.sciunit('exec', 'python', 'cwd.py')

        with assert_raises(SystemExit) as r:
            testit.sciunit('export', 'e1')
        assert_equal(r.exception.code, 2)
