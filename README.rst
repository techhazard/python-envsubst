python-envsubst
===============

Substitute environment variables in a string::

    >>> import os
    >>> from envsubst import envsubst
    
    >>> del os.environ['PS1']
    >>> print(envsubst('$USER@$HOST ${PS1:-$}:'))
    ashafer01@github.com $:
    
    >>> os.environ['PS1'] = ''
    >>> print(envsubst('$USER@$HOST ${PS1:-$}:'))
    ashafer01@github.com $:
    
    >>> print(envsubst('$USER@$HOST ${PS1-foo}:'))
    ashafer01@github.com :

    >>> os.environ['DEFAULT_PROMPT'] = '$'
    >>> print(envsubst('$USER@$HOST ${PS1:-$DEFAULT_PROMPT}:'))

Also supports $0, $1, etc. from argv.



Variable whitelist
------------------


python-envsubst also supports replacing only a listed subset of the environment variables::

    >>> import os
    >>> from envsubst import envsubst

    >>> os.environ['FOO'] = 'this is foo'
    >>> os.environ['BAR'] = 'this is bar'
    >>> print(envsubst('$FOO != $BAR'))
    this is foo != this is bar

    >>> print(envsubst('$FOO != $BAR', ['BAR']))
    $FOO != this is bar

    >>> print(envsubst('$FOO != $BAR', ['FOO']))
    this is foo != $BAR

    >>> print(envsubst('$FOO != $BAR', ['FOO', 'BAR']))
    this is foo != this is bar

    >>> os.environ['MY_NAME'] = 'ashafer01'
    >>> os.environ['DEFAULT_NAME'] = 'stranger'
    >>> print(envsubst('hello, ${MY_NAME:-$DEFAULT_NAME}!', ['DEFAULT_NAME']))
    hello, ${MY_NAME:-stranger}!

    >>> print(envsubst('hello, ${MY_NAME:-$DEFAULT_NAME}!', ['DEFAULT_NAME', 'MY_NAME']))
    hello, ashafer01!

    >>> del os.environ['MY_NAME']
    >>> print(envsubst('greetings, ${MY_NAME:-$DEFAULT_NAME}!', ['MY_NAME']))
    greetings, $DEFAULT_NAME!

if the list is not passed or ``None``, all values are replaced, with an empty list, no values are replaced.
