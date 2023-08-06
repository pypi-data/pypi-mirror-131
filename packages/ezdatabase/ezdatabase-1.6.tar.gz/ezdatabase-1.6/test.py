from ezdatabase import db

database = db("MyDatabase.db")

sas = bytes("ses".encode("ascii"))
database["sese"] = bytes(sas)
database["ses"] = {"sas": "sase"}
for x in database:
    print(x)
print(len(database))