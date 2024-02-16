#! get_keys
#! load headers
#! create
import sys
import yaml, unidecode, requests
from bs4 import BeautifulSoup
from bs4.element import Tag

class Utils:

    @staticmethod
    def add_path(path: str) -> None:
        sys.path.append(path)

    @staticmethod
    def get_id(id_name: str) -> str:
        id_name = unidecode.unidecode(id_name.replace(" ", "").lower())
        with open("./ids.yaml", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return data.get(id_name, None)

    @staticmethod
    def headers() -> dict:
        return {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
            "Authorization": "Bearer " + Utils.get_id("notion_api_key")
        }

    @staticmethod
    def post(endpoint: str, payload: dict) -> None:

        params = {
            "url": endpoint,
            "json": payload,
            "headers": Utils.headers()
        }
        
        response = requests.post(**params)
        # print(response.text)
        response.raise_for_status()
        return response
    
    @staticmethod
    def update(endpoint: str, payload: dict) -> None:
        
        params = {
            "url": endpoint,
            "json": payload,
            "headers": Utils.headers()
        }
        
        response = requests.patch(**params)
        response.raise_for_status()
        return response
    
    @staticmethod
    def get_soup(url: str) -> Tag:
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, "html.parser")

