import sys; sys.path.append("./")

from src.create.payloads import PlayerPayload
from src.utils import Utils

class Player:
    NOTION_ENDPOINT = "https://api.notion.com/v1/pages"

    def __init__(
        self, team: str,
        player_name: str, player_national_team: str,
        player_age: int, player_pos: str, player_weight: int, player_height: int,
        player_num: int, player_img: str,
        post: bool = True
        ) -> None:

        self.player_name = player_name
        self.player_pos  = player_pos.upper()
        self.post        = post
        
        self.params = {
            "team"                 : team,
            "player_name"          : player_name,
            "player_national_team" : player_national_team,
            "player_age"           : player_age,
            "player_pos"           : self.player_pos,
            "player_weight"        : player_weight,
            "player_height"        : player_height,
            "player_num"           : player_num,
            "player_img"           : player_img,
        }

        self.__call__()
        print(self)
        
    def __str__(self) -> str:
        return "<Player name={}, position={}>".format(self.player_name, self.player_pos)

    
    def __call__(self):
        
        payload = PlayerPayload(params=self.params)
        if self.post:
            Utils.post(endpoint=self.NOTION_ENDPOINT, payload=payload)

        
        # payload["children"][0]["heading_1"]['rich_text'][0]["text"]["content"]    = self. player_promo
        
        # if self.player_honours != None:
        #     payload["children"] += [
        #             {
        #                 "object": "block",
        #                 "type": "heading_3",
        #                 "heading_3": {"rich_text": [{"text": {"content": honour}}]}
        #             }
        #         for honour in self.player_honours]
