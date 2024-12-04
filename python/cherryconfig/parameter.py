"""
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
from cherryconfig import context_manager
from cherryconfig.string_manipulation import camel_case_to_dash_sep, camel_case_to_snake_case


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

