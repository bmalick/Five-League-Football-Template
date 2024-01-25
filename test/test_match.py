import sys; sys.path.append("./")

from datetime import datetime
from src.create.match import Match

if __name__ == "__main__":
    Match(
       league     = "fcbarcelona",
       matchday   = "Test Match",
       match_date = datetime.today().strftime("%Y-%m-%d %H:%M"),
       home_team  = "FC Barcelona",
       away_team  = "Real Madrid",
       post       = True
   )
