import requests, os
from dotenv import load_dotenv


class Team:
    def __init__(self, league_db_id: str, team_name: str, team_url: str, team_logo: str, POST: bool = True) -> None:
        
        self.league_db_id = league_db_id
        self.team_name    = team_name.upper()
        self.team_url     = team_url
        self.team_logo    = team_logo 
        self.POST         = POST
        
        self.NOTION_ENDPOINT = "https://api.notion.com/v1/"
        self.load_env()
        self.load_headers()
        self.create_team()

        print(self)
    
    def __str__(self):
        return "<Team {}>".format(self.team_name)

    def load_env(self):
        load_dotenv()
        self.TEAMS_DB_ID    = os.getenv("TEAMS_DB_ID")
        self.NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    
    def load_headers(self) -> None:
        self.headers = {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
            "Authorization": "Bearer " + self.NOTION_API_KEY
        }


    def create_team(self):
        
        payload = self.get_payload()
        if self.POST:
            response = requests.post(self.NOTION_ENDPOINT+"pages/", headers=self.headers, json=payload)
            response.raise_for_status()
        
        
    def get_payload(self):
        payload = self.team_payload
        
        payload["icon"]["external"]["url"]                           = self.team_logo
        payload["cover"]["external"]["url"]                          = self.team_logo
        payload["properties"]["Name"]["title"][0]["text"]["content"] = self.team_name
        payload["properties"]["Team URL"]["url"]                     = self.team_url
        payload["properties"]["League"]["relation"][0]["id"]         = self.league_db_id
        
        return payload
        
    @property
    def team_payload(self):
        payload = {
            "parent": {
                "type": "database_id",
                "database_id": self.TEAMS_DB_ID
            },
            
            "icon": {
                "type": "external",
                "external": {"url": ""}
            },
            
            "cover": {
                "type": "external",
                "external": {"url": ""}
            },
            
            "properties": {
                "Name": {
                    "title": [{
                        "text": {"content": ""}
                    }]
                },
                "Team URL": {"url": ""},
                "League": {
                    "relation": [{"id": ""}]
                }
            }
        }
        
        return payload
    