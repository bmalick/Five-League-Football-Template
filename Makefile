GREEN := 32
RED := 31
RESET := 

all:
	@echo
	@echo "Type the following commands in order to run the files."
	@echo 
	@echo "------------------------------"
	@echo "make install			<- install the required modules."
	@echo "make test-player		<- Fetch a player. Set POST to True if you want to create the player page in your database"
	@echo "make test-team		<- Fetch a team. Set POST to True if you want to create the team page in your database"
	@echo "make test-match		<- Fetch a match. Set POST to True if you want to create the match page in your database"

install:
	@pip install -r requirements.txt

test-player:
	@python3 ./test/test_player.py

test-team:
	@python3 ./test/test_team.py

test-match:
	@python3 ./test/test_match.py

laliga-teams:
	@python3 ./src/laliga_teams.py

laliga-calendar:
	@python3 ./src/laliga_calendar.py

fetch-barca-squad:
	@python3 ./src/barca_squad.py

bundesliga-calendar:
	@python3 ./scripts/bundesliga_calendar.py

premier-league-calendar:
	@python3 ./scripts/premier_league_calendar.py

laliga-calendar:
	@python3 ./scripts/laliga_calendar.py



# instructions:
# 	@start "" instructions.pdf