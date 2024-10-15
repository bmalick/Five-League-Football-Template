import re, datetime
# from src.create.payloads import LeaguePayload
from src.base import Base
# from src.create.payloads import LeaguePost
from abc import ABC, abstractmethod
from src.team import Team
from src.match import Match
import concurrent.futures
from src.utils import read_yaml, save_yaml
from src.notion import NotionApiHandler

# todo: write a croontab that will update all matches that do not have hour 

class BaseLeague(ABC, Base):
    
    def __init__(self, name: str, url: str, logo: str,
                 calendar_url: str, teams_url: str, num_gameweeks: int) -> None:
        super().__init__()
        id_name = self.get_id_name(name)

        self.save_parameters(name=name, url=url, logo=logo,
                             calendar_url=calendar_url,
                             teams_url=teams_url,
                             num_gameweeks=num_gameweeks,
                             id_name=id_name, api_handler=NotionApiHandler())
    
    def __str__(self) -> str:
        return "<'{}'>".format(self.name)

    def create(self) -> None:
        if self.exists(): return
        data = self.api_handler.create_page_in_database(
            database_id=self.api_handler.keys["leagues_db_token"],
            data={
                "icon": {"url": self.logo},
                "cover": {"url": self.logo},
                "properties": [
                    {"name": "Name", "type": "page_title", "values": {"title": self.name}},
                    {"name": "Url", "type": "url", "values": {"url": self.url}},
                ],
                # todo: add calendars for leagues in the children, add teams
                # "children": [

                # ]
            }
        )
        page_id = data["id"]
        self.add_id(page_id)
        print(f"[{self.name}] is created")
    
    def add_id(self, page_id):
        ids = read_yaml("keys.yaml")
        if not "league_ids" in ids:
            ids["league_ids"] = {}
        ids["league_ids"][self.id_name] = page_id
        save_yaml("keys.yaml", ids)
        
    def exists(self) -> bool:
        leagues = self.api_handler.query_database(
            database_id=self.api_handler.keys["leagues_db_token"],
            filters={
                "or": [
                    {
                        "property": "Name",
                        "rich_text": {"equals": self.name}
                    }
                ]
            } 
        )
        return len(leagues)>0
    
    def get_teams(self):
        teams = self.get_teams_soup()
        futures = []
        team_ids = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for team in teams:
                futures.append(executor.submit(self.get_team, team))
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res is not None:
                    id_name, team_id = res
                    team_ids[id_name] = team_id
        
        ids = read_yaml("keys.yaml")
        if not "team_ids" in ids:
            ids["team_ids"] = {}
        ids["team_ids"].update(team_ids)
        save_yaml("keys.yaml", ids)
    
    # def delete_all_fixtures():
    #     api_handler = NotionApiHandler()
    #     def get_fixtures():
    #         return api_handler.query_database(
    #                 database_id=api_handler.keys["fixtures_db_token"],
    #                 limit=100
    #             )
    #     while True:
    #         fixtures = get_fixtures()
    #         if len(fixtures)==0: break
    #         futures = []
    #         with concurrent.futures.ThreadPoolExecutor() as executor:
    #             for fixture in fixtures:
    #                 futures.append(executor.submit(api_handler.delete_page, fixture["id"]))
    #             for future in concurrent.futures.as_completed(futures):
    #                 future.result()

    # def update_gameweek(self, week: int):
    #     # fixtures = self.get_gameweek(week)
    #     fixtures = self.api_handler.query_database(
    #         database_id=self.api_handler.keys["matches_db_token"],
    #         filters={
    #             "and": [
    #                 {"property": "Name",
    #                  "rich_text": {"equals": "[%s] - [%s]" % (self.home_team, self.away_team)}},
    #                  {"property": "gw",
    #                   "number": {"equals": self.week}}
    #             ]
    #         }
    #     )
    #     return len(fixtures)>0

    def get_calendar(self):
        calendar = []
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for week in range(1, self.num_gameweeks+1):
                futures.append(executor.submit(self.get_gameweek, week))
            for future in concurrent.futures.as_completed(futures):
                calendar.extend(future.result())
                
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for fixture in calendar:
                futures.append(executor.submit(fixture.create))
            for future in concurrent.futures.as_completed(futures):
                future.result()

    @abstractmethod
    def get_teams_soup(self): pass

    @abstractmethod
    def get_team(self, item): pass

    @abstractmethod
    def get_gameweek(self, week: int): pass


class LaLiga(BaseLeague):
    def __init__(self, name: str, url: str, logo: str, calendar_url: str, teams_url: str, num_gameweeks: int) -> None:
        super().__init__(name, url, logo, calendar_url, teams_url, num_gameweeks)

    def get_teams_soup(self):
        soup = self.get_soup(self.teams_url)
        return soup.find_all(name="a", attrs={"href": re.compile("/en-FR/clubs/.*")})    

    def get_team(self, item) -> tuple[str, str]:
        team_name = self.get_item(item, "h2")
        page_team_url = item.attrs["href"]
        team_soup = self.get_soup(self.url + page_team_url)
        parent_div = team_soup.find(name="h1").parent
        team_url = parent_div.select_one(selector="table > tbody > tr:nth-of-type(4) > td:nth-of-type(2) > a")
        team_url = team_url.attrs["href"]
        team_logo = parent_div.previous_sibling.find(name="img").attrs["src"]
        team = Team(league=self.name, name=team_name, url=team_url, logo=team_logo)
        if hasattr(team, "team_id"):
            return team.id_name, team.team_id
        return
    
    def get_gameweek(self, week: int):
        soup = self.get_soup(self.calendar_url % week)
        result = soup.select("tr:nth-child(3n+1)")
        matches = []
        for item in result:
            match_date = Base.get_item(item, "td:nth-of-type(2)").split()[-1]
            match_hour = Base.get_item(item, "td:nth-of-type(3)")
            home_team, away_team = Base.get_item(item, "td:nth-of-type(5)").split(" VS ")
            try:
                match_date = datetime.datetime.strptime(match_date, "%d.%m.%Y")
                match_hour = list(map(int, match_hour.split(':')))
                match_date = match_date.replace(hour=match_hour[0], minute=match_hour[1])
                match_date = match_date.strftime("%Y-%m-%d %H:%M")
            except: match_date = None
            
            matches.append(Match(
                league=self.name,
                match_date=match_date,
                home_team=home_team,
                away_team=away_team,
                week=week)
                # todo: use the right time_zone
            )
        return matches
            

class PremierLeague(BaseLeague):
    def __init__(self, name: str, url: str, logo: str, calendar_url: str, teams_url: str, num_gameweeks: int) -> None:
        super().__init__(name, url, logo, calendar_url, teams_url, num_gameweeks)

    def get_teams_soup(self):
        soup = self.get_soup(self.teams_url)
        return soup.find(name="ul", attrs={"class": "clubList"}).find_all(name="a", attrs={"class": "clubList__link"})

    def get_team(self, item):
        team_name = self.get_item(item, "span")
        team_url = item.attrs["href"].strip()
        team_logo = item.find(name="img").attrs["srcset"].split()[0]
        team = Team(league=self.name, name=team_name, url=team_url, logo=team_logo)
        if hasattr(team, "team_id"):
            return team.id_name, team.team_id
        return
        
    def get_gameweek(self, item): pass
    def get_calendar(self): pass

class Bundesliga(BaseLeague):
    def __init__(self, name: str, url: str, logo: str, calendar_url: str, teams_url: str, num_gameweeks: int) -> None:
        super().__init__(name, url, logo, calendar_url, teams_url, num_gameweeks)

    def get_teams_soup(self):
        soup = self.get_soup(self.teams_url)
        teams = soup.find(name="div", attrs={"class": "clubs"}).find_all(name="club-card")
        return teams

    def get_team(self, item):
        url = self.url + item.find(name="a").attrs["href"]
        # TODO: find a solution for this
        if url.endswith("sc-freiburg"):
            team_name = "SC Freiburg"
            team_logo = "https://www.bundesliga.com/assets/clublogo/DFL-CLU-00000A.svg"
            team_url = "https://www.scfreiburg.com/"
        else:
            soup = self.get_soup(url)
            team_name = self.get_item(soup, "h1")
            team_logo = self.url + soup.find(name="img", attrs={"class": "logo"}).attrs["src"]
            team_url = soup.select_one("div.linkBar > div.container > div.row > div:nth-of-type(2)").find(name="a").attrs["href"]
        team = Team(league=self.name, name=team_name, url=team_url, logo=team_logo)
        if hasattr(team, "team_id"):
            return team.id_name, team.team_id
        return

    def get_gameweek(self, item): pass
    def get_calendar(self): pass

class Ligue1(BaseLeague):
    def __init__(self, name: str, url: str, logo: str, calendar_url: str, teams_url: str, num_gameweeks: int) -> None:
        super().__init__(name, url, logo, calendar_url, teams_url, num_gameweeks)
    
    # def get_teams_soup(self):
    #     # TODO
    #     soup = self.get_soup(self.teams_url)
    #     teams = soup.find_all(name="a", attrs={"href": re.compile(r"^/club-sheet/")})
    #     return teams
    # def get_team(self, item):
    #     # print(item.get_text())
    #     team_name = itemy.find(name="div", attrs={"dir": "auto"}).get_text()
    #     # team_logo
    #     # team_url
    # def get_gameweek(self, item): pass
    # def get_calendar(self): pass


class SerieA(BaseLeague):
    def __init__(self, name: str, url: str, logo: str, calendar_url: str, teams_url: str, num_gameweeks: int) -> None:
        super().__init__(name, url, logo, calendar_url, teams_url, num_gameweeks)

    # def get_teams_soup(self):
    #     # TODO
    #     soup = self.get_soup(self.teams_url)
    #     teams = soup.find(name="div", attrs={"class": "tab-pane"})
    #     print(teams.get_text())

    # def get_team(self, item): pass
    # def get_gameweek(self, item): pass
    # def get_calendar(self): pass

class League:
    _objects = {
        "laliga": LaLiga,
        "premierleague": PremierLeague,
        "bundesliga": Bundesliga,
        "ligue1": Ligue1,
        "seriea": SerieA

    }
    def __new__(self, name: str, url: str, logo: str, calendar_url: str, teams_url: str, num_gameweeks: int) -> None:
        object_name = name.replace(' ', '').lower()
        return self._objects.get(object_name)(
            name=name,
            url=url,
            logo=logo,
            calendar_url=calendar_url,
            teams_url=teams_url,
            num_gameweeks=num_gameweeks
        )
        

one
two
three
