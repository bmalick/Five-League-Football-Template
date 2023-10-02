import os, requests, unidecode
from dotenv import load_dotenv

def main() -> None:

    load_dotenv()
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    TEAMS_DB_ID    = os.getenv("TEAMS_DB_ID")
    DATABASE_ENDPOINT = "https://api.notion.com/v1/databases/"
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": "Bearer " + NOTION_API_KEY 
    }

    response = requests.post(DATABASE_ENDPOINT+TEAMS_DB_ID+"/query", headers=headers)
    response.raise_for_status()
    data = response.json()

    teams = data["results"]
    with open("./data/teams_id.txt","w") as txt:
        for team in teams:
            id   = team["url"].split("-")[-1]
            name = team["properties"]["Name"]["title"][0]["text"]["content"]
            name = unidecode.unidecode(name.replace(" ", "").lower())
            txt.write("{} = {}\n".format(name,id))

if __name__ == "__main__":
    main()