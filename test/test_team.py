import sys
sys.path.append("./src")

import os
from dotenv import load_dotenv

from team import Team

if __name__ == "__main__":
    load_dotenv()
    LA_LIGA_PAGE_ID = os.getenv("laliga")
    
    Team(
        league_db_id   = LA_LIGA_PAGE_ID,
        team_full_name = "Machester City",
        team_url       = "https://www.mancity.com/",
        team_logo      = "https://www.mancity.com/dist/images/logos/crest.svg",
        POST           = False
    )