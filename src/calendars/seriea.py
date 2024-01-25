import sys; sys.path.append("./")

import datetime
from tqdm import tqdm

from src.create.match import Match
from src.calendars.crawlers import Crawler
from src.calendars.scores import UpdateScore
from src.utils import Utils




# class SerieACalendar(Crawler):
#     league_name  = "Serie A"
    
#     short_names  = {"Naples": "Napoli","Hellas":"Hellas Verona","Rome":"Roma","Bologne":"Bologna","Inter Milan":"Milan"}
#     french_to_english = {
#         "janvier": "January",
#         "février": "February",
#         "mars": "March",
#         "avril": "April",
#         "mai": "May",
#         "juin": "June",
#         "juillet": "July",
#         "août": "August",
#         "septembre": "September",
#         "octobre": "October",
#         "novembre": "November",
#         "décembre": "December"
#     }
    
#     tags         = {
#         "match_tag": "div.blockVertical__content",
#         "match_date": "p.title__left",
#         "match_hour": "div.matchFull a time",
#         "team_tag": "div.matchFull a span.matchTeam__name",
#         "date_tag": "div.blockVertical"
#     }
    
#     def __str__(self) -> None:
#         return "<Calendar league='{}'>".format(self.league_name)
    
#     def __init__(self) -> None:
#         super().__init__()
#         self.league_id = Utils.get_id(self.league_name)
#         print(self)
#         self.count = 0
#         self.get_season_fixtures()
#         print();print("Total matches: {}".format(self.count))
        
        
#     def get_league_id(self):
#         load_dotenv()
#         self.league_id = os.getenv(unidecode.unidecode(self.league_name.replace(" ", "").lower()))

    
#     def get_fixtures(self, gameweek: int, calendar_url: str) -> None:
#         matchday = "GW {}".format(gameweek)
#         soup = Utils.get_soup(calendar_url)
        
#         for row in self.get_elements(soup, self.tags["date_tag"]):
#             match_date = self.get_element(row, self.tags["match_date"]).text
#             match_date = match_date.split()[1:]
#             match_date[1] = self.french_to_english[match_date[1]]
#             match_date = " ".join(match_date)
#             match_date = datetime.datetime.strptime(match_date, "%d %B %Y")
            
            
#             for sub_row in self.get_elements(row,self.tags["match_tag"]):
#                 home_team = self.get_element(sub_row,self.tags["team_tag"]).text
#                 away_team = self.get_elements(sub_row,self.tags["team_tag"])[-1].text
#                 if home_team in self.short_names: home_team = self.short_names[home_team]
#                 if away_team in self.short_names: away_team = self.short_names[away_team]
                
#                 match_hour = self.get_element(sub_row,self.tags["match_hour"]).text.split("\n")
#                 match_hour = [item for item in match_hour if len(item)>0][0].strip()
         
#                 match_time = match_hour.split(":")
#                 final_match_date = match_date.replace(hour=int(match_time[0]), minute=int(match_time[1]))
#                 final_match_date = final_match_date.strftime("%Y-%m-%d %H:%M")
  
#                 Match(
#                     league_db_id = self.league_id,
#                     matchday     = matchday,
#                     match_date   = final_match_date,
#                     home_team    = home_team,
#                     away_team    = away_team,
#                     # POST=False
#                 )
#                 self.count+=1
        
#     def get_season_fixtures(self) -> None:
#         with open("./data/seriea_calendar.json") as file:
#             urls = json.load(file)
#         for gameweek in range(1,39):
#             self.get_fixtures(gameweek=gameweek, calendar_url=urls[str(gameweek)])
            
            