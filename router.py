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
# print(func(**args))

import re

def makelist(data):
    if isinstance(data, (tuple, list, set, dict)):
        return list(data)
    elif data:
        return [data]
    else:
        return []

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
            len(m.group(1)) % 2 else m.group(1) + '(?:', regex)

class Router():
    """Routing class"""

    default_pattern = '[^/]+'
    default_filter = 're'

    def __init__(self):
        self.rules = {}         # rule[method] = [rule1, rule2, ...]
        self.static_rules = {}
        self.dynamic_rules = {}
        self.dispatch = None

        # filter is use to parse patterns such as <name:filter:conf>
        # a filter is a function that takes conf and return (conf_to_regex, str_to_param)
        self.filters = {
                're':    lambda conf: (_re_flatten(conf or self.default_pattern), None),
                'int':   lambda conf: (r'-?\d+', int),
                'float': lambda conf: (r'-?[\d.]+', float),
                'path':  lambda conf: (r'.+?', None)
                }

    def add_filter(self, name, func):
        """Add a custom filter"""
        self.filters[name] = func

    def match(self, environ):
        """dispatch URL

        :environ: TODO
        :returns: (target_function, dict_of_parameters)

        """
        method = environ['REQUEST_METHOD'].upper()
        path = environ['PATH_INFO'] or '/'

        if method in self.static_rules and path in self.static_rules[method]:
            target, getargs = self.static_rules[method][path]
            return target, getargs(path) if getargs else {}
        elif method in self.dynamic_rules and self.dispatch is not None:
                match = self.dispatch(path)
                if match:
                    _, _, target, getargs = self.dynamic_rules[method][match.lastindex-1]
                    return target, getargs(path) if getargs else {}

        # Not found
        raise Exception('404')

    def route(self, path=None, method='GET', callback=None):
        """Add a rule to router, this is a decorator

            @router.route('/hello/<name>')
            def hello(name):
               return 'Hello %s' % name

        the `<name>` part is wildcard.

        :path: URL pattern
        :method: ['GET' or 'POST' or ...]
        :callback: callback function, i.e. target handler
            This is used when you don't want avoid the decorator style. so that we can use
            `route(..., callback=func)`, and equals `route(...)(func)`

        """
        if callable(path):
            path, callback = None, path

        def decorator(callback):
            for rule in makelist(path):
                self.add(rule, method.upper(), callback)
            return callback

        return decorator(callback) if callback else decorator

    def add(self, rule, method, target):
        """add a new rule

        :rule: URL pattern such as '/hello/<name>'
        :method: ['GET' or 'POST' or ...]
        :target: handler if a rule is matched

        """
        is_static = True
        method = method.upper()
        filters = {}

        # we konw the last one is dummy
        components = [x.groups() for x in _rule_re.finditer(rule)][:-1]
        target_regex = []
        for prefix, name, mode, conf in components:
            if prefix:
                target_regex.append(re.escape(prefix))

            if name is None and mode is None and conf is None:
                continue

            is_static = False
            if not name:
                raise Exception('Invalid Pattern, should be "<name:mode:conf>"')

            if not mode:
                mode = self.default_filter

            tmp_regex, out_filter = self.filters[mode](conf)
            if out_filter: filters[name] = out_filter
            target_regex.append('(?P<%s>%s)' % (name, tmp_regex))

        if is_static:
            self.static_rules.setdefault(method, {})
            self.static_rules[method][''.join(target_regex)] = (target, None)
            return

        # non-static rules
        re_pattern = '^(%s)$' % ''.join(target_regex)
        re_match = re.compile(re_pattern).match

        if filters:
            def get_args(url):
                """get the url parameters and handle them by out_filters"""
                params = re_match(url).groupdict()
                for name, out_filter in filters.items():
                    params[name] = out_filter(params[name])
                return params
        else:
            def get_args(url):
                """get the url parameters"""
                return re_match(url).groupdict()

        # at last, build the pattern into the dispather
        flatpat = _re_flatten(re_pattern)
        whole_rule = (rule, flatpat, target, get_args)

        self.dynamic_rules.setdefault(method, []).append(whole_rule)
        self._compile(method)

    def _compile(self, method):
        """compile the dynamic rules for method"""
        all_rules = self.dynamic_rules[method]

        all_regexes = (flatpat for _, flatpat, _, _ in all_rules)
        combined = re.compile('|'.join('(^%s$)' % flatpat for flatpat in all_regexes))
        self.dispatch = combined.match
