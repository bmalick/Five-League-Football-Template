import sys; sys.path.append("./")

import datetime
from tqdm import tqdm

from src.create.match import Match
from src.calendars.crawlers import Crawler
from src.calendars.scores import UpdateScore
from src.utils import Utils


class LaLigaCalendar(Crawler):
    league_name  = "La Liga"
    calendar_url = "https://www.laliga.com/en-FR/laliga-easports/results/2023-24/gameweek-"
    tags         = {
        "match_tag":  "table > tbody > tr:nth-child(3n+1)",
        "date_tag":   "td:nth-child(2)",
        "hour_tag":   "td:nth-child(3)",
        "teams_tag":  "td:nth-child(5) a",
        "score_tag": ".live"
    }

    sep = '+' + '-'*58 + "+\n"

    def __init__(self) -> None:
        super().__init__()
        self.league_id = Utils.get_id(self.league_name)
        print(self)
        self.get_season_fixtures()
    
    def __str__(self) -> None:
        return "<Calendar league='{}'>".format(self.league_name)


    @classmethod
    def get_fixtures(cls, gameweek: int) -> None:
        matchday = "GW {}".format(gameweek)
        url = cls.calendar_url+str(gameweek)
        soup = Utils.get_soup(url)
        for row in cls.get_elements(soup, cls.tags["match_tag"]):
            match_date = cls.get_element(row, cls.tags["date_tag"])
            match_hour = cls.get_element(row, cls.tags["hour_tag"])
            home_team  = cls.get_elements(row, cls.tags["teams_tag"])[0].text.strip()
            away_team  = cls.get_elements(row, cls.tags["teams_tag"])[1].text.strip()
            
            
            # Process
            match_date = match_date.get_text().split(" ")[-1]
            match_date = datetime.datetime.strptime(match_date, "%d.%m.%Y")
            match_hour = match_hour.text
            
            if match_hour != "-- : --":
                match_time = match_hour.split(":")
                match_date=match_date.replace(hour=int(match_time[0])+2, minute=int(match_time[1]))
                match_date_fmt = match_date.strftime("%Y-%m-%d")
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
                
            else: match_date = match_date.strftime("%Y-%m-%d %H:%M"); print("Programme is not ready"); continue
    
    def get_season_fixtures(self) -> None:
        for gameweek in tqdm(range(1,39)):
            self.get_fixtures(gameweek=gameweek)
    
    @classmethod
    def update_scores(cls, gameweek: int) -> None:
        url = cls.calendar_url+str(gameweek)
        soup = Utils.get_soup(url)

        resume = cls.sep
        resume += ("| %s - Gameweek %d" % (cls.league_name, gameweek)).ljust(59) + "|\n"
        resume += cls.sep

        for row in tqdm(cls.get_elements(soup=soup, selector=cls.tags["match_tag"])):
            home_team = cls.get_elements(row, cls.tags["teams_tag"])[0].text.strip()
            away_team = cls.get_elements(row, cls.tags["teams_tag"])[1].text.strip()

            match_date  = cls.get_element(soup=row, selector=cls.tags["date_tag"])
            match_date = match_date.get_text().split(" ")[-1]
            match_date = datetime.datetime.strptime(match_date, "%d.%m.%Y")
            match_date = match_date.strftime("%Y-%m-%d")
            
            score = cls.get_element(row, cls.tags["score_tag"]).text.split('-')
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

