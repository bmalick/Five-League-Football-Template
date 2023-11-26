from calendars.crawlers import TeamCrawler
import re, time

class FCBarcelona(TeamCrawler):
    def __init__(self, team_name: str, squad_url: str, tags: dict[str, str]) -> None:
        super().__init__(team_name, squad_url, tags)
        self.get_players()
        self.post_players()
    
    def process_data(self, data):
        
        for key in data:
            if key not in ["team_page_id", "player_img", "player_honours"]:
                if data[key] is None : data[key] = ""
                else: data[key] = data[key].get_text()
        
        # Name
        data["player_name"] =  re.sub("\n | \s+", " ", data["player_name"]).split()
        data["player_name"] =  " ".join(data["player_name"][1:])
        
        raw_data = {}
        for key in ["player_national_team", "player_age", "player_weight", "player_height"]:
            split = [elem for elem in data[key].split("\n") if elem!=""]
            try: raw_data[split[0]] = split[1]
            except: continue
            
        if "Place of birth" in raw_data.keys(): data["player_national_team"] = raw_data["Place of birth"]
        else: data["player_national_team"] = data["player_national_team"] = ""
        
        if "Date of birth" in raw_data.keys(): data["player_age"] = raw_data["Date of birth"]
        else: data["player_age"] = 0
        
        data["player_weight"] = raw_data["Weight"]
        data["player_height"] = raw_data["Height"]
        
        # National Team
        if data["player_national_team"] != "":
            data["player_national_team"] = data["player_national_team"].split(",")[-1].rstrip().lstrip()
        
        # Age
        if data["player_age"] != 0: 
            data["player_age"] = data["player_age"].split("/")[-1].rstrip()
            data["player_age"] = time.localtime().tm_year - int(data["player_age"])
        
        # Weight
        data["player_weight"] = data["player_weight"].replace("kg","")
        data["player_weight"] = int(data["player_weight"])
        
        # Height
        data["player_height"] = data["player_height"].replace("cm","")
        data["player_height"] = int(data["player_height"])
        
        # Number
        
        if data["player_num"] == "": data["player_num"] = 0
        else: data["player_num"] = int(data["player_num"])
        
        # Image
        data["player_img"] = data["player_img"].attrs["src"]
        
        # Honours
        
        # def get_honour_format(elem):
        #     player_honour_title = elem.find(attrs={"class": "player-honour__title"}).get_text()
        #     player_honour_dates = elem.find(attrs={"class": "player-honour__dates"}).get_text().split()
        #     player_honour_dates = [dates for dates in player_honour_dates if len(dates)>1]
        #     player_honour_title_total = len(player_honour_dates)
        #     player_honour_dates = " | ".join(player_honour_dates)
        #     player_honour_data_meta = "{} {}🏆 → {}".format(player_honour_title, player_honour_title_total, player_honour_dates)
        #     return player_honour_data_meta
        
        # if data["player_honours"] != None:
        #     data["player_honours"] = [get_honour_format(elem) for elem in data["player_honours"]]