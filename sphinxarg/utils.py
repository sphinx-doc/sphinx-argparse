def command_pos_args(result: dict) -> str:
    """Returns the command up to the positional arg a string
    that is suitable for the text in the command index.

    >>> x, y, z = {}, {}, {}
    >>> x['prog']='simple-command'
    >>> command_pos_args(x)
    'simple-command'

    >>> y['name']='A'
    >>> y['parent']=x
    >>> command_pos_args(y)
    'simple-command A'

    >>> z['name']='zz'
    >>> z['parent']=y
    >>> command_pos_args(z)
    'simple-command A zz'

    >>> command_pos_args("blah")
    ''
    """
    ret = ''

    if 'name' in result and result['name'] != '':
        ret += f"{result['name']}"
    elif 'prog' in result and result['prog'] != '':
        ret += f"{result['prog']}"

    if 'parent' in result:
        ret = command_pos_args(result['parent']) + ' ' + ret

    return ret


def target_to_anchor_id(target: str) -> str:
    """Returns the a string with the spaces replaced
    with dashes so the string can be found in the
    command xref targets.

    >>> cmd='simple-command A'
    >>> target_to_anchor_id(cmd)
    'simple-command-A'
    """
    if len(target) < 1:
        msg = 'Supplied target string is less than one character long.'
        raise ValueError(msg)

    return target.replace(' ', '-')


if __name__ == '__main__':
    import doctest

    doctest.testmod()
