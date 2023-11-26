import sys
sys.path.append("./src")

from team import Team

if __name__ == "__main__":

    Team(
        league         = "laliga",
        team_name = "Supas Strikas",
        team_url       = "https://www.mancity.com/",
        team_logo      = "https://www.mancity.com/dist/images/logos/crest.svg",
        post           = True
    )