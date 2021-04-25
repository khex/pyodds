import pymongo


"""
mongodb+srv://stavros:balalajka7@cluster0.62wbu.mongodb.net/test
mongodb://stavros:balalajka7@cluster0.62wbu.mongodb.net/test
"""
pref = "mongodb+srv://stavros:balalajka7"
link = "cluster0.62wbu.mongodb.net"
prms = "myFirstDatabase?retryWrites=true&w=majority"
curl = pref + "@" + link + "/" + prms;
client = pymongo.MongoClient(curl)
db = client.test
print(curl)
