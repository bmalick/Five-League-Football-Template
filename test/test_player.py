import sys
sys.path.append(".")
sys.path.append("src")

from src.player import Player

if __name__ == "__main__":

    Player(
        team                 = "fcbarcelona",
        player_name          = "Malick",
        player_national_team = "Senegal",
        player_age           = 22,
        player_pos           = "MIDFIELDER",
        player_weight        = 59,
        player_height        = 185,
        player_num           = 14,
        player_img           = "https://media.licdn.com/dms/image/C4E03AQGJEqrdRuujVQ/profile-displayphoto-shrink_200_200/0/1640821997488?e=1706140800&v=beta&t=y78EaMgwzEXpn8nCDHFo0UOdMGtf6jjK5utqX5ntgiA",
        post                 = True
        # player_promo         = "The player enjoys playing on the front foot, driving at his direct opponent and having his passes break the defensive lines",
        # player_honours       = None,
        
    )