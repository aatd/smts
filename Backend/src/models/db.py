import pymongo
import os

##############################################
# Init DB
# # Init DB
try:

    if os.environ.get("DATABASE_IP") is not None:
        db_location = os.environ["DATABASE_IP"] + ":27017"
    else:
        db_location = "localhost:27017"

    print("Trying to connect to Device-DB located at: " +
          db_location)
    #mongo = pymongo.MongoClient(os.environ["DATABASE_IP"], 27017)
    mongo = pymongo.MongoClient(
        db_location, serverSelectionTimeoutMS=1000).smts
    db = mongo

    print(
        "Trying to connect to DB located at: "
        + db_location
        + "...Successful"
    )


except pymongo.errors.ConnectionFailure as err:

    if os.environ.get("DATABASE_IP") is not None:
        db_location = os.environ["DATABASE_IP"] + ":27017"
    else:
        db_location = "localhost:2017"

    print(
        "Trying to connect to Device-DB located at: "
        + db_location
        + "...Failed...Err: "
        + str(err)
    )
    exit(1)
