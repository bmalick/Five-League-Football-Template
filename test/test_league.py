import sys; sys.path.append("./")

from src.create.league import League

if __name__ == "__main__":
    League(
        name      = "UCL",
        url       = "https://fr.uefa.com/uefachampionsleague/",
        link_logo = "https://upload.wikimedia.org/wikipedia/fr/thumb/b/bf/UEFA_Champions_League_logo_2.svg/1067px-UEFA_Champions_League_logo_2.svg.png",
        post      = True,
        
    )
