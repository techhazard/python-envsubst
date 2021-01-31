"""
Substitute environment variables in a string.

For more info:
>>> from envsubst import envsubst
>>> help(envsubst)
"""
# MIT License
# 
# Copyright (c) 2019 Alex Shafer
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import os
import sys


_simple_re = re.compile(r'(?<!\\)\$([A-Za-z0-9_]+)')
_extended_re = re.compile(r'(?<!\\)\$\{([A-Za-z0-9_]+)((:?-)([^}]+))?\}')


def _resolve_var(var_name, default=None):
    try:
        index = int(var_name)
        try:
            return sys.argv[index]
        except IndexError:
            return default
    except ValueError:
        return os.environ.get(var_name, default)


def _repl_simple_env_var(env_var_list):
    def inner(regex_match):
        var_name = regex_match.group(1)
        if env_var_list is None or var_name in env_var_list:
            return _resolve_var(var_name, '')
        else:
            return regex_match.group(0)
    return inner


def _repl_extended_env_var(env_var_list):
    def inner(regex_match):
        var_name = regex_match.group(1)
        if env_var_list is not None and var_name not in env_var_list:
            return regex_match.group(0)
        default_spec = regex_match.group(2)
        if default_spec:
            default = regex_match.group(4)
            default = _simple_re.sub(_repl_simple_env_var(env_var_list), default)
            if regex_match.group(3) == ':-':
                # use default if var is unset or empty
                env_var = _resolve_var(var_name)
                if env_var:
                    return env_var
                else:
                    return default
            elif regex_match.group(3) == '-':
                # use default if var is unset
                return _resolve_var(var_name, default)
            else:
                raise RuntimeError('unexpected string matched regex')
        else:
            return _resolve_var(var_name, '')
    return inner


def envsubst(string, env_var_list=None):
    """
    Substitute environment variables in the given string

    The following forms are supported:

    Simple variables - will use an empty string if the variable is unset
      $FOO

    Bracketed expressions
      ${FOO}
        identical to $FOO
      ${FOO:-somestring}
        uses "somestring" if $FOO is unset, or set and empty
      ${FOO-somestring}
        uses "somestring" only if $FOO is unset

    :param str string: A string possibly containing environment variables
    :param list[str] env_var_list: An optional list of strings containing names of environment variables to replace.
                                   If not given, all variables will be replaced
    :return: The string with environment variable specs replaced with their values
    """
    if not isinstance(env_var_list, list):
        if isinstance(env_var_list, str):
            env_var_list = [env_var_list]
        else:
            env_var_list = None

    # handle simple un-bracketed env vars like $FOO
    a = _simple_re.sub(_repl_simple_env_var(env_var_list), string)

    # handle bracketed env vars with optional default specification
    b = _extended_re.sub(_repl_extended_env_var(env_var_list), a)
    return b


def main():
    opened = False

    input_file = sys.stdin
    output_file = sys.stdout

    try:
        try:
            filename = sys.argv[1]
            if filename != '-':
                input_file = open(filename)
                opened = True
        except IndexError:
            pass

        data = input_file.read()
        try:
            data = data.decode('utf-8')
        except AttributeError:
            pass

        output_file.write(envsubst(data))
    finally:
        if opened:
            input_file.close()


if __name__ == '__main__':
    main()
