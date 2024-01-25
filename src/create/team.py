import sys; sys.path.append("./")

from src.create.payloads import TeamPayload
from src.utils import Utils


class Team:
    def __init__(self, league: str, team_name: str, team_url: str, team_logo: str, post: bool = True) -> None:
        
        self.league = league
        self.team_name    = team_name.upper()
        self.post         = post
        
        self.NOTION_ENDPOINT = "https://api.notion.com/v1/pages"

        self.params = {
            "team_logo": team_logo,
            "team_logo": team_logo,
            "team_name": self.team_name,
            "team_url":  team_url,
            "league":    league
        }

        self.__call__()
        print(self)
    
    def __str__(self):
        return "<Team {}>".format(self.team_name)

    def __call__(self):
        
        payload = TeamPayload(params=self.params)
        if self.post:
            Utils.post(endpoint=self.NOTION_ENDPOINT, payload=payload)

    