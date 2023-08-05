"""
Tests translator module.
"""
from os import path
import unittest
import verbcalc


class TestTranslator(unittest.TestCase):
    """
    Tests how translator works.
    """

    def setUp(self):
        self.expected = ['2 + 2', '2 - 2', '2 * 2', '2 / 2', '2 ** 2',
                         'abs 2', '2 % 2']
        self.path = path.join(path.dirname(__file__),
                              'fixtures/custom_phrasings.json')

    def test_translation(self):
        values = [verbcalc.translate('2 plus 2'),
                  verbcalc.translate('2 minus 2'),
                  verbcalc.translate('2 times 2'),
                  verbcalc.translate('2 divided by 2'),
                  verbcalc.translate('2 to the power of 2'),
                  verbcalc.translate('absolute of 2'),
                  verbcalc.translate('2 mod 2')]
        self.assertListEqual(self.expected, values)

    def test_translation_with_custom_phrasings(self):
        custom_symbols = verbcalc.Symbols(path_to_phrasings=self.path)
        self.assertEqual('2 + 2', verbcalc.translate(
            '2 foo 2', custom_symbols))


if __name__ == '__main__':
    unittest.main()
