import sys; sys.path.append("./src")
from utils import Utils

class UpdateScore:
    database_endpoint = "https://api.notion.com/v1/databases"
    page_endpoint = "https://api.notion.com/v1/pages"

    @classmethod
    def match_exists(cls, date: str, home_team: str, away_team: str):
        matches = UpdateScore.find_fixtures(date, home_team, away_team, limit=1)
        return len(matches) == 1
    
    @classmethod
    def get_league_gameweek(cls, league_name: str):
        database_id = Utils.get_id("matches_db")
        url = "%s/%s/query" % (cls.database_endpoint, database_id)

        payload = {
            "page_size": 1,
            "filter":{
                "and": [
                    {
                        "property": "Date",
                        "date": {"this_week": {}}
                    },
                    {
                        "property": "League",
                        "relation": {"contains": Utils.get_id(league_name)}
                    }
                    
                ]
            }
        }

        response = Utils.post(endpoint=url,payload=payload)
        gameweek = response.json()["results"][0]
        gameweek = gameweek["properties"]["Name"]["title"][0]["text"]["content"]
        gameweek = gameweek.split(':')[0].split("GW")[-1].strip()
        
        return int(gameweek)
    


    @classmethod
    def find_fixtures(cls, date: str, home_team: str, away_team: str, limit=100) -> list[dict]:
        database_id = Utils.get_id("matches_db")
        url = "%s/%s/query" % (cls.database_endpoint, database_id)

        home_team_id = Utils.get_id(home_team)
        away_team_id = Utils.get_id(away_team)

        payload = {
            "page_size": limit,
            "filter":{
                "and": [
                    {
                        "property": "Date",
                        "date": {"equals": date}
                    },
                    {
                        "property": "Home Team",
                        "relation": {"contains": home_team_id}
                    },
                    {
                        "property": "Away Team",
                        "relation": {"contains": away_team_id}
                    }
                    
                ]
            }
        }

        response = Utils.post(endpoint=url,payload=payload)
        return response.json()["results"]


    @classmethod
    def update(cls, date, home_team, away_team, home_score, away_score):

        fixtures = UpdateScore.find_fixtures(date, home_team, away_team)

        home_team_id = Utils.get_id(home_team)
        away_team_id = Utils.get_id(away_team)

        for item in fixtures:
            match_id = item["id"]

            url = "%s/%s" % (cls.page_endpoint, match_id)
            payload = {
                "properties":{
                    "Home Score":{
                        "number": home_score
                    },
                    "Away Score":{
                        "number": away_score
                    },
                    "Played?":{
                        "checkbox": True
                    }
                }
            }

            if home_score > away_score:
                payload["properties"]["Winner"] = {"relation": [{"id": home_team_id}]}
                payload["properties"]["Looser"] = {"relation": [{"id": away_team_id}]}
            elif home_score < away_score:
                payload["properties"]["Winner"] = {"relation": [{"id": away_team_id}]}
                payload["properties"]["Looser"] = {"relation": [{"id": home_team_id}]}
            else:
                payload["properties"]["Draw H"] = {"relation": [{"id": home_team_id}]}
                payload["properties"]["Draw A"] = {"relation": [{"id": away_team_id}]}
            
            Utils.update(url, payload)
