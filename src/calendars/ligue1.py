import sys; sys.path.append("./src")
import datetime
from create.match import Match
from calendars.crawlers import Crawler
from utils import Utils
from calendars.scores import UpdateScore
    

class Ligue1Calendar(Crawler):
    league_name  = "Ligue 1"
    calendar_url = "https://www.ligue1.com/fixtures-results?matchDay="
    base_url = "https://www.ligue1.com/"
    tags         = {
        "match_tag": "a.js-Calendar-matchLink",
        "match_date_tag": "p.MatchHeader-text",
        "home_team_tag": "div.home h2.MatchHeader-clubName",
        "away_team_tag": "div.away h2.MatchHeader-clubName",
        "score_tag":"p.MatchHeader-scoreResult"
    }

    sep = '+' + '-'*58 + "+\n"

    short_names  = {
        "OGC NICE": "OGC NICE",
        "LOSC": "LOSC LILLE",
        "OM": "OLYMPIQUE DE MARSEILLE",
        "REIMS": "STADE DE REIMS",
        "PSG":"PARIS SAINT-GERMAIN",
        "FC LORIENT":"FC LORIENT",
        "BREST":"STADE BRESTOIS 29",
        "RC LENS":"RC LENS",
        "CLERMONT":"CLERMONT FOOT 63",
        "AS MONACO":"AS MONACO",
        "MONTPELLIER":"MONTPELLIER HÉRAULT SC",
        "HAVRE AC":"HAVRE AC",
        "FC NANTES":"FC NANTES",
        "TOULOUSE FC":"TOULOUSE FC",
        "RENNES":"STADE RENNAIS FC",
        "FC METZ":"FC METZ",
        "STRASBOURG":"RC STRASBOURG ALSACE",
        "OL":"OLYMPIQUE LYONNAIS",

    
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
        url = cls.calendar_url+str(gameweek)
        soup = Utils.get_soup(url)
        for row in cls.get_elements(soup, cls.tags["match_tag"]):
            if "href" in row.attrs:
                match_soup = Utils.get_soup(cls.base_url+row.attrs["href"])
                try:
                    match_date, match_hour = cls.get_element(match_soup, cls.tags["match_date_tag"]).text.strip().split('-')
                    match_date = list(map(lambda x:x.strip(), (match_date,match_hour)))

                    match_date = ' '.join(match_date)
                    match_date = datetime.datetime.strptime(match_date, "%a %d %B %Y %H:%M")
                    match_date_fmt = match_date.strftime("%Y-%m-%d")
                    match_date = match_date.strftime("%Y-%m-%d %H:%M")

                    home_team = cls.get_element(match_soup, cls.tags["home_team_tag"]).text.strip()
                    away_team = cls.get_element(match_soup, cls.tags["away_team_tag"]).text.strip()
                    home_team, away_team = list(map(lambda x:cls.short_names[x], (home_team, away_team)))
                        
                    if not UpdateScore.match_exists(match_date_fmt, home_team, away_team):
                        
                        Match(
                            league     = cls.league_name,
                            matchday   = matchday,
                            match_date = match_date,
                            home_team  = home_team,
                            away_team  = away_team,
                            post       = True
                        )
                    else: print("%s vs %s fixture is already planned on %s" % (home_team, away_team, match_date))
                except: pass
                
    
    def get_season_fixtures(self) -> None:
        for gameweek in range(1, 35):
            self.get_fixtures(gameweek=gameweek)

    @classmethod
    def update_scores(cls, gameweek: int) -> None:
        url = cls.calendar_url+str(gameweek)
        soup = Utils.get_soup(url)

        resume = cls.sep

        for row in cls.get_elements(soup, cls.tags["match_tag"]):
            match_soup = Utils.get_soup(cls.base_url+row.attrs["href"])
            match_date, match_hour = cls.get_element(match_soup, cls.tags["match_date_tag"]).text.strip().split('-')
            match_date = list(map(lambda x:x.strip(), (match_date,match_hour)))

            match_date = ' '.join(match_date)
            match_date = datetime.datetime.strptime(match_date, "%a %d %B %Y %H:%M")
            match_date = match_date.strftime("%Y-%m-%d %H:%M")

            home_team = cls.get_element(match_soup, cls.tags["home_team_tag"]).text.strip()
            away_team = cls.get_element(match_soup, cls.tags["away_team_tag"]).text.strip()
            home_team, away_team = list(map(lambda x:cls.short_names[x], (home_team, away_team)))

            score = cls.get_element(match_soup, cls.tags["score_tag"]).text.split('-')
            try:
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