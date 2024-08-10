import os, yaml, requests, unidecode
from bs4 import BeautifulSoup
from src.utils import Parameters, read_yaml, save_yaml
from typing import Union, List, Dict, Any

# TODO

class Base(Parameters):
    
    @staticmethod
    def get_soup(url: str) -> BeautifulSoup:
        try:
            response = requests.get(url=url)
        except requests.exceptions.RequestException as e:
            return None
        return BeautifulSoup(response.text, "html.parser")
    
    @staticmethod
    def get_item(soup, selector):
        item = soup.select_one(selector=selector)
        if item is not None:
            return item.get_text().strip()
        return
    @staticmethod
    def get_items(soup, selector):
        items = soup.select(selector=selector)
        if len(items)>0:
            return [item.get_text().strip() for item in items]
        return
    
    def create_dir(self, path: str): os.makedirs(path, exist_ok=True)

    @staticmethod
    def get_id_name(name):
        return unidecode.unidecode(name.replace(" ", "").lower())
