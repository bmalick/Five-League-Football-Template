import sys; sys.path.append("./")

import datetime
from tqdm import tqdm

from src.create.match import Match
from src.calendars.crawlers import Crawler
from src.calendars.scores import UpdateScore
from src.utils import Utils


class PremierLeagueCalendar(Crawler):
    league_name  = "Premier League"
    calendar_url = "https://www.premierleague.com/matchweek/"
    base_url     = "https://www.premierleague.com/"
    label        = 12268

    sep = '+' + '-'*58 + "+\n"
    
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
        "BUR": "Burnley",
        "MCI": "Manchester City"
    }
    
    tags = {
        "match_tag": "a.match-fixture",
        "home_team_tag": "div.match-fixture__team--home span",
        "away_team_tag": "div.match-fixture__team--away span",
        "date_tag": "div.mc-summary__info",
        "hour_tag": "div.mc-summary__info-kickoff span.renderKOContainer",
        "score_tag": "div.mc-summary__score"
    }
    
    def __str__(self) -> None:
        return "<Calendar league='{}'>".format(self.league_name)
    
    def __init__(self) -> None:
        super().__init__()
        self.league_id = Utils.get_id(self.league_name)
        print(self)
        self.get_season_fixtures()
    
    @classmethod
    def get_fixtures(cls, gameweek: int) -> None:
        matchday = "GW {}".format(gameweek)
        url = cls.calendar_url+str(gameweek+cls.label)+"/blog?match=true"
        soup = Utils.get_soup(url)
        
        for row in cls.get_elements(soup, cls.tags["match_tag"]):
            
            home_team  = cls.get_element(row, cls.tags["home_team_tag"]).text
            away_team  = cls.get_element(row, cls.tags["away_team_tag"]).text
                    
            home_team  = cls.short_names[home_team]
            away_team  = cls.short_names[away_team]

            try:
                match_soup = Utils.get_soup(cls.base_url+row.attrs["href"])
                match_date = cls.get_element(match_soup, cls.tags["hour_tag"]).attrs["data-kickoff"]
                match_date = match_date[:-3]
                match_date = datetime.datetime.fromtimestamp(int(match_date))

                match_date_fmt =match_date.strftime("%Y-%m-%d")
                match_date = match_date.strftime("%Y-%m-%d %H:%M")

                if not UpdateScore.match_exists(match_date_fmt, home_team, away_team):
                        
                    Match(
                        league     = cls.league_name,
                        matchday   = matchday,
                        match_date = match_date,
                        home_team  = home_team,
                        away_team  = away_team,
                        post       = True
                    )
                else:
                    continue
                    # print("%s vs %s fixture is already planned on %s" % (home_team, away_team, match_date))
            except: pass
                
                
    def get_season_fixtures(self) -> None:
        for gameweek in tqdm(range(1,39)):
            self.get_fixtures(gameweek=gameweek)
    
    @classmethod
    def update_scores(cls, gameweek: int) -> None:
        url = cls.calendar_url+str(gameweek+cls.label)+"/blog?match=true"
        soup = Utils.get_soup(url)

        resume = cls.sep
        resume += ("| %s - Gameweek %d" % (cls.league_name, gameweek)).ljust(59) + "|\n"
        resume += cls.sep
        
        for row in tqdm(cls.get_elements(soup, cls.tags["match_tag"])):
            
            home_team  = cls.get_element(row, cls.tags["home_team_tag"]).text
            away_team  = cls.get_element(row, cls.tags["away_team_tag"]).text
                    
            home_team  = cls.short_names[home_team]
            away_team  = cls.short_names[away_team]

            try:
                match_soup = Utils.get_soup(cls.base_url+row.attrs["href"])
                match_date = cls.get_element(match_soup, cls.tags["hour_tag"]).attrs["data-kickoff"]
                match_date = match_date[:-3]
                match_date = datetime.datetime.fromtimestamp(int(match_date))

                match_date = match_date.strftime("%Y-%m-%d")
                score = cls.get_element(match_soup, cls.tags["score_tag"]).text.split('-')
                home_score, away_score = list(map(int, score))

                UpdateScore.update(
                    date=match_date,
                    home_team=home_team, away_team=away_team,
                    home_score=home_score, away_score=away_score
                )
                
                resume += "|%s | %d - %d | %s |\n" % (home_team.rjust(23), home_score, away_score, away_team.ljust(23))
                resume += cls.sep

            except: pass
        print(resume)

