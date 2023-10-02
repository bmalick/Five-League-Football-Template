from laliga import gameday
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--week",type=int)
    args = parser.parse_args()
    week = args.week
    gameday(week)