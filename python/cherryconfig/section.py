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
from cherryconfig.parameter import Parameter


class Section:
    def __init__(self, name, **kwargs):
        self.name = name
        self._parameters = {}

    def __getattr__(self, item):
        if item not in self._parameters:
            raise AttributeError("No such property: " + str(item))

        return self._parameters[item]

    def __setattr__(self, key, value):
        self._parameters[key] = value

    def __enter__(self):
        context_manager.CURRENT_CONTEXT.append(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        context_manager.CURRENT_CONTEXT[::-1].remove(self)
