#!/usr/bin/env python

"""
Reads config files from defined locations

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

class ConfigFileReader:
    """
    Encapsulates reading from multiple config files from multiple locations

    Instantiate a ConfigFileReader with instructions about how to search for config files.
    """

    DEFAULT_LOCATIONS = [
        '/opt/{app_name}/{file}'
        '~/.{app_name}/{file}'
        './{app_name}{suffix}'
    ]

    # define the supported formast and default search order
    DEFAULT_FORMATS = [
        'toml',
        'yaml',
        'conf',
        # 'ini', # Don't support ini by default because of how complex and non-standard it is
    ]

    SUFFIXES = {
        'toml': ['.toml'],
        'yaml': ['.yaml', '.yml'],
        'conf': ['.conf', '.config'],  # Uses the python ConfigParser implementation
        '.ini': ['.ini'],  # allows extended ini format
    }

    def __init__(self, app_name, locations=None, formats=None):
        self.app_name = app_name
        self.locations = locations or self.DEFAULT_LOCATIONS
        self.formats = formats or self.DEFAULT_FORMATS


