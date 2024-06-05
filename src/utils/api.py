import requests

class APIHandler():
    def __init__(self, base_url: str, api_token: str) -> None:
        self.__base_url = base_url
        self.__api_token = api_token
        self.__headers = {"Authorization": f"Bearer {api_token}"}
        print('API Handler successfully initialized!')

    def get(self, endpoint: str, params: str=None):
        url = f'{self.__base_url}/{endpoint}'
        response = requests.get(url, params=params, headers=self.__headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict = None, json: dict = None):
        url = f'{self.__base_url}/{endpoint}'
        response = requests.post(url, data=data, json=json, headers=self.__headers)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: dict = None, json: dict = None):
        url = f'{self.__base_url}/{endpoint}'
        response = requests.put(url, data=data, json=json, headers=self.__headers)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str, data: dict = None, json: dict = None):
        url = f'{self.__base_url}/{endpoint}'
        response = requests.delete(url, headers=self.__headers)
        response.raise_for_status()
        return response.json()