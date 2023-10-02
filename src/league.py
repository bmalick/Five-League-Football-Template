from bs4 import BeautifulSoup
import requests, os
from dotenv import load_dotenv


class League:
    
    def __init__(self, name: str, url: str, logo_tag: str, link_logo: str, POST: bool = True) -> None:
        
        self.NOTION_ENDPOINT = "https://api.notion.com/v1/"
        self.name       = name
        self.url        = url
        self.logo_tag   = logo_tag
        self.link_logo  = link_logo
        self.POST       = POST
        
        self.load_env()
        self.load_headers()
        print(self)
        
        self.create_league()
    
    def __str__(self) -> str:
        return "<League name='{}'>".format(self.name)
     
    def load_headers(self) -> None:
        self.headers = {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
            "Authorization": "Bearer " + self.NOTION_API_KEY 
        }
    
    def load_env(self) -> None:
        load_dotenv()
        self.NOTION_API_KEY = os.getenv("NOTION_API_KEY")
        self.LEAGUES_DB_ID   = os.getenv("LEAGUES_DB_ID")
    
    def get_soup(self, url: str) -> BeautifulSoup:
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        return soup
    
    def create_league(self) -> None:
        payload = self.get_payload()
        if self.POST:
            response = requests.post(self.NOTION_ENDPOINT+"pages/", headers=self.headers, json=payload)
            response.raise_for_status()
    
    def get_logo_url(self):
        soup = self.get_soup(self.url)
        logo_url = soup.select_one(self.logo_tag).attrs["src"]
        return logo_url
        
    
    def get_payload(self) -> dict:
        payload = self.league_payload
        
        
        
        payload["properties"]["Name"]["title"][0]["text"]["content"] = self.name
        payload["properties"]["URL"]["url"]                          = self.url
        if self.logo_tag != "": logo_url = self.get_logo_url()
        else: logo_url = self.link_logo
        payload["icon"]["external"]["url"]                           = logo_url
        payload["cover"]["external"]["url"]                          = logo_url
        
        return payload
    
    @property
    def league_payload(self) -> dict:
        payload = {
            "parent": {
                "type": "database_id",
                "database_id": self.LEAGUES_DB_ID
            },
            
            "icon": {
                "type": "external",
                "external": {"url": ""}
            },
            
            "cover": {
                "type": "external",
                "external": {"url": ""}
            },
            
            "properties":{
                "Name": {
                    "title": [{
                        "text": {"content": ""}
                    }]
                },
                "URL": {"url":""}
            }
        }
        
        return payload