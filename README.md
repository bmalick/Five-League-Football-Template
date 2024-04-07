# Five League Football Template

This project aims to create datasets of Football fixtures into your Notion page.
The teams and fixtures are taken from official leagues calendars and then they are embedded into Notion page.
The fetching of gameweek matches are scraped and there are commands to have updates every week.
Note that only Laliga, Premier League and Bundesliga and Ligue1 matches are available. Serie A fixtures are coming soon.


# Notion API
Notion API is used for page creation. Follow the description [here](https://developers.notion.com/docs/authorization) to create your Notion Integration.




<!-- IMAGE DE LA PAGE -->


# Makefile commands

- calendar: Create Notion pages of matches available since the gameweek 1 when given the league name. league arguments must be: liga, laliga, pl, premierleague, bundesliga and ligue1
    ```bash
    make calendar league=[league name]
    ```
- gameweek: Some of the fixtures are not yet available. So create them via this command.
    ```bash
    make gameweek league=[league name] week=[gameweek num]
    ```

- update: Find matches scores of the gameweek for a given league and update pages in Notion.
    ```bash
    make update league=[league name] week=[gameweek num]
    ```
- today: Update matches results that occur today for all leagues.
    ```bash
    make today
    ```
- delete: Delete a whole league gameweek pages in Notion.
    ```bash
    make delete league=[league name] week=[gameweek num]
    ```
