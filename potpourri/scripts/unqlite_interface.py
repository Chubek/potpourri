from unqlite import UnQLite


def store_in_db(unql_path, db_coll, results):
    unql_path_split = unql_path.split(".")

    if unql_path_split[-1] != "db":
        unql_path = unql_path + ".db"

    db = UnQLite(unql_path)


    collection = db.collection(db_coll)

    return collection.store(results)