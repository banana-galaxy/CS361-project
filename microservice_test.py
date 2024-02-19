from requests import request

print("Requesting the data")
data = request('GET', 'http://localhost:8000/USD-RUB')

print("Getting the json payload from the received data")
data = data.json()

print("Data: ", data)