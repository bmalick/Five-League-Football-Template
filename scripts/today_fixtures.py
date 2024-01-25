import sys; sys.path.append("./")

from src.calendars.laliga import LaLigaCalendar
from src.calendars.bundesliga import BundesligaCalendar
from src.calendars.ligue1 import Ligue1Calendar
from src.calendars.premierleague import PremierLeagueCalendar
from src.calendars.scores import UpdateScore

CALENDARS = [
    LaLigaCalendar, Ligue1Calendar, PremierLeagueCalendar,
    # BundesligaCalendar,
]

def main():
    for calendar in CALENDARS:
        league_name = calendar.league_name
        gameweek = UpdateScore.get_league_gameweek(league_name)
        calendar.update_scores(gameweek)

if __name__ == "__main__": main()