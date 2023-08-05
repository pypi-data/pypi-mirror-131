"""
    Tests how custom answers work.
"""
from os import path
import unittest
import verbcalc


class TestCustomAnswers(unittest.TestCase):
    """
    Tests how custom answers work.
    """

    def setUp(self):
        self.expected_default = ['It is', 'The answer is', 'The result is',
                                 'The total is', 'Altogether you get']
        self.expected_custom = ['Foo', 'Bar']
        self.path = path.join(path.dirname(__file__),
                              'fixtures/custom_answers.json')

    def test_random_phrase(self):
        result = verbcalc.calculate('What is 2 plus 2')
        check = [i for i in self.expected_default if i in result]
        self.assertTrue(check)

    def test_custom_random_phrase(self):
        result = verbcalc.calculate(
            'What is 2 plus 2', path_to_answers=self.path)
        check = [i for i in self.expected_custom if i in result]
        self.assertTrue(check)


if __name__ == '__main__':
    unittest.main()
