import sys; sys.path.append("./")

from argparse import ArgumentParser
from src.league import LaLiga, Bundesliga, PremierLeague
from src.utils import read_yaml
objects = {
    "laliga": LaLiga,
    "bundesliga": Bundesliga,
    "premierleague": PremierLeague,
}

names = {
    "liga": "laliga",
    "pl": "premierleague",
}

def main(args) -> None:
    name = names.get(args.league, args.league)
    data = read_yaml("build.yaml")
    try:
        league = objects[name](**data[name])
        league.get_teams()
    except: print(f"{name} not found")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-l", "--league",
        type=str, required=True,
        help="Name of the league without space."
    )
    args = parser.parse_args()
    main(args)