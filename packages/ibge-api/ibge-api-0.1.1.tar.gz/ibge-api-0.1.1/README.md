# IBGE API
Simple library to get City information from IBGE

### Installation
```
pip install ibge-api
```

### Get started
How to get data from a city with this lib:

```Python
from ibge_api import IbgeAPI

# Instantiate a IbgeAPI object
ibge = IbgeAPI('05513970')

# Call the get_city_information method
city_data = ibge.get_city_information()

# Call the city_data property
city_data = ibge.city_data
```