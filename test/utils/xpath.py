import re


def check_xpath(etree, fname, path, check, be_found=True):
    nodes = list(etree.xpath(path))
    if check is None:
        assert nodes == [], f'found any nodes matching xpath {path!r} in file {fname}'
        return
    else:
        assert nodes != [], f'did not find any node matching xpath {path!r} in file {fname}'
    if callable(check):
        check(nodes)
    elif not check:
        # only check for node presence
        pass
    else:

        def get_text(node):
            if node.text is not None:
                # the node has only one text
                return node.text
            else:
                # the node has tags and text; gather texts just under the node
                return ''.join(n.tail or '' for n in node)

        rex = re.compile(check)
        if be_found:
            if any(rex.search(get_text(node)) for node in nodes):
                return
            msg = (
                f'{check!r} not found in any node matching path {path} in {fname}: '
                f'{[node.text for node in nodes]!r}'
            )
        else:
            if all(not rex.search(get_text(node)) for node in nodes):
                return
            msg = (
                f'Found {check!r} in a node matching path {path} in {fname}: '
                f'{[node.text for node in nodes]!r}'
            )

        raise AssertionError(msg)
