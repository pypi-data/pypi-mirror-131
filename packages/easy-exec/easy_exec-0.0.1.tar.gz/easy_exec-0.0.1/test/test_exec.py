from unittest import TestCase
from easy_exec import exec

class TestExec(TestCase):
    
    def test_stdout(self):
        stdout, stderr, has_error = exec('echo "hello world"')
        self.assertEqual('hello world\n', stdout)
        self.assertEqual('', stderr)
        self.assertFalse(has_error)
    
    def test_stderr(self):
        stdout, stderr, has_error = exec('logger -s error')
        self.assertEqual('', stdout)
        self.assertIn('error', stderr)
        self.assertFalse(has_error)

    def test_has_error(self):
        stdout, stderr, has_error = exec('python3 -m asdfljasldkjfaöldkf')
        self.assertEqual('', stdout)
        self.assertTrue(has_error)
        