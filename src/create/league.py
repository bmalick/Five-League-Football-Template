import sys; sys.path.append("./")

from src.create.payloads import LeaguePayload
from src.utils import Utils


class League:
    NOTION_ENDPOINT = "https://api.notion.com/v1/pages"
    
    def __init__(self, name: str, url: str, link_logo: str, post: bool = True, logo_tag: str = None) -> None:
        
        self.name       = name
        self.url        = url
        self.logo_tag   = logo_tag
        self.link_logo  = link_logo
        self.post       = post
        
        self.params = {
            "name": name,
            "url":  url
        }

        print(self)
        
        self.__call__()
    
    def __str__(self) -> str:
        return "<League name='{}'>".format(self.name)

    
    def __call__(self) -> None:
        if self.logo_tag is not None: logo_url = self.get_logo_url()
        else: logo_url = self.link_logo

        self.params = {
            **self.params,
            "logo_url": logo_url
            
        }

        payload = LeaguePayload(self.params)
        if self.post:
            Utils.post(endpoint=self.NOTION_ENDPOINT, payload=payload)
    
    def get_logo_url(self):
        soup = Utils.get_soup(self.url)
        logo_url = soup.select_one(self.logo_tag).attrs["src"]
        return logo_url
        
