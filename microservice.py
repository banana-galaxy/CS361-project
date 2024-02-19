from fastapi import FastAPI
import requests, os, json, time

# Getting conversion rates on microservice startup
# Storing them to minimize API use
# Updating stored rates as necessary
def getNewRates():
    print("Getting new rates...")
    with open('api') as f:
        key = f.read()
    url = f'https://v6.exchangerate-api.com/v6/{key}/latest/USD'

    response = requests.get(url)
    return response.json()

print("Starting microservice...")

# Microservice main code
app = FastAPI()

@app.get("/{base}-{conversion}")
async def getRate(base: str, conversion: str):
    if not os.path.isfile('rates.json'):
        print("Downloading rates...")
        data = getNewRates()

        with open('rates.json', 'w') as f:
            json.dump(data, f, indent=2)
    else:
        with open('rates.json') as f:
            data = json.load(f)

        if time.time() > data['time_next_update_unix']:
            print("Updating rates...")
            data = getNewRates()
            with open('rates.json', 'w') as f:
                json.dump(data, f, indent=2)

    rates = data['conversion_rates']

    if base not in rates.keys():
        return {"result": "error",
                "currency": base}
    elif conversion not in rates.keys():
        return {"result": "error",
                "currency": conversion}

    return {"result": "success",
            "rate": rates[conversion]/rates[base]}
