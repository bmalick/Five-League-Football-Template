import sys
sys.path.append("./src")

import os
from dotenv import load_dotenv

from league import League

if __name__ == "__main__":
    load_dotenv()
    LEAGUES_DB_ID = os.getenv("LEAGUES_DB_ID")

if __name__ == "__main__":
    League(
        name     = "La Liga",
        url      = "https://www.laliga.com/en-GB",
        logo_tag = "",
        POST     = False
    )