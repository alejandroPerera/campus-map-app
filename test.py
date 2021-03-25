import unittest


class TestMethods(unittest.TestCase):
    def test_equal(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_false(self):
        self.assertFalse("FOo".isupper())


if __name__ == '__main__':
    unittest.main()
