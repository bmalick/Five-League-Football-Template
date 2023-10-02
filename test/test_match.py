import sys
sys.path.append("./src")

import os
from dotenv import load_dotenv

from match import Match


if __name__ == "__main__":
    load_dotenv()
    PL_ID = os.getenv("premierleague")

if __name__ == "__main__":
    Match(
       league_db_id  = PL_ID,
       matchday      = "Friendly Match",
       match_date    = "2023-07-29 23:00",
       home_team     = "Manchester City",
       away_team     = "Arsenal",
       POST          = True
   )