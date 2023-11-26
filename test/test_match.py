import sys
sys.path.append(".")
sys.path.append("src")

from src.match import Match

if __name__ == "__main__":
    Match(
       league        = "premierleague",
       matchday      = "Test Match",
       match_date    = "2024-11-20 20:00",
       home_team     = "Manchester City",
       away_team     = "Arsenal",
       post          = True
   )