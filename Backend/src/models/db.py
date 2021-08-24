import pymongo

##############################################
# Init DB
try:
    mongo = pymongo.MongoClient("localhost", 27017)
    db = mongo.smts
except pymongo.errors.ConnectionFailure:
    print("Cannot connect to database")