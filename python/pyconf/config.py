#!/usr/bin/env python

"""
Defines the main interface for declarative configuration file.

The pattern here is a little bit crazy, and operates on some single-threading assumptions
In order to reduce the redundancy of the API, there is a global registry that constructors add themsleves to.
For example:

>>> Config('my_config')

will create a config object, and add it to ConfigRegistry.currentConfig. 

Similarly:
>>> with Section('section_a')

will add itself to the current Config instance



MIT License

Copyright (c) 2024 Stefan Sullivan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import re

from pyconf import context_manager
from pyconf.section import Section


class Config:
    CURRENT_CONTEXT = None  # create a singleton context variable to allow Parameters to reference it

    def __init__(self, app_name, default_format='toml', env_prefix=None, cl_prefix=None):
        self._app_name = app_name
        self._default_format = default_format
        self._env_prefix = env_prefix or f'{camel_case_to_snake_case(app_name)}'
        self._cl_prefix = cl_prefix or f'--{camel_case_to_dash_sep(app_name)}'

        self._sections = {"<GLOBAL SECTION>": Section()}
        Config.CURRENT_CONTEXT = self

    def __getattr__(self, item):
        if item in self._sections["<GLOBAL SECTION>"]:
            return getattr(self._sections, item)
        elif item in self._sections:
            return self._sections[item]

    def section(self, name, *, context=None, **kwargs):
        """ Build a section """
        if context is None:
            context = context_manager.CURRENT_CONTEXT

        if name in self._sections:
            return self._sections[name]

        section = Section(**kwargs)
        self._sections[name] = section
        context.append(section)

        return section


class Parameter:
    def __init__(self, name, default=None, type=str, cl=True, env=True, cl_flags=None, env_var=None, context=None):
        if context is None:
            context = context_manager.CURRENT_CONTEXT

        if cl and cl_flags is None and context._cl_prefix is not None:
            cl_flags = [f'{context._cl_prefix}-{camel_case_to_dash_sep(name)}']
        if env and env_var is None:
            env_var = f'{context._env_prefix}_{camel_case_to_snake_case(name)}'

        context.append(self)
        self.name = name
        self.cl_flags = cl_flags
        self.env_var = env_var
        self._value = None
        self._default = default
        self._decode = type

    def get_value(self, readers):
        for r in readers:
            if r.has(self.name):
                return r.get(self.name, cl_flags=self.cl_flags, env_var=self.env_var)

        return self._default


def camel_case_to_snake_case(s):
    regex = re.compile(r'(?<!^)(?=[A-Z])')
    return regex.sub('_', s).upper()

def camel_case_to_dash_sep(s):
    snake_case = camel_case_to_snake_case(s)
    return snake_case.replace('_', '-')
