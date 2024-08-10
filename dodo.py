from doit.tools import Interactive
from doit.action import CmdAction

from src.league import LaLiga, PremierLeague, Bundesliga
import yaml

DOIT_CONFIG = {
    "default_tasks": [],
    "action_string_formatting": "both",
}

def load_config():
    with open("build.yaml", 'r') as f:
        return yaml.safe_load(f)
    
def show_league(task):
    return task.options["league"]

def task_league():
    return {"actions": ["python scripts/create_league.py -l %(league)s"],
            "params": [{"name": "league",
                        "short": "l",
                        "long": "league",
                        "type": str,
                        "help": "League name",
                        "default": ''}],
            "verbosity": 2, "doc": "Create league. Use -l or --league argument.",
            "title": show_league
            }
def task_teams():
    return {"actions": ["python scripts/create_teams.py -l %(league)s"],
            "params": [{"name": "league",
                        "short": "l",
                        "long": "league",
                        "type": str,
                        "help": "League name",
                        "default": ''}],
            "verbosity": 2, "doc": "add teams to league. Use -l or --league argument.",
            "title": show_league
            }
def task_calendar():
    return {"actions": ["python scripts/create_calendar.py -l %(league)s"],
            "params": [{"name": "league",
                        "short": "l",
                        "long": "league",
                        "type": str,
                        "help": "League name",
                        "default": ''}],
            "verbosity": 2, "doc": "Add matches to leagues. Use -l or --league argument.",
            "title": show_league
            }

