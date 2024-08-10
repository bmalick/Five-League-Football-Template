import requests, unidecode
from src.base import Base
from src.utils import read_yaml, save_yaml
from src.notion import NotionApiHandler
# todo: make a table for properties in datasate of hw i canll it
class Team(Base):
    def __init__(self, league: str, name: str, url: str, logo: str) -> None:
        super().__init__()
        id_name = self.get_id_name(name)
        self.save_parameters(
            league=league, name=name, id_name=id_name,
            logo=logo, url=url, api_handler=NotionApiHandler())
        
        self.create()
        
    
    def __str__(self):
        return "%s<%s - %s>" % (''.ljust(20), self.league, self.name)

    def create(self):
        if self.exists(): return
        data = self.api_handler.create_page_in_database(
            database_id=self.api_handler.keys["teams_db_token"],
            data={
                "icon": {"url": self.logo},
                "cover": {"url": self.logo},
                "properties": [
                    {"name": "Name", "type": "page_title", "values": {"title": self.name}},
                    {"name": "url", "type": "url", "values": {"url": self.url}},
                    {"name": "league", "type": "relation", "values": {"id": self.api_handler.keys["league_ids"][self.get_id_name(self.league)]}},
                ],
                # "children": []
            }
        )
        self.team_id = data["id"]
        print(self)

    def exists(self):
        team = self.api_handler.query_database(
            database_id=self.api_handler.keys["teams_db_token"],
            filters={
                "or": [
                    {
                        "property": "Name",
                        "rich_text": {"equals": self.name}
                    }
                ]
            }
        )
        return len(team)>0

    def add_id(self, page_id):
        ids = read_yaml("keys.yaml")
        if not "team_ids" in ids:
            ids["team_ids"] = {}
        ids["team_ids"][self.id_name] = page_id
        save_yaml("keys.yaml", ids)
        # print("%s%s id is saved." % (''.ljust(21), self.name))


