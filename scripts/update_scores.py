import sys; sys.path.append("./src")
from argparse import ArgumentParser

from calendars.laliga import LaLigaCalendar
from calendars.bundesliga import BundesligaCalendar
from calendars.ligue1 import Ligue1Calendar
from calendars.premierleague import PremierLeagueCalendar

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
    name = args.league.lower()
    week = args.week
    CALENDARS.get(name).update_scores(week)


if __name__ == "__main__":
    main()