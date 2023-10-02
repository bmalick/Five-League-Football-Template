import os, unidecode, datetime, json
from dotenv import load_dotenv
from match import Match
from crawlers import Crawler


class LaLigaCalendar(Crawler):
    league_name  = "La Liga"
    calendar_url = "https://www.laliga.com/en-FR/laliga-easports/results/2023-24/gameweek-"
    tags         = {
        "match_tag":  "table > tbody > tr:nth-child(3n+1)",
        "date_tag":   "td:nth-child(2)",
        "hour_tag":   "td:nth-child(3)",
        "teams_tag":  "td:nth-child(5) a",
    }
    
    def __init__(self) -> None:
        super().__init__()
        self.get_league_id()
        print(self)
        self.get_season_fixtures()
    
    def __str__(self) -> None:
        return "<Calendar league='{}'>".format(self.league_name)
    
    def get_league_id(self):
        load_dotenv()
        self.league_id = os.getenv(unidecode.unidecode(self.league_name.replace(" ", "").lower()))

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
        self.get_league_id()
        print(self)
        self.get_season_fixtures()
        # print("Number of matches: {}".format(self.count))
        
    def get_league_id(self):
        load_dotenv()
        self.league_id = os.getenv(unidecode.unidecode(self.league_name.replace(" ", "").lower()))
    
    def get_previous(self, soup, name):
        return soup.find_previous_siblings(name)[0]

    
    def get_fixtures(self, gameweek: int) -> None:
        matchday = "GM {}".format(gameweek)
        url = self.calendar_url+str(gameweek)
        soup = self.get_soup(url)
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
                league_db_id = self.league_id,
                matchday     = matchday,
                match_date   = match_date,
                home_team    = home_team,
                away_team    = away_team,
                POST=False
            )
            
    
    def get_season_fixtures(self) -> None:
        for gameweek in range(1,35):
            self.get_fixtures(gameweek=gameweek)

    

class Ligue1Calendar(Crawler):
    league_name  = "Ligue 1"
    calendar_url = "https://www.ligue1.com/fixtures-results?matchDay="
    tags         = {
        "match_day_tag": "div.calendar-widget-day",
        "match_tag": "li.match-result",
        "home_team_tag": "span.calendarTeamNameDesktop",
        "hour_tag": "span > span.lost"
    }
    
    def __str__(self) -> None:
        return "<Calendar league='{}'>".format(self.league_name)
    
    def __init__(self) -> None:
        super().__init__()
        self.get_league_id()
        print(self)
        self.count = 0
        self.get_season_fixtures()
        
    def get_league_id(self):
        load_dotenv()
        self.league_id = os.getenv(unidecode.unidecode(self.league_name.replace(" ", "").lower()))


    
    def get_fixtures(self, gameweek: int) -> None:
        matchday = "GM {}".format(gameweek)
        url = self.calendar_url+str(gameweek)
        soup = self.get_soup(url)
        for day in self.get_elements(soup, self.tags["match_day_tag"]):
            match_date = day.text.strip()
            match_date = " ".join([item for item in match_date.split(" ")[1:]])
            match_date = datetime.datetime.strptime(match_date, "%d %B %Y")
            matches = day.find_next('ul').select('li.match-result')
            
           
            for match in matches:
                home_team = self.get_element(match, self.tags["home_team_tag"]).text.strip()
                away_team = self.get_elements(match, self.tags["home_team_tag"])[-1].text.strip()
                match_hour = self.get_element(match, self.tags["hour_tag"]).text
                    

                
            
            # Process
            if len(match_hour)>1 and match_hour!="--:--":
                match_time = match_hour.split(":")
                match_date =match_date.replace(hour=int(match_time[0]), minute=int(match_time[1]))
                match_date = match_date.strftime("%Y-%m-%d %H:%M")
            else: match_date = match_date.strftime("%Y-%m-%d %H:%M")
            
            
            Match(
                league_db_id = self.league_id,
                matchday     = matchday,
                match_date   = match_date,
                home_team    = home_team,
                away_team    = away_team,
                POST=False
            )
            self.count+=1
            
    
    def get_season_fixtures(self) -> None:
        for gameweek in range(1,35):
            self.get_fixtures(gameweek=gameweek)





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








class SerieACalendar(Crawler):
    league_name  = "Serie A"
    
    short_names  = {"Naples": "Napoli","Hellas":"Hellas Verona","Rome":"Roma","Bologne":"Bologna","Inter Milan":"Milan"}
    french_to_english = {
        "janvier": "January",
        "février": "February",
        "mars": "March",
        "avril": "April",
        "mai": "May",
        "juin": "June",
        "juillet": "July",
        "août": "August",
        "septembre": "September",
        "octobre": "October",
        "novembre": "November",
        "décembre": "December"
    }
    
    tags         = {
        "match_tag": "div.blockVertical__content",
        "match_date": "p.title__left",
        "match_hour": "div.matchFull a time",
        "team_tag": "div.matchFull a span.matchTeam__name",
        "date_tag": "div.blockVertical"
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

    
    def get_fixtures(self, gameweek: int, calendar_url: str) -> None:
        matchday = "GM {}".format(gameweek)
        soup = self.get_soup(calendar_url)
        
        for row in self.get_elements(soup, self.tags["date_tag"]):
            match_date = self.get_element(row, self.tags["match_date"]).text
            match_date = match_date.split()[1:]
            match_date[1] = self.french_to_english[match_date[1]]
            match_date = " ".join(match_date)
            match_date = datetime.datetime.strptime(match_date, "%d %B %Y")
            
            
            for sub_row in self.get_elements(row,self.tags["match_tag"]):
                home_team = self.get_element(sub_row,self.tags["team_tag"]).text
                away_team = self.get_elements(sub_row,self.tags["team_tag"])[-1].text
                if home_team in self.short_names: home_team = self.short_names[home_team]
                if away_team in self.short_names: away_team = self.short_names[away_team]
                
                match_hour = self.get_element(sub_row,self.tags["match_hour"]).text.split("\n")
                match_hour = [item for item in match_hour if len(item)>0][0].strip()
         
                match_time = match_hour.split(":")
                final_match_date = match_date.replace(hour=int(match_time[0]), minute=int(match_time[1]))
                final_match_date = final_match_date.strftime("%Y-%m-%d %H:%M")
  
                Match(
                    league_db_id = self.league_id,
                    matchday     = matchday,
                    match_date   = final_match_date,
                    home_team    = home_team,
                    away_team    = away_team,
                    # POST=False
                )
                self.count+=1
        
    def get_season_fixtures(self) -> None:
        with open("./data/seriea_calendar.json") as file:
            urls = json.load(file)
        for gameweek in range(1,39):
            self.get_fixtures(gameweek=gameweek, calendar_url=urls[str(gameweek)])
            
            