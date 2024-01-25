import sys; sys.path.append("./")

from src.utils import Utils

class Payload:
    def __new__(self, database_id: str) -> dict:
        database_id
 
        return {
            "parent": {
                "type": "database_id",
                "database_id": database_id
            },
            
            "properties": {
                "Name": {
                    "title": [{
                        "text": {"content": ""}
                    }]
                },
                
            }
        }
    
    @staticmethod
    def add_image(payload):
        return {
            **payload,
            "icon": {
                "type": "external",
                "external": {"url": ""}
            }
            }
    

# League
class LeaguePayload(Payload):
    def __new__(self, params) -> dict:
        payload = super().__new__(self, database_id=Utils.get_id("leagues_db"))
        
        if params.get("logo_url") is not None:
            payload = self.add_image(payload)
            payload["icon"]["external"]["url"]  = params.get("logo_url")
            payload["cover"] = payload["icon"]
        
        payload["properties"]["Name"]["title"][0]["text"]["content"] = params.get("name")
        payload["properties"] = {
            **payload["properties"],
            "URL" : {"url": params.get("url")}
        }
        

        return payload

# Team
class TeamPayload(Payload):
    def __new__(self, params) -> dict:
        payload = super().__new__(self, database_id=Utils.get_id("teams_db"))

        if params.get("team_logo") is None:
            payload = self.add_image(payload)
            payload["icon"]["external"]["url"] = params.get("team_logo")
            payload["cover"]                   = payload["icon"]
        payload["properties"]["Name"]["title"][0]["text"]["content"] = params.get("team_name")

        payload["properties"] = {
            **payload["properties"],
            "Team URL" : {"url": params.get("team_url")},
            "League" : {"relation": [{"id": Utils.get_id(params.get("league"))}]}
        }
        
        return payload



# Player
class PlayerPayload(Payload):
    def __new__(self, params) -> dict:
        payload = super().__new__(self, database_id=Utils.get_id("players_db"))

        if params.get("player_img") is not None:
            payload = self.add_image(payload)
            payload["icon"]["external"]["url"] = params.get("player_img")
            payload["cover"]                   = payload["icon"]
        payload["properties"]["Name"]["title"][0]["text"]["content"] = params.get("player_name")

        payload["properties"] = {
            **payload["properties"],
            "Club": {
                "relation": [{"id": Utils.get_id(params.get("team"))}]
            },
            "National Team": {
                "rich_text": [{
                    "text": {"content": params.get("player_national_team")}
                }]
            },
            "Age": {"number": params.get("player_age")},
            "Position": {
                "select": {"name": params.get("player_pos")}
            },
            "Weight": {"number": params.get("player_weight")},
            "Height": {"number": params.get("player_height")},
            "Jersey Number": {"number": params.get("player_num")},
        }

        return payload


# Match
class MatchPayload(Payload):
    
    def __new__(self, params) -> dict:
        payload = super().__new__(self, database_id=Utils.get_id("matches_db"))
        payload = self.add_image(payload)

        payload["icon"]["external"]["url"] = "https://www.notion.so/icons/playback-play_gray.svg"
        payload["properties"]["Name"]["title"][0]["text"]["content"] = "%s : %s vs %s" % (
            params.get("matchday"), params.get("home_team").upper(), params.get("away_team").upper()
        )

        payload["properties"] = {
            **payload["properties"],
            "Home Team": {"relation": [{"id": Utils.get_id(params.get("home_team"))}]},
            "Away Team": {"relation": [{"id": Utils.get_id(params.get("away_team"))}]},
            "Date": {"date": {"start": params.get("match_date"), "time_zone": "Europe/Paris"}},
            "League": {"relation": [{"id": Utils.get_id(params.get("league"))}]},
        }

        payload = {
            **payload,
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