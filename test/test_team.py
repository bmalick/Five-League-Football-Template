import sys; sys.path.append("./")

from src.create.team import Team

if __name__ == "__main__":

    Team(
        league    = "laliga",
        team_name = "Supa Strikas",
        team_url  = "supastrikas.com",
        team_logo = "https://pbs.twimg.com/profile_images/640891952834215936/FwueNEWL_400x400.png",
        post      = True
    )