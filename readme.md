# Cherry Config 
![Cherry Config](docs/img/logo_256x192.png)

Cherry Config attempts to create a python library for defining configuration parameters in a cohesive easy-to-read 
manner. Generally speaking, it attempts to abstract acquiring parameters away from defining values.

## Example

Quick example:

```python
import cherryconfig
with cherryconfig.Config('my_application') as config:
    with cherryconfig.Section('my_application') as main_section:
        config_version = '1.0'
        cache_path = '/tmp/cache'
        
# Somewhere else in code
def functionality():
    print(config.my_application.cache_path)
```

```bash
$ python -m my_application --cache-path=/tmp/cache/my_application
/tmp/cache/my_application
```