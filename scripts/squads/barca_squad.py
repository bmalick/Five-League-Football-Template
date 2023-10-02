from scripts.squads.barca import FCBarcelona

if __name__ == "__main__":
    barca_tags = {
        "player_url_tag"      : "div.team-list__person-container",
        "player_name"         : "div.player-hero__name",
        "player_national_team": "div.player-strip__content > div.player-strip__info:nth-of-type(1)",
        "player_age"          : "div.player-strip__content > div.player-strip__info:nth-of-type(2)",
        "player_pos"          : "div.player-hero__info-meta",
        "player_weight"       : "div.player-strip__content > div.player-strip__info:nth-of-type(3)",
        "player_height"       : "div.player-strip__content > div.player-strip__info:nth-of-type(4)",
        "player_num"          : "span.player-hero__number",
        "player_img"          : "img.player-hero__img"
    }



    FCBarcelona(
        team_name = "FC Barcelona",
        squad_url = "https://www.fcbarcelona.com/en/football/first-team/players",
        tags = barca_tags
    )