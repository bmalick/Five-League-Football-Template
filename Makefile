
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
	@python ./test/test_player.py

test-team:
	@python ./test/test_team.py

test-match:
	@python ./test/test_match.py

test-league:
	@python ./test/test_league.py 


# Fixtures

calendar:
	@python ./scripts/create_calendar.py \
	--league $(league)

today:
	@python ./scripts/today_fixtures.py 


# laliga-calendar:
# 	@python ./src/laliga_calendar.py

# fetch-barca-squad:
# 	@python ./src/barca_squad.py

# bundesliga-calendar:
# 	@python ./scripts/bundesliga_calendar.py

# premier-league-calendar:
# 	@python ./scripts/premier_league_calendar.py

# laliga-calendar:
# 	@python ./scripts/laliga_calendar.py

update:
	@python ./scripts/update_scores.py \
	--league $(league) \
	--week $(week)

delete:
	@python ./scripts/delete.py \
	--league $(league) \
	--week $(week)

gameweek:
	@python ./scripts/gameweek.py \
	--league $(league) \
	--week $(week)


# instructions:
# 	@start "" instructions.pdf
