import requests

# this code assumes that the device/server is within the same network
def send_data(data: str):
    url = "http://10.10.144.89:8001/classify"
    response = requests.post(url, json={"data": data})
    if response.status_code == 200:
        return response.json()
    else:
        return "Error: Unable to process data"

if __name__ == "__main__":
    data = "mero paisa khai"
    result = send_data(data)
    print("Processed Data:", result)