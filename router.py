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
        self.rules = []         # rule[method] = [rule1, rule2, ...]
        self.static_rules = []
        self.dynamic_rules = []
        self.dispatcher = None

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

    def add(self, rule, method, target):
        """add a new rule

        :rule: TODO
        :method: TODO
        :target: TODO
        :name: TODO
        :returns: TODO

        """
        is_static = True

        # we konw the last one is dummy
        components = [x.groups() for x in _rule_re.finditer(rule)][:-1]
        target_regex = []
        for prefix, name, mode, conf in components:
            if prefix:
                target_url_regex.append(re.escape(prefix))

            if name is None and mode is None and conf is None:
                continue

            is_static = False
            if not name:
                raise Exception('Invalid Patter, should be "<name:mode:conf>"')

            if not mode:
                mode = self.default_filter

            tmp_regex = self.filters[mode](conf)
            target_regex.append('(?P<%s>%s)' % name, regex)

        if is_static:
            self.static_rules.setdefault(method, {})
            self.static_rules[method][''.join(target_regex)] = (target, None)
            return

        # non-static rules
        re_pattern = re.compile('^(%s)$' % ''.join(target_regex))
        re_match = re_pattern.match

        def get_args(self, url):
            """get the url parameters"""
            return re_match(url).groupdict()

        # at last, build the pattern into the dispather
        flatpat = _re_flatten(pattern)
        whole_rule = (rule, flatpat, target, get_args)

        self.dynamic_rules.setdefault(method, []).append(whole_rule)
        self._compile(method)

    def _compile(self, method):
        """compile the dynamic rules for method"""
        all_rules = self.dynamic_rules[method]

        all_regexes = (flatpat for _, flatpat, _, _ in all_rules)
        combined = re.compile('|'.join('(^%s$)' % flatpat for flatpat in all_regexes))
        self.dispatcher = combined.match
