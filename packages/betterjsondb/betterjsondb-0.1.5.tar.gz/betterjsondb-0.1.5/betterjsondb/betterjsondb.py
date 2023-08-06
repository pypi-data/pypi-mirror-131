#!usr/bin/python3

def get_standarts_read(filename: str) -> str:
    """Return standart code for exec().reading."""
    return f"""from json import load\n\nwith open("{filename}", "r") as dbfile:\n    data = load(dbfile)\n\n"""


def get_standarts_write(filename: str) -> str:
    """Return standart code for exec().writing."""
    return f"""from json import dump\n\nwith open("{filename}", "w") as dbfile:\n    dump(data, dbfile)\n\n"""


def splitter(key: str, prefix: str) -> str:
    """Split key by its prefix."""
    key = key.split(prefix)
    if type(key) is list:
        tojsonpath = "".join(f"['{i}']" for i in key)
    else:
        tojsonpath = f"['{key}']"

    return tojsonpath


class connect:
    """Class that being container for working with database files."""
    def __init__(self, file: str, prefix: str):
        self.file = file
        self.prefix = prefix

    def get(self, key: str):
        """Search and return key from database file if exists, in else you'll get error."""
        result = {}
        exec(f"{get_standarts_read(self.file)}final_result = data{splitter(key, self.prefix)}", result)
        return result["final_result"]

    def push(self, key: str, value, callback: bool = None):
        """Write information to database file if key's NOT exists.
        So function, create key and after update data here."""
        if type(value) is str:
            value = f"'{value}'"
        value_class = str(value.__class__)[8:][:-2]

        exec(f"{get_standarts_read(self.file)}data{splitter(key, self.prefix)} = {value_class}({value})\n\n{get_standarts_write(self.file)}")
        if callback:
            return True

    def update(self, key: str, operator: str, value, callback: bool = None):
        """Write information to database file if key's EXISTS."""
        if type(value) is str:
            value = f"'{value}'"
        value_class = str(value.__class__)[8:][:-2]

        exec(f"{get_standarts_read(self.file)}data{splitter(key, self.prefix)} {operator} {value_class}({value})\n\n{get_standarts_write(self.file)}")
        if callback:
            return True

    def delete(self, key: str, callback: bool = None):
        """Delete information from database file."""
        exec(f"{get_standarts_read(self.file)}del data{splitter(key, self.prefix)}\n\n{get_standarts_write(self.file)}")
        if callback:
            return True
