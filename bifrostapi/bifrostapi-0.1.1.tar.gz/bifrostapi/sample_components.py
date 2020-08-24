import pymongo

from .utils import get_connection, date_now


def save_sample_component(data_dict, connection_name="default"):
    """COPIED FROM BIFROSTLIB. Insert sample dict into mongodb.
    Return the dict with an _id element"""
    connection = get_connection(connection_name)
    db = connection.get_database()
    sample_components_db = db.sample_components
    now = date_now()
    data_dict["metadata"] = data_dict.get("metadata", {'created_at': now})
    data_dict["metadata"]["updated_at"] = now
    if "_id" in data_dict:
        data_dict = sample_components_db.find_one_and_update(
            filter={"_id": data_dict["_id"]},
            update={"$set": data_dict},
            # return new doc if one is upserted
            return_document=pymongo.ReturnDocument.AFTER,
            # This might change in the future. It doesnt make much sense with our current system.
            upsert=True
            # Import relies on this to be true.
            # insert the document if it does not exist
        )

    else:
        search_fields = {
            "sample._id": data_dict["sample"]["_id"],
            "component._id": data_dict["component"]["_id"],
        }
        data_dict = sample_components_db.find_one_and_update(
            filter=search_fields,
            update={
                "$set": data_dict
            },
            # return new doc if one is upserted
            return_document=pymongo.ReturnDocument.AFTER,
            upsert=True  # insert the document if it does not exist
        )

    return data_dict
