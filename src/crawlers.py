import os, requests, unidecode, json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from bs4.element import Tag
from player import Player
from team import Team


class Crawler:
    def __init__(self) -> None:
        self.load_headers()
    
    def load_headers(self) -> None:
        load_dotenv()
        self.NOTION_API_KEY = os.getenv("NOTION_API_KEY")
        self.headers = {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
            "Authorization": "Bearer " + self.NOTION_API_KEY 
        }
    
    def get_soup(self, url: str):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, "html.parser")

    def get_element(self, soup: BeautifulSoup,  selector: str) -> Tag:
        child = soup.select_one(selector=selector)
        return child
    
    def get_elements(self, soup: BeautifulSoup,  selector: str) -> Tag:
        childs = soup.select(selector=selector)
        return childs




class LeagueCrawler(Crawler):
    def __init__(
        self, name: str, base_url: str, club_list_endpoint: str,
        club_list_tag: str, club_name_tag: str, website_tag: str,
        logo_tag: list[str]
        ) -> None:
        
        super().__init__()
        self.league_name        = name
        self.base_url           = base_url
        self.club_list_tag      = club_list_tag
        self.club_name_tag      = club_name_tag
        self.website_tag        = website_tag
        self.logo_tag           = logo_tag
        self.club_list_endpoint = club_list_endpoint
        self.get_league_id()
        print("-"*40)
        print(self)
        self.get_teams()
        print("-"*40)
    
    def __str__(self,):
        return "<LeagueCrawler name='{}'>".format(self.league_name)
    
        
    def get_league_id(self):
        load_dotenv()
        self.league_id = os.getenv(unidecode.unidecode(self.league_name.replace(" ", "").lower()))
    
    
    def get_team_rows(self):
        soup = self.get_soup(url=self.base_url+self.club_list_endpoint)
        rows = self.get_elements(soup=soup, selector=self.club_list_tag)
        return rows
    
    def get_teams(self):
        rows = self.get_team_rows()
        for row in rows:
            team_name = self.get_element(soup=row, selector=self.club_name_tag).get_text()
            
            if self.league_name != "Serie A": club_url = self.base_url+row.attrs["href"]
            else: club_url = self.base_url+"team/{}".format(team_name).lower().replace(" ","-")
            soup = self.get_soup(club_url)
            team_url = self.get_element(soup=soup, selector=self.website_tag).attrs["href"]
            if self.league_name == "Serie A":
                self.get_italian_logo()
                team_logo = self.italian_logo[team_name.upper()]
            else:
                team_logo = self.get_element(soup=soup, selector=self.logo_tag[1]).attrs["src"]
                if self.logo_tag[0] == "extend": team_logo = self.base_url+team_logo
            
            kwargs = {"team_name": team_name, "team_url": team_url, "team_logo": team_logo}
            team_dict = {
                "team_name": team_name,
                "team_url": team_url,
                "team_logo": team_logo,
                "squad_url": "",
                "tags": self.tags
            }
            
            with open("./data/data.json","r", encoding='utf-8') as file:
                data = json.load(file)
            data["teams"].append(team_dict)
            
            with open("./data/data.json","w", encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            try:
                Team(
                    league_db_id=self.league_id,
                    **kwargs,
                    POST=True
                )
            except:continue
            
    def get_italian_logo(self):
        with open("data\italian_flags.json","r") as file:
            self.italian_logo = json.load(file)
    
    
    @property
    def tags(self):
        return {
                "player_url_tag"      : "",
                "player_name"         : "",
                "player_national_team": "",
                "player_age"          : "",
                "player_pos"          : "",
                "player_weight"       : "",
                "player_height"       : "",
                "player_num"          : "",
                "player_img"          : ""
            }




class TeamCrawler(Crawler):
    def __init__(self, team_name: str, squad_url: str, tags: dict[str, str]) -> None:
        super().__init__()
        self.squad_url = squad_url
        self.team_name = team_name
        self.tags      = tags
        self.players   = []
        self.load_headers()
        self.get_team_id()
        print(self)
    
    def __str__(self):
        return "<TeamCrawler name={}>".format(self.team_name)
    
    def get_team_id(self):
        load_dotenv()
        self.team_id = os.getenv(unidecode.unidecode(self.team_name.replace(" ", "").lower()))
    
    
    def process_data(self, data): pass
    
    def post_players(self):
        for player_data in self.players:
            Player(**player_data, POST=False)
        
    def get_players(self):
        soup = self.get_soup(self.squad_url)
        for row in soup.select(selector = self.tags["player_url_tag"]):
            player_url = row.find(name="a").attrs["href"]
            player_soup = self.get_soup(player_url)
            
            player_data = {"team_page_id": self.team_id}
            
            for tag in list(self.tags.keys())[1:]:
                player_data[tag] = self.get_element(player_soup, self.tags[tag])
            
            try: self.process_data(player_data)
            except: continue
                
            self.players.append(player_data) 



# "tags": {
#                 "player_url_tag"      : "",
#                 "player_name"         : "",
#                 "player_national_team": "",
#                 "player_age"          : "",
#                 "player_pos"          : "",
#                 "player_weight"       : "",
#                 "player_height"       : "",
#                 "player_num"          : "",
#                 "player_img"          : ""
#             }


# {
#             "team_name": "FC Barcelona",
#             "team_url": "",
#             "squad_url": "https://www.fcbarcelona.com/en/football/first-team/players",
#             "tags": {
#                 "player_url_tag"      : "div.team-list__person-container",
#                 "player_name"         : "div.player-hero__name",
#                 "player_national_team": "div.player-strip__content > div.player-strip__info:nth-of-type(1)",
#                 "player_age"          : "div.player-strip__content > div.player-strip__info:nth-of-type(2)",
#                 "player_pos"          : "div.player-hero__info-meta",
#                 "player_weight"       : "div.player-strip__content > div.player-strip__info:nth-of-type(3)",
#                 "player_height"       : "div.player-strip__content > div.player-strip__info:nth-of-type(4)",
#                 "player_num"          : "span.player-hero__number",
#                 "player_img"          : "img.player-hero__img"
#             }
#         }