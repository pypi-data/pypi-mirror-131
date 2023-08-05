from unittest import TestCase
from unittest.case import expectedFailure
from gerrit_coverage.condense import condense

class TestMissingLinesToComments(TestCase):
    
    def test_empty_list(self):
        self.assertEqual([], condense([]))

    def test_single_line(self):
        lines = [('file', 1)]
        self.assertEqual([('file', (1,1))], condense(lines))

    def test_two_seperated_lines(self):
        lines = [
            ('file', 9),
            ('file', 1),
        ]
        expected = [
            ('file', (1,1)),
            ('file', (9,9)),
        ]
        self.assertEqual(expected, condense(lines))

    def test_multiple_following_lines(self):
        lines = [
            ('file', 3),
            ('file', 2),
            ('file', 4),
        ]
        expected = [
            ('file', (2,4)),
        ]
        self.assertEqual(expected, condense(lines))

    def test_one_line_one_group(self):
        lines = [
            ('file', 3),
            ('file', 5),
            ('file', 4),
            ('file', 1)
        ]
        expected = [
            ('file', (1,1)),
            ('file', (3,5)),
        ]
        self.assertEqual(expected, condense(lines))

    def test_multiple_groups(self):
        lines = [
            ('file', 8),
            ('file', 9),
            ('file', 2),
            ('file', 1)
        ]
        expected = [
            ('file', (1,2)),
            ('file', (8,9)),
        ]
        self.assertEqual(expected, condense(lines))

    def test_multiple_files(self):
        lines = [
            ('file1', 2),
            ('file2', 4),
            ('file2', 3),
            ('file1', 1)
        ]
        expected = [
            ('file1', (1,2)),
            ('file2', (3,4)),
        ]
        self.assertEqual(expected, condense(lines))
