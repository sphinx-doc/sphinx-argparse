from __future__ import annotations

import importlib
import os
import shutil
import sys
from argparse import ArgumentParser

from docutils import nodes
from docutils.frontend import get_default_settings
from docutils.parsers.rst import Parser
from docutils.parsers.rst.directives import flag, unchanged
from docutils.statemachine import StringList
from sphinx.ext.autodoc import mock
from sphinx.util.docutils import SphinxDirective, new_document
from sphinx.util.nodes import nested_parse_with_titles

from sphinxarg import __version__
from sphinxarg.parser import parse_parser, parser_navigate


def map_nested_definitions(nested_content):
    if nested_content is None:
        msg = 'Nested content should be iterable, not null'
        raise Exception(msg)
    # build definition dictionary
    definitions = {}
    for item in nested_content:
        if not isinstance(item, nodes.definition_list):
            continue
        for subitem in item:
            if not isinstance(subitem, nodes.definition_list_item):
                continue
            if not len(subitem.children) > 0:
                continue
            classifier = '@after'
            idx = subitem.first_child_matching_class(nodes.classifier)
            if idx is not None:
                ci = subitem[idx]
                if len(ci.children) > 0:
                    classifier = ci.children[0].astext()
            if classifier is not None and classifier not in {
                '@replace',
                '@before',
                '@after',
                '@skip',
            }:
                msg = f'Unknown classifier: {classifier}'
                raise Exception(msg)
            idx = subitem.first_child_matching_class(nodes.term)
            if idx is not None:
                term = subitem[idx]
                if len(term.children) > 0:
                    term = term.children[0].astext()
                    idx = subitem.first_child_matching_class(nodes.definition)
                    if idx is not None:
                        subcontent = [
                            _ for _ in subitem[idx] if isinstance(_, nodes.definition_list)
                        ]
                        definitions[term] = (classifier, subitem[idx], subcontent)

    return definitions


def render_list(l, markdown_help, settings=None):
    """
    Given a list of reStructuredText or MarkDown sections, return a docutils node list
    """
    if len(l) == 0:
        return []
    if markdown_help:
        from sphinxarg.markdown import parse_markdown_block

        return parse_markdown_block('\n\n'.join(l) + '\n')
    else:
        if settings is None:
            settings = get_default_settings(Parser)
        all_children = []
        for element in l:
            if isinstance(element, str):
                document = new_document('', settings)
                Parser().parse(element + '\n', document)
                all_children += document.children
            elif isinstance(element, nodes.definition):
                all_children += element

        return all_children


def _is_suppressed(item: str | None) -> bool:
    """Return whether item should not be printed."""
    if item is None:
        return True
    item = str(item).replace('"', '').replace("'", '')
    return item == '==SUPPRESS=='


def print_action_groups(
    data,
    nested_content,
    markdown_help=False,
    settings=None,
    id_prefix='',
):
    """
    Process all 'action groups', which are also include 'Options' and 'Required
    arguments'. A list of nodes is returned.
    """
    definitions = map_nested_definitions(nested_content)
    nodes_list = []
    if 'action_groups' in data:
        for action_group in data['action_groups']:
            # Every action group is composed of a section, holding
            # a title, the description, and the option group (members)
            title_as_id = action_group['title'].replace(' ', '-').lower()
            if data['name']:
                title_as_id = f'{data["name"]}-{title_as_id}'
            if id_prefix:
                title_as_id = f'{id_prefix}-{title_as_id}'
            section = nodes.section(ids=[title_as_id])
            section += nodes.title(action_group['title'], action_group['title'])

            desc = []
            if action_group['description']:
                desc.append(action_group['description'])
            # Replace/append/prepend content to the description according to nested content
            subcontent = []
            if action_group['title'] in definitions:
                classifier, s, subcontent = definitions[action_group['title']]
                if classifier == '@replace':
                    desc = [s]
                elif classifier == '@after':
                    desc.append(s)
                elif classifier == '@before':
                    desc.insert(0, s)
                elif classifier == '@skip':
                    continue
                if len(subcontent) > 0:
                    for k, v in map_nested_definitions(subcontent).items():
                        definitions[k] = v
            # Render appropriately
            for element in render_list(desc, markdown_help):
                section += element

            local_definitions = definitions
            if len(subcontent) > 0:
                local_definitions = dict(definitions.items())
                for k, v in map_nested_definitions(subcontent).items():
                    local_definitions[k] = v

            items = []
            # Iterate over action group members
            for entry in action_group['options']:
                # Members will include:
                #    default	The default value. This may be ==SUPPRESS==
                #    name	A list of option names (e.g., ['-h', '--help']
                #    help	The help message string
                # There may also be a 'choices' member.
                # Build the help text
                arg = []
                if 'choices' in entry:
                    arg.append(
                        f"Possible choices: {', '.join(str(c) for c in entry['choices'])}\n"
                    )
                if 'help' in entry:
                    arg.append(entry['help'])
                if not _is_suppressed(entry['default']):
                    # Put the default value in a literal block,
                    # but escape backticks already in the string
                    default_str = str(entry['default']).replace('`', r'\`')
                    arg.append(f'Default: ``{default_str}``')

                # Handle nested content, the term used in the dict
                # has the comma removed for simplicity
                desc = arg
                term = ' '.join(entry['name'])
                if term in local_definitions:
                    classifier, s, subcontent = local_definitions[term]
                    if classifier == '@replace':
                        desc = [s]
                    elif classifier == '@after':
                        desc.append(s)
                    elif classifier == '@before':
                        desc.insert(0, s)
                term = ', '.join(entry['name'])

                n = nodes.option_list_item(
                    '',
                    nodes.option_group('', nodes.option_string(text=term)),
                    nodes.description('', *render_list(desc, markdown_help, settings)),
                )
                items.append(n)

            section += nodes.option_list('', *items)
            nodes_list.append(section)

    return nodes_list


def print_subcommands(data, nested_content, markdown_help=False, settings=None):  # noqa: N803
    """
    Each subcommand is a dictionary with the following keys:

    ['usage', 'action_groups', 'bare_usage', 'name', 'help']

    In essence, this is all tossed in a new section with the title 'name'.
    Apparently there can also be a 'description' entry.
    """

    definitions = map_nested_definitions(nested_content)
    items = []
    if 'children' in data:
        subcommands = nodes.section(ids=['Sub-commands'])
        subcommands += nodes.title('Sub-commands', 'Sub-commands')

        for child in data['children']:
            sec = nodes.section(ids=[child['name']])
            sec += nodes.title(child['name'], child['name'])

            if 'description' in child and child['description']:
                desc = [child['description']]
            elif child['help']:
                desc = [child['help']]
            else:
                desc = ['Undocumented']

            # Handle nested content
            subcontent = []
            if child['name'] in definitions:
                classifier, s, subcontent = definitions[child['name']]
                if classifier == '@replace':
                    desc = [s]
                elif classifier == '@after':
                    desc.append(s)
                elif classifier == '@before':
                    desc.insert(0, s)

            for element in render_list(desc, markdown_help):
                sec += element
            sec += nodes.literal_block(text=child['bare_usage'])
            for x in print_action_groups(
                child, nested_content + subcontent, markdown_help, settings=settings
            ):
                sec += x

            for x in print_subcommands(
                child, nested_content + subcontent, markdown_help, settings=settings
            ):
                sec += x

            if 'epilog' in child and child['epilog']:
                for element in render_list([child['epilog']], markdown_help):
                    sec += element

            subcommands += sec
        items.append(subcommands)

    return items


def ensure_unique_ids(items):
    """
    If action groups are repeated, then links in the table of contents will
    just go to the first of the repeats. This may not be desirable, particularly
    in the case of subcommands where the option groups have different members.
    This function updates the title IDs by adding _repeatX, where X is a number
    so that the links are then unique.
    """
    s = set()
    for item in items:
        for n in item.findall(descend=True, siblings=True, ascend=False):
            if isinstance(n, nodes.section):
                ids = n['ids']
                for idx, id in enumerate(ids):
                    if id not in s:
                        s.add(id)
                    else:
                        i = 1
                        while f'{id}_repeat{i}' in s:
                            i += 1
                        ids[idx] = f'{id}_repeat{i}'
                        s.add(ids[idx])
                n['ids'] = ids


class ArgParseDirective(SphinxDirective):
    has_content = True
    option_spec = {
        'module': unchanged,
        'func': unchanged,
        'ref': unchanged,
        'prog': unchanged,
        'path': unchanged,
        'nodefault': flag,
        'nodefaultconst': flag,
        'filename': unchanged,
        'manpage': unchanged,
        'nosubcommands': unchanged,
        'passparser': flag,
        'noepilog': unchanged,
        'nodescription': unchanged,
        'markdown': flag,
        'markdownhelp': flag,
    }

    def _construct_manpage_specific_structure(self, parser_info):
        """
        Construct a typical man page consisting of the following elements:
            NAME (automatically generated, out of our control)
            SYNOPSIS
            DESCRIPTION
            OPTIONS
            FILES
            SEE ALSO
            BUGS
        """
        items = []
        # SYNOPSIS section
        synopsis_section = nodes.section(
            '',
            nodes.title(text='Synopsis'),
            nodes.literal_block(text=parser_info['bare_usage']),
            ids=['synopsis-section'],
        )
        items.append(synopsis_section)
        # DESCRIPTION section
        if 'nodescription' not in self.options:
            description_section = nodes.section(
                '',
                nodes.title(text='Description'),
                nodes.paragraph(
                    text=parser_info.get(
                        'description',
                        parser_info.get('help', 'undocumented').capitalize(),
                    )
                ),
                ids=['description-section'],
            )
            nested_parse_with_titles(self.state, self.content, description_section)
            items.append(description_section)
        if parser_info.get('epilog') and 'noepilog' not in self.options:
            # TODO: do whatever sphinx does to understand ReST inside
            # docstrings magically imported from other places. The nested
            # parse method invoked above seem to be able to do this but
            # I haven't found a way to do it for arbitrary text
            if description_section:
                description_section += nodes.paragraph(text=parser_info['epilog'])
            else:
                description_section = nodes.paragraph(text=parser_info['epilog'])
                items.append(description_section)
        # OPTIONS section
        options_section = nodes.section(
            '', nodes.title(text='Options'), ids=['options-section']
        )
        if 'args' in parser_info:
            options_section += nodes.paragraph()
            options_section += nodes.subtitle(text='Positional arguments:')
            options_section += self._format_positional_arguments(parser_info)
        for action_group in parser_info['action_groups']:
            if 'options' in action_group:
                options_section += nodes.paragraph()
                options_section += nodes.subtitle(text=action_group['title'])
                options_section += self._format_optional_arguments(action_group)

        # NOTE: we cannot generate NAME ourselves. It is generated by
        # docutils.writers.manpage
        # TODO: items.append(files)
        # TODO: items.append(see also)
        # TODO: items.append(bugs)

        if len(options_section.children) > 1:
            items.append(options_section)
        if 'nosubcommands' not in self.options:
            # SUBCOMMANDS section (non-standard)
            subcommands_section = nodes.section(
                '', nodes.title(text='Sub-Commands'), ids=['subcommands-section']
            )
            if 'children' in parser_info:
                subcommands_section += self._format_subcommands(parser_info)
            if len(subcommands_section) > 1:
                items.append(subcommands_section)
        if os.getenv('INCLUDE_DEBUG_SECTION'):
            import json

            # DEBUG section (non-standard)
            debug_section = nodes.section(
                '',
                nodes.title(text='Argparse + Sphinx Debugging'),
                nodes.literal_block(text=json.dumps(parser_info, indent='  ')),
                ids=['debug-section'],
            )
            items.append(debug_section)
        return items

    def _format_positional_arguments(self, parser_info):
        assert 'args' in parser_info
        items = []
        for arg in parser_info['args']:
            arg_items = []
            if arg['help']:
                arg_items.append(nodes.paragraph(text=arg['help']))
            elif 'choices' not in arg:
                arg_items.append(nodes.paragraph(text='Undocumented'))
            if 'choices' in arg:
                arg_items.append(
                    nodes.paragraph(text='Possible choices: ' + ', '.join(arg['choices']))
                )
            items.append(
                nodes.option_list_item(
                    '',
                    nodes.option_group(
                        '', nodes.option('', nodes.option_string(text=arg['metavar']))
                    ),
                    nodes.description('', *arg_items),
                )
            )
        return nodes.option_list('', *items)

    def _format_optional_arguments(self, parser_info):
        assert 'options' in parser_info
        items = []
        for opt in parser_info['options']:
            names = []
            opt_items = []
            for name in opt['name']:
                option_declaration = [nodes.option_string(text=name)]
                if not _is_suppressed(opt['default']):
                    option_declaration += nodes.option_argument(
                        '', text='=' + str(opt['default'])
                    )
                names.append(nodes.option('', *option_declaration))
            if opt['help']:
                opt_items.append(nodes.paragraph(text=opt['help']))
            elif 'choices' not in opt:
                opt_items.append(nodes.paragraph(text='Undocumented'))
            if 'choices' in opt:
                opt_items.append(
                    nodes.paragraph(text='Possible choices: ' + ', '.join(opt['choices']))
                )
            items.append(
                nodes.option_list_item(
                    '',
                    nodes.option_group('', *names),
                    nodes.description('', *opt_items),
                )
            )
        return nodes.option_list('', *items)

    def _format_subcommands(self, parser_info):
        assert 'children' in parser_info
        items = []
        for subcmd in parser_info['children']:
            subcmd_items = []
            if subcmd['help']:
                subcmd_items.append(nodes.paragraph(text=subcmd['help']))
            else:
                subcmd_items.append(nodes.paragraph(text='Undocumented'))
            items.append(
                nodes.definition_list_item(
                    '',
                    nodes.term('', '', nodes.strong(text=subcmd['bare_usage'])),
                    nodes.definition('', *subcmd_items),
                )
            )
        return nodes.definition_list('', *items)

    def _nested_parse_paragraph(self, text):
        content = nodes.paragraph()
        self.state.nested_parse(StringList(text.split('\n')), 0, content)
        return content

    def _open_filename(self):
        # try open with given path
        try:
            return open(self.options['filename'])
        except OSError:
            pass
        # try open with abspath
        try:
            return open(os.path.abspath(self.options['filename']))
        except OSError:
            pass
        # try open with shutil which
        try:
            return open(shutil.which(self.options['filename']))
        except (OSError, TypeError):
            pass
        # raise exception
        raise FileNotFoundError(self.options['filename'])

    def run(self):
        if 'module' in self.options and 'func' in self.options:
            module_name = self.options['module']
            attr_name = self.options['func']
        elif 'ref' in self.options:
            _parts = self.options['ref'].split('.')
            module_name = '.'.join(_parts[0:-1])
            attr_name = _parts[-1]
        elif 'filename' in self.options and 'func' in self.options:
            mod = {}
            f = self._open_filename()
            code = compile(f.read(), self.options['filename'], 'exec')
            exec(code, mod)
            module_name = None
            attr_name = self.options['func']
            func = mod[attr_name]
        else:
            msg = ':module: and :func: should be specified, or :ref:, or :filename: and :func:'
            raise self.error(msg)

        # Skip this if we're dealing with a local file, since it obviously can't be imported
        if 'filename' not in self.options:
            with mock(self.config.autodoc_mock_imports):
                try:
                    mod = importlib.import_module(module_name)
                except ImportError as exc:
                    msg = (
                        f'Failed to import "{attr_name}" from "{module_name}".\n'
                        f'{sys.exc_info()[1]}'
                    )
                    raise self.error(msg) from exc

                if not hasattr(mod, attr_name):
                    msg = (
                        f'Module "{module_name}" has no attribute "{attr_name}"\n'
                        f'Incorrect argparse :module: or :func: values?'
                    )
                    raise self.error(msg)
                func = getattr(mod, attr_name)

        if isinstance(func, ArgumentParser):
            parser = func
        elif 'passparser' in self.options:
            parser = ArgumentParser()
            func(parser)
        else:
            parser = func()
        if 'path' not in self.options:
            self.options['path'] = ''
        path = str(self.options['path'])
        if 'prog' in self.options:
            parser.prog = self.options['prog']
        result = parse_parser(
            parser,
            skip_default_values='nodefault' in self.options,
            skip_default_const_values='nodefaultconst' in self.options,
        )
        result = parser_navigate(result, path)
        if 'manpage' in self.options:
            return self._construct_manpage_specific_structure(result)

        # Handle nested content, where markdown needs to be preprocessed
        items = []
        nested_content = nodes.paragraph()
        if 'markdown' in self.options:
            from sphinxarg.markdown import parse_markdown_block

            items.extend(parse_markdown_block('\n'.join(self.content) + '\n'))
        else:
            self.state.nested_parse(self.content, self.content_offset, nested_content)
            nested_content = nested_content.children
        # add common content between
        items += [
            item for item in nested_content if not isinstance(item, nodes.definition_list)
        ]

        markdown_help = False
        if 'markdownhelp' in self.options:
            markdown_help = True
        if 'description' in result and 'nodescription' not in self.options:
            if markdown_help:
                items.extend(render_list([result['description']], True))
            else:
                items.append(self._nested_parse_paragraph(result['description']))
        items.append(nodes.literal_block(text=result['usage']))
        items.extend(
            print_action_groups(
                result,
                nested_content,
                markdown_help,
                settings=self.state.document.settings,
                id_prefix=f'{module_name}-{attr_name}' if module_name else attr_name,
            )
        )
        if 'nosubcommands' not in self.options:
            items.extend(
                print_subcommands(
                    result,
                    nested_content,
                    markdown_help,
                    settings=self.state.document.settings,
                )
            )
        if 'epilog' in result and 'noepilog' not in self.options:
            items.append(self._nested_parse_paragraph(result['epilog']))

        # Traverse the returned nodes, modifying the title IDs as necessary to avoid repeats
        ensure_unique_ids(items)

        return items


def setup(app):
    app.setup_extension('sphinx.ext.autodoc')
    app.add_directive('argparse', ArgParseDirective)
    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
