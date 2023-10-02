import os, unidecode, datetime, requests, json
from dotenv import load_dotenv
from match import Match
from crawlers import Crawler


class UpdatesLaLiga(Crawler):
    league_name  = "La Liga"
    calendar_url = "https://www.laliga.com/en-FR/laliga-easports/results/2023-24/gameweek-"
    tags         = {
        "match_tag":  "table > tbody > tr:nth-child(3n+1)",
        "date_tag":   "td:nth-child(2)",
        "hour_tag":   "td:nth-child(3)",
        "teams_tag":  "td:nth-child(5) a",
    }
    NOTION_ENDPOINT = "https://api.notion.com/v1/"
    
    def __init__(self) -> None:
        super().__init__()
        self.load_headers()
        self.get_league_id()
        print(self)
        # self.get_season_fixtures()
    
    def __str__(self) -> None:
        return "<Calendar league='{}'>".format(self.league_name)
    
    def load_headers(self) -> None:
        load_dotenv()
        self.NOTION_API_KEY = os.getenv("NOTION_API_KEY")
        self.headers = {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
            "Authorization": "Bearer " + self.NOTION_API_KEY 
        }
    
    def get_league_id(self):
        load_dotenv()
        self.MATCHES_DB_ID  = os.getenv("MATCHES_DB_ID")
        


        self.league_id = os.getenv(unidecode.unidecode(self.league_name.replace(" ", "").lower()))
        fixtures = requests.get(self.NOTION_ENDPOINT+"databases/"+self.MATCHES_DB_ID+"/query", headers=self.headers).json()
        print(fixtures)

    def get_fixtures(self, gameweek: int) -> None:
        matchday = "GM {}".format(gameweek)
        url = self.calendar_url+str(gameweek)
        soup = self.get_soup(url)
        for row in self.get_elements(soup, self.tags["match_tag"]):
            match_date  = self.get_element(row, self.tags["date_tag"])
            match_hour  = self.get_element(row, self.tags["hour_tag"])
            home_team = self.get_elements(row, self.tags["teams_tag"])[0].text.strip()
            away_team = self.get_elements(row, self.tags["teams_tag"])[1].text.strip()
            
            
            # Process
            match_date = match_date.get_text().split(" ")[-1]
            match_date = datetime.datetime.strptime(match_date, "%d.%m.%Y")
            match_hour = match_hour.text
            
            if match_hour != "-- : --":
                match_time = match_hour.split(":")
                match_date=match_date.replace(hour=int(match_time[0])+2, minute=int(match_time[1]))
                match_date = match_date.strftime("%Y-%m-%d %H:%M")

                Match(
                league_db_id = self.league_id,
                matchday     = matchday,
                match_date   = match_date,
                home_team    = home_team,
                away_team    = away_team,
                POST=False
            )
                
            else: match_date = match_date.strftime("%Y-%m-%d %H:%M"); print("Programme is not ready"); continue
            

            
    
    def get_season_fixtures(self) -> None:
        for gameweek in range(8,39):
            self.get_fixtures(gameweek=gameweek)

UpdatesLaLiga()





class PremierLeagueCalendar(Crawler):
    league_name  = "Premier League"
    calendar_url = "https://www.premierleague.com/matchweek/"
    base_url     = "https://www.premierleague.com/"
    label        = 12268
    
    short_names  = {
        "MUN": "Manchester United",
        "WOL": "Wolverhampton Wanderers",
        "CHE": "Chelsea",
        "LIV": "Liverpool",
        "BRE": "Brentford",
        "TOT": "Tottenham Hotspur",
        "NEW": "Newcastle United",
        "AVL": "Aston Villa",
        "BOU": "Bournemouth",
        "WHU": "West Ham United",
        "BHA": "Brighton & Hove Albion",
        "LUT": "Luton Town",
        "EVE": "Everton",
        "SHU": "Sheffield United",
        "ARS": "Arsenal",
        "FUL": "Fulham",
        "CRY": "Crystal Palace",
        "NFO": "Nottingham Forest",
        "BUR": "Burnelay",
        "MCI": "Manchester City"
    }
    
    tags         = {
        "match_tag": "div.fixedSidebar.u-hide-tab > div.fixtures-abridged a",
        "home_team_tag": "div.home",
        "away_team_tag": "div.away",
        "date_tag": "div.mc-summary__info",
        "timestamp_tag": "div.mc-summary__score-container.upcoming > div",
        "score": "div.mc-summary__score"
    }
    
    def __str__(self) -> None:
        return "<Calendar league='{}'>".format(self.league_name)
    
    def __init__(self) -> None:
        super().__init__()
        self.get_league_id()
        print(self)
        self.count = 0
        self.get_season_fixtures()
        print();print("Total matches: {}".format(self.count))
        
        
    def get_league_id(self):
        load_dotenv()
        self.league_id = os.getenv(unidecode.unidecode(self.league_name.replace(" ", "").lower()))


    
    def get_fixtures(self, gameweek: int) -> None:
        matchday = "GM {}".format(gameweek)
        url = self.calendar_url+str(gameweek+self.label)+"/blog?match=true"
        soup = self.get_soup(url)
        
        for link in self.get_elements(soup, self.tags["match_tag"]):
            try:
                match_soup = self.get_soup(self.base_url+link.attrs["href"])
                # print(match_soup)
                home_team  = self.get_element(match_soup, self.tags["home_team_tag"]).text.split("\n")
                home_team  = [item for item in home_team if len(item)>1][-1]
                
                home_team  = self.short_names[home_team]
                away_team  = self.get_element(match_soup, self.tags["away_team_tag"]).text.split("\n")
                away_team = [item for item in away_team if len(item)>1][-1]
                away_team  = self.short_names[away_team]
                
                try:
                    match_date = self.get_element(match_soup, self.tags["date_tag"]).text.strip()
                    match_date = " ".join(match_date.split(" ")[1:])
                    match_date = datetime.datetime.strptime(match_date, "%d %b %Y")
                    home_score, away_score = self.get_element(match_soup, self.tags["score"]).text.split("-")
                    
                except:
                    match_date = self.get_element(match_soup, self.tags["timestamp_tag"]).attrs["data-kickoff"]
                    match_date = match_date[:-3]
                    match_date = datetime.datetime.fromtimestamp(int(match_date))
                    
                    Match(
                        league_db_id = self.league_id,
                        matchday     = matchday,
                        match_date   = match_date,
                        home_team    = home_team,
                        away_team    = away_team,
                        POST=False
                    )
                    self.count+=1
                    
            except: continue
        
    def get_season_fixtures(self) -> None:
        for gameweek in range(6,39):
            self.get_fixtures(gameweek=gameweek)






