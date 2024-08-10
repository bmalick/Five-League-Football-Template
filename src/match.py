import requests, unidecode, datetime
from src.base import Base
from src.utils import read_yaml, save_yaml
from src.notion import NotionApiHandler, NotionObject
# todo: make a table for properties in datasate of hw i canll it
class Match(Base):
    def __init__(self, league: str, match_date: str,
            home_team: str, away_team: str, week: int = None,
            time_zone: str = "Europe/Paris") -> None:
        super().__init__()
        # id_name = self.get_id_name(name)
        if match_date is not None:
            start_date = match_date
            end_date = datetime.datetime.strptime(match_date, "%Y-%m-%d %H:%M")
            end_date += datetime.timedelta(minutes=90)
            end_date = end_date.strftime("%Y-%m-%d %H:%M")
        else:
            start_date = None
            end_date = None
            
        self.save_parameters(
            league=league, start_date=start_date, end_date=end_date, time_zone=time_zone,
            home_team=home_team, away_team=away_team, week=week,
            start_date_str = start_date if start_date is not None else "%sNone%s" % (' '*6, ' '*6),
            api_handler=NotionApiHandler())
        
    def __str__(self):
        return "%s%s [%s] %s" % (''.ljust(21), self.home_team.rjust(25), self.start_date_str.rjust(16), self.away_team)


    def create(self):
        # if self.exists(): return
        # properties = [
        #     {"name": "Name", "type": "page_title", "values": {"title": "[%s] - [%s]" % (self.home_team, self.away_team)}},
        #     {"name": "gw", "type": "number", "values": {"number": self.week}},
        #     {"name": "league", "type": "relation", "values": {"id": self.api_handler.keys["league_ids"][self.get_id_name(self.league)]}},
        #     {"name": "home team", "type": "relation", "values": {"id": self.api_handler.keys["team_ids"][self.get_id_name(self.home_team)]}},
        #     {"name": "away team", "type": "relation", "values": {"id": self.api_handler.keys["team_ids"][self.get_id_name(self.away_team)]}},
        # ]
        # if self.start_date is not None:
        #     properties.append({"name": "date", "type": "date", "values": {
        #         "start": self.start_date, "end": self.end_date, "time_zone": self.time_zone}})
        # data = self.api_handler.create_page_in_database(
        #     database_id=self.api_handler.keys["matches_db_token"],
        #     data={
        #         "icon": {"url": "https://www.notion.so/icons/playback-play_gray.svg"},
        #         "properties": properties,
        #         # todo: add blocks for your reaction, top, flops, thoughts
        #         # "children": []
        #     }
        # )
        # print(self)
        self.update()

    
    def find_match(self):
        fixture = self.api_handler.query_database(
            database_id=self.api_handler.keys["matches_db_token"],
            filters={
                "and": [
                    {"property": "Name",
                     "rich_text": {"equals": "[%s] - [%s]" % (self.home_team, self.away_team)}},
                     {"property": "gw",
                      "number": {"equals": self.week}}
                ]
            }
        )
        return fixture
    
    def exists(self):
        fixture = self.find_match()
        return len(fixture)>0
    
    def update(self):
        fixture = self.find_match()[0]        
        if fixture["properties"]["date"]["date"] == None:
            page_id = fixture["id"]
            response = requests.patch(
                url=self.api_handler._pages_endpoint + f"/{page_id}",
                headers=self.api_handler.headers,
                json={
                    "properties": {
                        "date": NotionObject("date")({"start": self.start_date})
                    }
                }
            )
            try:
                response.raise_for_status()
            except: print(response.text)
