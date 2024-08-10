import yaml, requests
from typing import Union, List, Dict, Any


def read_yaml(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(filename: str, data: dict):
    with open(filename, 'w') as f:
        yaml.safe_dump(data, f)


class Parameters:
    def save_parameters(self, ignore: list[str] = None, **kwargs):
        ignore = ignore or []
        for k, v in kwargs.items():
            if k not in ignore: setattr(self, k, v)


def update_dict_from_path(dictionnary: Dict, path: str, value: Union[str, List]) -> Dict:
    keys = path.split('.')
    current = dictionnary
    for key in keys[:-1]:
        if '[' in key:
            key_split = key.split('[')
            key = key_split[0]
            idx = int(key_split[1][:-1])
            try:
                current = current[key][idx]
            except:
                current = current[key]
                current.append({})
                current = current[-1]
        else:
            if key not in current:
                current[key] = {}
            current = current[key]
    current[keys[-1]] = value
    return dictionnary

class NotionObject:
    _objects_fname = "objects.yaml"
    def __init__(self, name: str):
        self.name = name
    
    @property
    def objects(self) -> dict: return read_yaml(self._objects_fname)
    
    def __call__(self, values: dict) -> Dict:
        if values is None: return None
        args = self.objects[self.name].copy()
        item = args["object"].copy()
        paths = args["paths"]
        for name, val in values.items():
            if args.get("extend_paths", False):
                try:
                    idx = int(name[-1])
                    val_extend = paths[name[:-1]].replace('0', str(idx))
                    paths[name] = val_extend
                except: pass
            item = update_dict_from_path(item, paths[name], val).copy()
        return item


class NotionApiHandler(Parameters):
    _keys_fname = "keys.yaml"
    _objects_fname = "objects.yaml"
    _pages_endpoint = "https://api.notion.com/v1/pages"
    _database_endpoint = "https://api.notion.com/v1/databases"
    _query_endpoint = "https://api.notion.com/v1/databases/%s/query"
    _max_chars = 1999

    def __init__(self) -> None:
        self.set_headers()
    
    @property
    def keys(self) -> None: return read_yaml(self._keys_fname)
    
    def set_headers(self) -> None:
        self.headers ={
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
            "Authorization": "Bearer %s" % self.keys.get("api_token")
        }
    
    @property
    def objects(self) -> dict: return read_yaml(self._objects_fname)

    def fill_object(self, property_object: str, property_values: List[Any]) -> Dict:
        assert isinstance(property_values, list), "Enter a list please."
        args = self.objects[property_object].copy()
        item = args["object"].copy()
        for path, value in zip(args["paths"], property_values):
            item = update_dict_from_path(item, path, value).copy()
        return item

    def create_page(self, parent_id: str, page_title: str, icon: str = None, cover: str = None):
        response = requests.post(
            url=self._pages_endpoint,
            headers=self.headers,
            json={
                "parent": NotionObject("page_parent")({"id": parent_id}),
                "icon": NotionObject("icon")({"url": icon}),
                "cover": NotionObject("icon")({"url": cover}),
                "properties": {
                    "title": {"id": "title", "type": 'title', **NotionObject("page_title")({"title": page_title})}
                }
                
            }
        )
        try:
            response.raise_for_status()
            url = response.json()["url"]
            print("Page creation")
            print("%s: %s" % ("Name".rjust(10), page_title))
            print("%s: %s" % ("URL".rjust(10), url))
        except:
            print(response.text)

    def retrieve_page(self, page_id: str):
        response = requests.get(
            url=f"{self._pages_endpoint}/{page_id}",
            headers=self.headers
        )
        try:
            response.raise_for_status()
            return response.json()
        except:
            print("FAIL\n\n")
            print(response.text)
    
    def create_database(self, parent_id: str, db_title: str, properties: list[dict]):
        init_properties = self.objects["init_properties"]
        properties = {
            item["name"]: init_properties[item["type"]]
            for item in properties
        }
        response = requests.post(
            url=self._database_endpoint,
            headers=self.headers,
            json={
                "parent": NotionObject("database_parent")({"id": parent_id}),
                **NotionObject("page_title")({"title": db_title}),
                "properties": {"Name": {"title": {}}, **properties}
            }
        )
        try:
            response.raise_for_status()
            url = response.json()["url"]
            print("Database creation")
            print("%s: %s" % ("Name".rjust(10), db_title))
            print("%s: %s" % ("URL".rjust(10), url))
        except:
            print("FAIL\n\n")
            print(response.text)

    def create_page_in_database(self, database_id: str, data: dict):
        response = requests.post(
            url=self._pages_endpoint,
            headers=self.headers,
            json={
                "parent": NotionObject("database_parent")({"id": database_id}),
                "icon": NotionObject("icon")(data.get("icon")),
                "cover": NotionObject("icon")(data.get("cover")),
                "properties": {
                    item["name"]: NotionObject(item["type"])(item["values"])
                    for item in data["properties"]
                },
                "children": [
                    NotionObject(item["type"])(item["values"])
                    for item in data.get("children", [])
                ]
            }
        )
        try:
            response.raise_for_status()
            return response.json()
        except:
            print(response.text)
    
    def query_database(self, database_id: str, limit: int = 10, filters: dict = {"or": []}) -> List[dict]:
        response = requests.post(
            url=self._query_endpoint % database_id,
            headers=self.headers,
            json={
                "page_size": limit,
                "filter": filters
            }
        )
        try:
            response.raise_for_status()
            return response.json()["results"]
        except:
            print(response.text)
    
    @staticmethod
    def extend_rich_text(text):
        return {f"text{i+1}": text[i*2000:(i+1)*2000] for i in range(len(text)//2000+1)}

    def delete_page(self, page_id: str):
        response = requests.patch(
            url=self._pages_endpoint + f"/{page_id}",
            headers=self.headers,
            json={"archived": True}
        )
        response.raise_for_status()
        try:
            response.raise_for_status()
            print(page_id + " deleted")
        except:
            print(response.text)