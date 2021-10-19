# navitia_python_wrapper
Python wrapper around the navitia API (api.navitia.io)

## Usage
```python
import navitia_wrapper

url = "http://api.navitia.io/"
api_key = "get_your_token_own_api_key_on_navitia.io"
coverage = "fr-idf"

nav = navitia_wrapper.Navitia(url=url, token=api_key).instance(coverage)

print(nav.stop_areas("stop_area:OIF:SA:8768600")[0]['label'])
```
