"""
This is really hard to test. Pyconf provides an API for declarative global configs. 
That means encapsulating those configs is going to be a challenge. We'll see
"""
from pyconf.config import Config, Parameter
from pyconf.section import Section


def test_basic_config():
    with Config(app_name='test', default_format='toml', env_prefix='MY_APP_'):
        with Section('my_app'):
            version = Parameter('version', default='1.0', env=False)
            
            with Section('subsection'):
                a = Parameter('a', cl_flags=['-a', '--a'])
            
            with Section('section2', cl_prefix='sec2-'):
                b = Parameter('b')
