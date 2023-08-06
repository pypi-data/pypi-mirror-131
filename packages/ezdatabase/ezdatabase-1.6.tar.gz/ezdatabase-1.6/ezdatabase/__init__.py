import json
from base64 import b64encode, b64decode

class db(list):
    def __init__(self, database_name: str) -> None:
        """Initializes the Database

        Args:
            database_name (str): The Name of the Database with ending
        """
        self.database_name = str(database_name)
        try:
            with open(database_name, "r") as f:
                json.load(f)
        except:
            with open(database_name, "w") as s:
                s.write("[]")
                s.close()
        return None

    def __getitem__(self, key: str):
        try:
            with open(self.database_name, "r") as f:
                js = json.load(f)
            for x in js:
                if x["key"] == key:
                    type_ = x["type"]
                    if type_ == "<class 'bytes'>":
                        return b64decode(str(x["value"]).encode('utf-8')).decode('utf-8')
                    return x["value"]
            return None
        except Exception as e:
            print(e)
            return False
    
    def __setitem__(self, key: str, value) -> bool:
        type_ = type(value)
        if type_ == bytes:
            value = b64encode(value).decode('utf-8')
        try:
            with open(self.database_name, "r") as f:
                js = json.load(f)
            for x in js:
                if x["key"] == key:
                    x["value"] = value
                    x["type"] = str(type_)
                    with open(self.database_name, "w") as f:
                        json.dump(js, f)
                    return True
            js.append({"key": key, "value": value, "type": str(type_)})
            with open(self.database_name, "w") as f:
                json.dump(js, f)
            return True
        except Exception as e:
            print(e)
            return False

    def __delitem__(self, key: str) -> bool:
        try:
            deleted = False
            with open(self.database_name, "r") as f:
                js = json.load(f)
            for x in js:
                if x["key"] == key:
                    js.remove(x)
                    deleted = True
            with open(self.database_name, "w") as f:
                json.dump(js, f)
            return deleted
        except Exception as e:
            print(e)
            return False

    def __len__(self) -> int:
        with open(self.database_name, "r") as f:
            js = json.load(f)
        return len(js)

    def __iter__(self):
        with open(self.database_name, "r") as f:
            js = json.load(f)
        for x in js:
            yield x["key"]