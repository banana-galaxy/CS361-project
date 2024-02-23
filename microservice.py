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

def checkAPIKey():
    if not os.path.isfile('api'):
        return 0
    else:
        with open('api') as f:
            key = f.read()
        if key == "":
            return 0
    return 1

print("Starting microservice...")

if not os.path.isfile('api'):
    print("\033[91mAPI key not found. Please create an \"api\" file and place the API key in it.\033[0m")
else:
    with open('api', 'r') as f:
        key = f.read()
    if key == "":
        print("\033[91mAPI key not found. Please place the API key in the \"api\" file\033[0m")

# Microservice main code
app = FastAPI()

@app.get("/{base}-{conversion}")
async def getRate(base: str, conversion: str):
    if not os.path.isfile('rates.json'):
        print("Downloading rates...")
        key = checkAPIKey()
        if key == 1:
            data = getNewRates()
        else:
            return {"result": "error", "api": "key not found"}

        with open('rates.json', 'w') as f:
            json.dump(data, f, indent=2)
    else:
        with open('rates.json') as f:
            data = json.load(f)

        if time.time() > data['time_next_update_unix']:
            print("Updating rates...")

            key = checkAPIKey()
            if key == 1:
                data = getNewRates()
            else:
                return {"result": "error", "api": "key not found"}

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
