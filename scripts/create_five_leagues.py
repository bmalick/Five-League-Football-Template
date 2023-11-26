import sys, json
sys.path.append("./src")

from create.league import League

def main() -> None:

    with open("./data/data.json") as file:
        data = json.load(file)
    leagues_data = data["leagues"]
    for row in leagues_data:
        kwargs = row["class_kwargs"]
        League(**kwargs)

    
if __name__ == "__main__":
    main()