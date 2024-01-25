import sys; sys.path.append("./")

from src.create.player import Player

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
        post                 = True
        # player_promo         = "The player enjoys playing on the front foot, driving at his direct opponent and having his passes break the defensive lines",
        # player_honours       = None,
        
    )