import sys; sys.path.append("./")

import datetime
from tqdm import tqdm

from src.create.match import Match
from src.calendars.crawlers import Crawler
from src.utils import Utils




class BundesligaCalendar(Crawler):
    league_name  = "Bundesliga"
    calendar_url = "https://www.bundesliga.com/en/bundesliga/matchday/2023-2024/"
    tags         = {
        "match_tag":     "div.matchRow",
        "time_tag":      "match-date-header",
        "date_tag":      "match-date-header span:nth-child(1)",
        "hour_tag":      "match-date-header span:nth-child(2)",
        "home_team_tag": "match-team:nth-of-type(1)",
        "away_team_tag": "match-team:nth-of-type(2)"
    }
    
    def __str__(self) -> None:
        return "<Calendar league='{}'>".format(self.league_name)
    
    def __init__(self) -> None:
        super().__init__()
        self.league_id = Utils.get_id(self.league_name)
        print(self)
        self.get_season_fixtures()
        # print("Number of matches: {}".format(self.count))
        
    def get_previous(self, soup, name):
        return soup.find_previous_siblings(name)[0]

    
    def get_fixtures(self, gameweek: int) -> None:
        matchday = "GW {}".format(gameweek)
        url = self.calendar_url+str(gameweek)
        soup = Utils.get_soup(url)
        for row in self.get_elements(soup, self.tags["match_tag"]):
            home_team = self.get_element(row, self.tags["home_team_tag"]).get_text()
            away_team = self.get_element(row, self.tags["away_team_tag"]).get_text()
            match_details = self.get_previous(row, self.tags["time_tag"])
            match_date = self.get_element(match_details, self.tags["date_tag"])
            match_hour = self.get_element(match_details, self.tags["hour_tag"])
            
            try: match_date = match_date.get_text()
            except:
                match_date = [date for date in match_details.get_text().split(" ") if len(date)>1]
                match_date, second_match_date = match_date
                matchday += " optional date: {}".format(second_match_date)
                
            
            # Process
            match_date = [item for item in match_date.split(" ") if len(item)>0][-1]
            match_date = datetime.datetime.strptime(match_date, "%d-%b-%Y")
            if match_hour is not None:
                match_time = match_hour.get_text().split(":")
                match_date =match_date.replace(hour=int(match_time[0]), minute=int(match_time[1]))
                match_date = match_date.strftime("%Y-%m-%d %H:%M")
            else: match_date = match_date.strftime("%Y-%m-%d %H:%M")
            
            
            Match(
                league     = self.league_name,
                matchday   = matchday,
                match_date = match_date,
                home_team  = home_team,
                away_team  = away_team,
                post       = False
            )
            
    
    def get_season_fixtures(self) -> None:
        for gameweek in tqdm(range(1,35)):
            self.get_fixtures(gameweek=gameweek)