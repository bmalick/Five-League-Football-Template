from dotenv import load_dotenv
import os, unidecode, requests, time

class Match:
    def __init__(
            self, league_db_id: str,
            matchday: str, match_date: str,
            home_team: str, away_team: str,
            POST: bool = True
        
    ) -> None:
        self.NOTION_ENDPOINT = "https://api.notion.com/v1/"
        
        self.LEAGUE_PAGE_ID = league_db_id     
        self.matchday       = matchday
        self.match_date     = match_date
        self.home_team      = home_team
        self.away_team      = away_team
        self.POST           = POST
        self.get_teams_id()
        
        self.load_env()
        self.load_headers()
        self.create_match()
        
        print(self)
    
    def __str__(self):
        return "<Match home='{}', away='{}', date='{}'>".format(unidecode.unidecode(self.home_team), unidecode.unidecode(self.away_team), self.match_date)
    
    def get_teams_id(self):
        load_dotenv()
        self.home_team_key  = os.getenv(unidecode.unidecode(self.home_team.replace(" ", "").lower()))
        self.away_team_key  = os.getenv(unidecode.unidecode(self.away_team.replace(" ", "").lower()))
    
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
        self.MATCHES_DB_ID  = os.getenv("MATCHES_DB_ID")
        self.NOTION_API_KEY = os.getenv("NOTION_API_KEY")

        
    
    def create_match(self) -> None:
        
        payload = self.get_payload()
        if self.POST:
            response = requests.post(self.NOTION_ENDPOINT+"pages/", headers=self.headers, json=payload)
            response.raise_for_status()
        
    
    def get_payload(self) -> dict:
        payload = self.match_payload
        
        payload["properties"]["Name"]["title"][0]["text"]["content"] = "{} : {} vs {}".format(self.matchday, self.home_team.upper(), self.away_team.upper())
        payload["properties"]["Home Team"]["relation"][0]["id"]      = self.home_team_key
        payload["properties"]["Away Team"]["relation"][0]["id"]      = self.away_team_key
        payload["properties"]["Date"]["date"]["start"]               = self.match_date
        
        return payload
        
    @property
    def match_payload(self) -> dict:
        payload = {
            "parent": {
                "type": "database_id",
                "database_id": self.MATCHES_DB_ID
            },
            
            "icon": {
                "type": "external",
                "external": {"url": "https://www.notion.so/icons/playback-play_gray.svg"}
            },
            
            "properties": {
                "Name": {
                    "title": [{
                        "text": {"content": ""}
                    }]
                },
                "Home Team": {"relation": [{"id": ""}]},
                "Away Team": {"relation": [{"id": ""}]},
                "Date": {"date": {"start": "", "time_zone": "Europe/Paris"}},
                "League": {"relation": [{"id": self.LEAGUE_PAGE_ID}]}
            },
            
            "children": [
                {
                    "object": "block",
                    "type": "quote",
                    "quote": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "Your impressions on the match !!!"}
                        }]
                    }
                }
            ]
        }
        
        return payload