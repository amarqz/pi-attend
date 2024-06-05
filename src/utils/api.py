import requests

class APIHandler():
    def __init__(self, base_url: str, email: str, password: str) -> None:
        self.__base_url = base_url
        self.__headers = {}
        admin_info = self.post("admins/auth-with-password", json={'identity': email, 'password': password})
        self.__headers = {"Authorization": f"Bearer {admin_info['token']}"}
        
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