import unittest
from ..utils.args_handler import create_parser


class TestModelFilePaths(unittest.TestCase):
    def test_valid_path(self):
        self.assertRaises(AssertionError, create_parser, ['-m', 'model3'])


if __name__ == "__main__":
    unittest.main()
