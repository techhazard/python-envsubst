import os
import sys
import unittest
from envsubst import envsubst


class TestEnvsubst(unittest.TestCase):
    def test_simple(self):
        test_val = 'test_val_1'
        os.environ['FOO'] = test_val
        test_fmt = 'foo {0} bar'
        expected = test_fmt.format(test_val)
        test_str = test_fmt.format('$FOO')
        actual = envsubst(test_str)
        self.assertEqual(actual, expected)

    def test_bracketed_simple(self):
        test_val = 'test_val_1'
        os.environ['FOO'] = test_val
        test_fmt = 'foo {0} bar'
        expected = test_fmt.format(test_val)
        test_str = test_fmt.format('${FOO}')
        actual = envsubst(test_str)
        self.assertEqual(actual, expected)

    def test_unset_default(self):
        try:
            del os.environ['FOO']
        except KeyError:
            pass

        test_fmt = 'abc {0} def'
        default_str = 'i am a default'
        test_var = '${FOO-' + default_str + '}'
        test_str = test_fmt.format(test_var)
        expected = test_fmt.format(default_str)
        actual = envsubst(test_str)
        self.assertEqual(actual, expected)

    def test_unset_only_no_default(self):
        test_val = ''
        os.environ['FOO'] = test_val

        test_fmt = 'abc {0} def'
        default_str = 'i am a default'
        test_var = '${FOO-' + default_str + '}'
        test_str = test_fmt.format(test_var)
        expected = test_fmt.format(test_val)
        actual = envsubst(test_str)
        self.assertEqual(actual, expected)

    def test_no_default_with_unset_only_operator(self):
        test_val = 'i am definitely a value'
        os.environ['FOO'] = test_val

        test_fmt = 'abc {0} def'
        test_var = '${FOO-i am a default}'
        test_str = test_fmt.format(test_var)
        expected = test_fmt.format(test_val)
        actual = envsubst(test_str)
        self.assertEqual(actual, expected)

    def test_empty_unset_or_empty_default(self):
        test_val = ''
        os.environ['FOO'] = test_val

        test_fmt = 'abc {0} def'
        default_str = 'i am a default'
        test_var = '${FOO:-' + default_str + '}'
        test_str = test_fmt.format(test_var)
        expected = test_fmt.format(default_str)
        actual = envsubst(test_str)
        self.assertEqual(actual, expected)

    def test_unset_unset_or_empty_default(self):
        try:
            del os.environ['FOO']
        except KeyError:
            pass

        test_fmt = 'abc {0} def'
        default_str = 'i am a default'
        test_var = '${FOO:-' + default_str + '}'
        test_str = test_fmt.format(test_var)
        expected = test_fmt.format(default_str)
        actual = envsubst(test_str)
        self.assertEqual(actual, expected)

    def test_no_default_with_emtpy_operator(self):
        test_val = 'i am a real live value'
        os.environ['FOO'] = test_val

        test_fmt = 'abc {0} def'
        test_var = '${FOO:-i am a default}'
        test_str = test_fmt.format(test_var)
        expected = test_fmt.format(test_val)
        actual = envsubst(test_str)
        self.assertEqual(actual, expected)

    def test_multiple(self):
        foo_val = 'i am FOO value'
        os.environ['FOO'] = foo_val
        bar_val = 'i am BAR value'
        os.environ['BAR'] = bar_val
        bar2_val = 'i am BAR2 value'
        os.environ['BAR2'] = bar2_val

        try:
            del os.environ['NOPE']
        except KeyError:
            pass

        nope_default = 'var NOPE not there'

        test_fmt = 'abc {0} def {1}{2} jkl {3} mno'
        test_str = test_fmt.format(
            '$FOO',
            '${BAR}',
            '${BAR2:-default for bar2}',
            '${NOPE-' + nope_default + '}',
        )
        expected = test_fmt.format(
            foo_val,
            bar_val,
            bar2_val,
            nope_default
        )
        actual = envsubst(test_str)
        self.assertEqual(actual, expected)

    def test_escaped(self):
        tests = [
            r'i am an \$ESCAPED variable',
            r'i am an \${ESCAPED:-bracketed} \${expression}',
        ]
        for test in tests:
            self.assertEqual(test, envsubst(test))

    def test_escaped_not_in_witelist(self):
        tests = [
            r'i am an \$ESCAPED variable',
            r'i am an \${ESCAPED:-bracketed} \${expression}',
        ]
        for test in tests:
            self.assertEqual(test, envsubst(test, ['OTHER_VAR']))

    def test_escaped_in_witelist(self):
        tests = [
            r'i am an \$ESCAPED variable',
            r'i am an \${ESCAPED:-bracketed} \${expression}',
        ]
        for test in tests:
            self.assertEqual(test, envsubst(test, ['ESCAPED', 'expression']))

    def test_simple_var_default_in_whitelist(self):
        default_val = 'test default val'
        os.environ['DEFAULT'] = default_val
        os.environ['TEST'] = ''

        test_fmt = 'abc {0} def'
        test_str = test_fmt.format('${TEST:-$DEFAULT}')
        expected = test_fmt.format('${TEST:-' + default_val + '}')
        actual = envsubst(test_str, ['DEFAULT'])
        self.assertEqual(actual, expected)

    def test_simple_var_default_both_in_whitelist(self):
        default_val = 'test default val'
        os.environ['DEFAULT'] = default_val
        os.environ['TEST'] = ''

        test_fmt = 'abc {0} def'
        test_str = test_fmt.format('${TEST:-$DEFAULT}')
        expected = test_fmt.format(default_val)
        actual = envsubst(test_str, ['DEFAULT', 'TEST'])
        self.assertEqual(actual, expected)

    def test_simple_var_test_both_in_whitelist(self):
        default_val = 'test default val'
        os.environ['DEFAULT'] = default_val
        os.environ['TEST'] = ''

        test_fmt = 'abc {0} def'
        test_str = test_fmt.format('${TEST:-$DEFAULT}')
        expected = test_fmt.format('$DEFAULT')
        actual = envsubst(test_str, ['TEST'])
        self.assertEqual(actual, expected)


    def test_simple_var_default(self):
        default_val = 'test default val'
        os.environ['DEFAULT'] = default_val
        os.environ['TEST'] = ''

        test_fmt = 'abc {0} def'
        test_str = test_fmt.format('${TEST:-$DEFAULT}')
        expected = test_fmt.format(default_val)
        actual = envsubst(test_str)
        self.assertEqual(actual, expected)

    def test_argv(self):
        test_val = 'test argv value'
        try:
            sys.argv[1] = test_val
        except IndexError:
            sys.argv.append(test_val)

        test_fmt = 'abc {0} def'
        test_str = test_fmt.format('$1')
        expected = test_fmt.format(test_val)
        actual = envsubst(test_str)
        self.assertEqual(actual, expected)
