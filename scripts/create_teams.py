import sys, json, os
sys.path.append("./src")

from crawlers import LeagueCrawler

def main() -> None:
    with open("./data/data.json") as file:
        data  = json.load(file)
    leagues_data = data["leagues"]
    for row in leagues_data:
        crawler_data = row["crawler_data"]
        kwargs = {
            "name": row["class_kwargs"]["name"],
            "base_url": row["class_kwargs"]["url"],
            **crawler_data
        }
        LeagueCrawler(**kwargs)
        
if __name__ == "__main__":
    main()

