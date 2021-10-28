# navitia_python_wrapper
Python wrapper around the navitia API (api.navitia.io)

Python 3 is required.

If you are using Python 2, please refer to v1.0.0

## Usage
```python
import navitia_wrapper

url = "http://api.navitia.io/"
api_key = "get_your_token_own_api_key_on_navitia.io"
coverage = "fr-idf"

nav = navitia_wrapper.Navitia(url=url, token=api_key).instance(coverage)

print(nav.stop_areas("stop_area:OIF:SA:8768600")[0]['label'])
```
