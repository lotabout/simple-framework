#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# usage:
# router = Router()
#
# @router.route('/hello/<name>')
# def hello(name):
#    return 'Hello %s' % name
#
# func, args = router.match('/hello/world')
# print(func.call(**args))

import re

# used to parse rules
_rule_re = re.compile(r'''
        (?P<prefix>[^<]*)                      # rule prefix
        (?:
          <
          (?P<name>[a-zA-Z_][a-zA-Z0-9_]*)?    # variable name
          (?:
            (?::(?P<filter>[a-zA-Z_]*))        # filter name
            (?::(?P<config>[^>]+))?            # config name
          )?                                   # can contain filter or not
          >
        )?                                     # can contain wildcard or not
''', re.VERBOSE)

# copied from bottle.py
def _re_flatten(regex):
    """turn capturing groups into non capturing groups"""
    if '(' not in regex:
        return regex
    return re.sub(r'(\\*)(\(\?P<[^>]+>|\((?!\?))', lambda m: m.group(0) if
            len(m.group(1)) % 2 else m.group(1) + '(?:', p)

class Router():
    """Routing class"""

    default_pattern = '^[^/]'
    default_filter = 're'

    def __init__(self):
        self.rules = []
        self.filters = {
                're':    lambda conf: _re_flatten(conf or self.default_pattern),
                'int':   lambda conf: r'-?\d+',
                'float': lambda conf: r'-?[\d.]+',
                'path':  lambda conf: r'.+?',
                }

    def match(self, environ):
        """dispatch URL

        :environ: TODO
        :returns: TODO

        """
        pass

    def route(self, path=Nonne, method='GET', callback=None):
        """Add a rule to router

        :path: TODO
        :method: TODO
        :callback: TODO
        :returns: TODO

        """
        pass

    def add(self, rule, method, target, name=None):
        """TODO: Docstring for add.

        :rule: TODO
        :method: TODO
        :target: TODO
        :name: TODO
        :returns: TODO

        """
        pass
