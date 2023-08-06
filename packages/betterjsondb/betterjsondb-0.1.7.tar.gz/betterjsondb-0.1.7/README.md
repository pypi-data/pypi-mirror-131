# Betterjson
Library for easier working with JSON files in Python

# Quick example
```json
{"names": ["Alex", "Allan"]}
```
```py
import betterjsondb

db = betterjsondb.connect(file="tests.json", prefix="~")                  # Name of file and prefix can be custom

print(                                                                    # In concole you'll see:
    db.get("all"),                                                        # {'names': ['Alex', 'Allan']}
    db.push("cars", {"BMW": "car", "Tosiba": "not_car"}, callback=True),  # True
    db.update("cars", "=", {"BMW": "car"}, callback=True),                # True
    db.delete("names", callback=True),                                    # True
    db.get("all")                                                         # {'cars': {'BMW': 'car'}}
)
```

# Important information
Sorry, for now it's not full description, later we'll open our [GitHub Page](https://github.com/DarkJoij/betterjsondb).