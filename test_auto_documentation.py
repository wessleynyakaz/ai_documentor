import unittest
from unittest.mock import patch
from auto_documentation import parse_code, generate_comments


class TestAutoDocumentation(unittest.TestCase):

    def test_parse_code(self):
        code = """
        def add(a, b):
            return a + b
        """
        expected_info = {'add': {'parameters': ['a', 'b']}}
        self.assertEqual(parse_code(code), expected_info)

    @patch('auto_documentation.openai.Completion.create')
    def test_generate_comments(self, mock_openai_completion):
        code_snippet = "def add(a, b):\n    return a + b\n"
        expected_comments = "This function adds two numbers."
        mock_openai_completion.return_value.choices[0].text = expected_comments
        self.assertEqual(generate_comments(code_snippet), expected_comments)


if __name__ == '__main__':
    unittest.main()
