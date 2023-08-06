from tinydb import Query, TinyDB


class SimpleKeyValueDb:
    def __init__(self, filename):
        self.db = TinyDB(filename, sort_keys=True, indent=4)

    def load(self, key):
        query = Query()
        result = self.db.search(query.key == key)

        if not result:
            return

        return result[0]["value"]

    def save(self, key, value):
        self.db.insert({"key": key, "value": value})
