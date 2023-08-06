import requests

def get_facts(number: int = 1):
    url = "https://meowfacts.herokuapp.com/"
    header = {'count': str(number)}
    response = requests.request("GET", url, headers=header)
    return response.json().get("data")