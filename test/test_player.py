import sys
sys.path.append("./src")

import os
from dotenv import load_dotenv

from player import Player

if __name__ == "__main__":
    
    load_dotenv()
    BARCA_PAGE_ID = os.getenv("fcbarcelona")
    Player(
        team_page_id         = BARCA_PAGE_ID,
        player_name          = "Pedri",
        player_national_team = "Spain",
        player_age           = 21,
        player_pos           = "MIDFIELDER",
        player_weight        = 60,
        player_height        = 174,
        player_num           = 8,
        player_img           = "https://www.fcbarcelona.com/photo-resources/2022/11/02/b6748d23-c5f6-47d2-8cc2-9fcebff5e0a1/mini_08-PEDRI.png?width=670&height=790",
        player_promo         = "The player enjoys playing on the front foot, driving at his direct opponent and having his passes break the defensive lines",
        player_honours       = None,
        POST                 = False
    )