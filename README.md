# CS361 Project

## Request and receive data from microservice
```python
# import requests library to request data from microservice
from requests import request

# request data
# upon receiving the data, retrieve the json payload and store in "data" variable 
data = request('GET', 'http://localhost:8000/USD-RUB').json()

# print the data
print(data)
```

`{'result': 'success', 'rate': 92.4172}`

## UML diagram
```mermaid
sequenceDiagram
    App->>+Microservice: Request currency conversion rate
    alt if conversion rates not stored
        Microservice->>+API: Request all rates
        API->>-Microservice: Return all rates
        Microservice->>Microservice: Store rates
    else if conversion rates stored
        Microservice->>Microservice: Get stored rates
        alt if rates are outdated
            Microservice->>+API: Request all rates
            API->>-Microservice: Return all rates
            Microservice->>Microservice: Store rates
        end
    end
    Microservice->>Microservice: Calculate requested rate
    Microservice->>-App: Conversion rate
```