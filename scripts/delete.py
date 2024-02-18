import sys; sys.path.append("./")

from argparse import ArgumentParser

from src.calendars.laliga import LaLigaCalendar
from src.calendars.bundesliga import BundesligaCalendar
from src.calendars.ligue1 import Ligue1Calendar
from src.calendars.premierleague import PremierLeagueCalendar
from src.calendars.scores import UpdateScore

CALENDARS = {
    "laliga": LaLigaCalendar,
    "liga": LaLigaCalendar,
    "ligue1": Ligue1Calendar,
    "bundesliga": BundesligaCalendar,
    "premierleague": PremierLeagueCalendar,
    "pl": PremierLeagueCalendar,
    # "seriea": SerieACalendar
}

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "-l", "--league",
        type=str, required=True,
        help="Name of the league without space."
    )

    parser.add_argument(
        "-w", "--week",
        type=int, required=True,
        help="Gameweek whom you would like to update scores' fixtures."
    )

    args = parser.parse_args()
    league = args.league.lower()
    week = args.week

    UpdateScore.delete_gameweek(
        league=league,
        gameweek=week
    )
    
    # CALENDARS.get(league).get_fixtures(gameweek=week)


if __name__ == "__main__":
    main()