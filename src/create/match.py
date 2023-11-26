import sys; sys.path.append("./src")

import unidecode
from create.payloads import MatchPayload
from utils import Utils

class Match:
    def __init__(
            self, league: str,
            matchday: str, match_date: str,
            home_team: str, away_team: str,
            post: bool = True
        
    ) -> None:
        
        self.NOTION_ENDPOINT = "https://api.notion.com/v1/pages"
        self.post            = post

        self.params = {
            "league":league,
            "matchday": matchday,
            "match_date":match_date,
            "home_team": home_team,
            "away_team": away_team
        }

        self.home_team  = home_team
        self.away_team  = away_team
        self.match_date = match_date

        self.__call__()
        
        print(self)
    
    def __str__(self):
        return "<Match home='{}', away='{}', date='{}'>".format(unidecode.unidecode(self.home_team), unidecode.unidecode(self.away_team), self.match_date)

    def __call__(self) -> None:
        
        payload = MatchPayload(params=self.params)
        if self.post:
            Utils.post(endpoint=self.NOTION_ENDPOINT, payload=payload)
        
    