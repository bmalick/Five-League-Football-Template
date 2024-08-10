import concurrent.futures
from src.notion import NotionApiHandler
import requests

def delete_all_fixtures():
    api_handler = NotionApiHandler()
    def get_fixtures():
        return api_handler.query_database(
                database_id=api_handler.keys["matches_db_token"],
                limit=100
            )
    while True:
        fixtures = get_fixtures()
        if len(fixtures)==0: break
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for fixture in fixtures:
                futures.append(executor.submit(api_handler.delete_page, fixture["id"]))
            for future in concurrent.futures.as_completed(futures):
                future.result()


            


