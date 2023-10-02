from dotenv import load_dotenv
import os, requests

class Player:
    def __init__(
        self, team_page_id: str,
        player_name: str, player_national_team: str,
        player_age: int, player_pos: str, player_weight: int, player_height: int,
        player_num: int, player_img: str,
        POST: bool = True
        ) -> None:
        
        self.team_page_id         = team_page_id
        self.player_name          = player_name
        self.player_national_team = player_national_team
        self.player_age           = player_age
        self.player_pos           = player_pos.capitalize()
        self.player_weight        = player_weight
        self.player_height        = player_height
        self.player_num           = player_num
        self.player_img           = player_img
        self.POST                 = POST
        
        self.NOTION_ENDPOINT = "https://api.notion.com/v1/"
        self.load_env()
        self.load_headers()
        self.create_player()
        
        print(self)
        
    def __str__(self) -> str:
        return "<Player name={}, position={}>".format(self.player_name, self.player_pos)
    
    def load_env(self):
        load_dotenv()
        self.PLAYERS_DB_ID = os.getenv("PLAYERS_DB_ID")
        self.NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    
    def load_headers(self) -> None:
        self.headers = {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
            "Authorization": "Bearer " + self.NOTION_API_KEY 
        }
    
    def create_player(self):
        
        payload = self.get_payload()
        if self.POST:
            response = requests.post(self.NOTION_ENDPOINT+"pages/", headers=self.headers, json=payload)
            response.raise_for_status()
    
    def get_payload(self) -> dict:
        
        payload = self.player_payload
        
        payload["icon"]["external"]["url"]                                        = self.player_img
        payload["cover"]["external"]["url"]                                       = self.player_img
        payload["properties"]["Name"]["title"][0]["text"]["content"]              = self.player_name
        payload["properties"]["Club"]["relation"][0]["id"]                        = self.team_page_id
        payload["properties"]["National Team"]["rich_text"][0]["text"]["content"] = self.player_national_team
        payload["properties"]["Age"]["number"]                                    = self. player_age
        payload["properties"]["Position"]["select"]["name"]                       = self.player_pos
        payload["properties"]["Weight"]["number"]                                 = self.player_weight
        payload["properties"]["Height"]["number"]                                 = self.player_height
        payload["properties"]["Jersey Number"]["number"]                          = self.player_num
        # payload["children"][0]["heading_1"]['rich_text'][0]["text"]["content"]    = self. player_promo
        
        # if self.player_honours != None:
        #     payload["children"] += [
        #             {
        #                 "object": "block",
        #                 "type": "heading_3",
        #                 "heading_3": {"rich_text": [{"text": {"content": honour}}]}
        #             }
        #         for honour in self.player_honours]
        
        return payload

    @property
    def player_payload(self) -> dict:
        
        payload = {
            "parent": {
                "type": "database_id",
                "database_id": self.PLAYERS_DB_ID
            },
            
            "icon": {
                "type": "external",
                "external": {"url": ""}
            },
            
            "cover": {
                "type": "external",
                "external": {"url": ""}
            },
            
            "properties": {
                "Name": {
                    "title": [{
                        "text": {"content": ""}
                    }]
                },
                "Club": {
                    "relation": [{
                        "id": ""
                    }]
                },
                "National Team": {
                    "rich_text": [{
                        "text": {"content": ""}
                    }]
                },
                "Age": {"number": 0},
                "Position": {
                    "select": {"name": ""}
                },
                "Weight": {"number": 0},
                "Height": {"number": 0},
                "Jersey Number": {"number": 0},
            },
            
            # "children": [
            #     {
            #         "object":"block",
            #         "type": "heading_1",
            #         "heading_1" : {"rich_text": [{"text": {"content": ""}}]}
            #     },
                
            #     {
            #         "object": "block",
            #         "type": "divider",
            #         "divider": {}
            #     }
                
            #     ]
        }
        
        return payload