from search_indexer import preprocess_text, create_index, are_similar, score, search, display_results
import doctest
import io
import unittest
from unittest.mock import patch


class Test(unittest.TestCase):
    def test_preprocess_text(self):
        with patch("sys.stdout", io.StringIO()) as report:
            doctest.run_docstring_examples(preprocess_text, globals())
            self.maxDiff = 1000
            self.assertEqual(report.getvalue(), "")

    def test_create_index(self):
        with patch("sys.stdout", io.StringIO()) as report:
            doctest.run_docstring_examples(create_index, globals())
            self.maxDiff = 1000
            self.assertEqual(report.getvalue(), "")

    def test_are_similar(self):
        with patch("sys.stdout", io.StringIO()) as report:
            doctest.run_docstring_examples(are_similar, globals())
            self.maxDiff = 1000
            self.assertEqual(report.getvalue(), "")

    def test_score(self):
        with patch("sys.stdout", io.StringIO()) as report:
            doctest.run_docstring_examples(score, globals())
            self.maxDiff = 1000
            self.assertEqual(report.getvalue(), "")

    def test_search(self):
        with patch("sys.stdout", io.StringIO()) as report:
            doctest.run_docstring_examples(search, globals())
            self.maxDiff = 1000
            self.assertEqual(report.getvalue(), "")

    def test_display_results(self):
        with patch("sys.stdout", io.StringIO()) as report:
            doctest.run_docstring_examples(display_results, globals())
            self.maxDiff = 1000
            self.assertEqual(report.getvalue(), "")
