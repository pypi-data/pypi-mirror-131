import pymongo


def get_pymongo_client(host="9.25.181.135", port=27017):
    mongo_client = pymongo.MongoClient(
        host,
        port,
    )
    return mongo_client


def _insert_mongo(
    collection_name, data, db_name="Dataset", host="9.25.181.135", port=27017
):
    mongoclient = get_pymongo_client(host, port)
    mongo_db = mongoclient[db_name]
    mongo_col_tag = mongo_db[collection_name]
    mongo_col_tag.insert_many(data)
    mongoclient.close()


def _search_mongo(data):
    mongoclient = get_pymongo_client(data["host"], data["port"])
    mongo_db = mongoclient[data["db_name"]]
    mongo_col = mongo_db[data["collection_name"]]
    key = data["key"]
    cursor = mongo_col.find({key: {"$in": data["content"]}})
    result = []
    for entity in cursor:
        result.append(entity)
    mongoclient.close()
    return result


def _delete_mongo(data):
    mongoclient = get_pymongo_client(data["host"], data["port"])
    mongo_db = mongoclient[data["db_name"]]
    mongo_col = mongo_db[data["collection_name"]]
    key = data["key"]
    result = mongo_col.delete_many({key: {"$in": data["content"]}})
    mongoclient.close()


def _update_mongo(data):
    mongoclient = get_pymongo_client(data["host"], data["port"])
    mongo_db = mongoclient[data["db_name"]]
    mongo_col = mongo_db[data["collection_name"]]
    content = data["content"]
    keys = data["keys"]
    for value in content:
        tmp = {}
        for i, key in enumerate(keys):
            if i == 0:
                query = {key: value[key]}
            else:
                tmp[key] = value[key]
        new = {"$set": tmp}
        mongo_col.update_one(query, new)
    mongoclient.close()
