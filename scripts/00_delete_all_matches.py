import sys; sys.path.append("./")
# from argparse import ArgumentParser

from src.delete import delete_all_fixtures


# def main() -> None:
#     parser = ArgumentParser()
#     parser.add_argument(
#         "-l", "--league",
#         type=str, required=True,
#         help="Name of the league without space."
#     )

#     parser.add_argument(
#         "-w", "--week",
#         type=int, required=True,
#         help="Gameweek whom you would like to update scores' fixtures."
#     )

#     args = parser.parse_args()
#     league = args.league.lower()
#     week = args.week

#     UpdateScore.delete_gameweek(
#         league=league,
#         gameweek=week
#     )
    
#     # CALENDARS.get(league).get_fixtures(gameweek=week)

def main():
    delete_all_fixtures()

if __name__ == "__main__":
    main()